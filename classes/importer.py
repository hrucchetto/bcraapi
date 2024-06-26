import logging
import os
import urllib3
from datetime import date, timedelta
from functools import cached_property

import pandas as pd
import requests
import unidecode
from sqlalchemy import create_engine, text

import classes.configs.queries as queries

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

pd.options.mode.chained_assignment = None
urllib3.disable_warnings()

START_DATE = (date.today() + timedelta(days=-60)).strftime('%Y-%m-%d') 
END_DATE = date.today().strftime('%Y-%m-%d')

class Importer:

    def __init__(
            self, 
            action: str = 'import',
            start_date: date = START_DATE, 
            end_date: date = END_DATE,
            vars: str = None
            
        ):
        self.__base_url = 'https://api.bcra.gob.ar'
        self.__db_name = 'bcra'
        self.__endpoint_ppal_vars = '{BASE_URL}/estadisticas/v2.0/PrincipalesVariables'
        self.__endpoint_var = '{BASE_URL}/estadisticas/v2.0/DatosVariable/{ID}/{START_DATE}/{END_DATE}'
        self.__output_dir = 'outputs'
        self.end_date = end_date if end_date else END_DATE
        self.start_date = start_date if start_date else START_DATE
        self.action = action
        self.vars = list(self._get_ppal_vars) if vars == 'all' else vars.split(',') if vars else None

    @cached_property    
    def _get_ppal_vars(self) -> dict: 
        '''
        Returns a list with all the variables available in BCRA API.
        '''

        LOGGER.info('Get variables from BCRA')
        r = requests.get(
            self.__endpoint_ppal_vars.format(
                BASE_URL=self.__base_url
            ), 
            verify=False
        )

        print(r.status_code)

        if r.status_code == 200:

            results_ppal_vars = r.json()['results']

            all_vars_dict = {}

            for var in results_ppal_vars:
                
                id =  str(var['idVariable'])
                description = var['descripcion']
                all_vars_dict[id] = description 

            return all_vars_dict
        
        else:
            raise Exception("Error during API call")
    
    def __ask_for_vars(self) -> list:
        
        vars = []

        all = str(input('Do you want to include all the variables (yes/no)'))

        if all == 'no':

            while True:
                
                ids = str(input('Please enter the ids with this format: 1,2,3... (separeted by , and without spaces)'))
                ids_list = ids.split(',')

                if set(ids_list).issubset(self._get_ppal_vars):
                    vars.extend(ids_list)
                    break
                else:
                    print('At least one of the ids is not correct, try again')
        
            return vars

        else:
            return list(self._get_ppal_vars)
    
    def __display_bcra_variables(self):
        '''
        Prints variables available in BCRA to users.
        '''

        LOGGER.info('Print BCRA variables')
        for k, v in self._get_ppal_vars.items():
            print(f'ID: {k}, {v}')

    def __normalize_df(self, df: pd.DataFrame, var_id: str) -> pd.DataFrame:
        
        curated_df = df[['fecha', 'valor']]
        curated_df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d').dt.date

        var_name = unidecode.unidecode(self._get_ppal_vars[var_id])
        curated_df['variable'] = var_name   

        return curated_df

    def __save_vars(self, vars):
        '''
        Displays data for each variable selected by the user.
        '''

        LOGGER.info(f'Period of analysis from {self.start_date} to {self.end_date}')
        dfs = []

        for var in vars:

            LOGGER.info(f'Getting data from var_id: {var}')
            
            r = requests.get(
                self.__endpoint_var.format(
                    BASE_URL=self.__base_url,
                    ID=var,
                    START_DATE=self.start_date,
                    END_DATE=self.end_date
                ), 
                verify=False
            )

            r_json = r.json()

            if r.status_code == 200:
                
                results = r_json['results']
  
                df = pd.DataFrame(results)
                curated_df = self.__normalize_df(df, var)

                dfs.append(curated_df)
                
            else: 
                error_messages = r_json['errorMessages']
                
                if 'No existen registros para los parámetros enviados.' in error_messages:
                    LOGGER.info('There is no new data for this variable')
                    continue
            
                else:
                    raise Exception("Error during API call")
        
        
        isExist = os.path.exists(self.__output_dir)

        if not isExist:
            os.makedirs(self.__output_dir)
        
        temp_df = pd.concat(dfs, axis=0, ignore_index=True)
        
        engine = create_engine(f'sqlite:///{self.__output_dir}/{self.__db_name}.db')
        conn = engine.connect()
        
        temp_df.to_sql('bcra_temp', engine, if_exists='replace', index=False)

        LOGGER.info('Getting min date for the new import')
        min_date = pd.read_sql(queries.MIN_DATE.format(table='bcra_temp'), engine)['min_date'].values[0]
        
        LOGGER.info('Deleting duplicated rows')
        delete_query = queries.DELETE_ROWS.format(
            table='bcra_final',
            where_condition=f'fecha >= \'{min_date}\''
        )
        conn.execute(text(delete_query))
        conn.commit()

        LOGGER.info('Inserting new rows')
        insert_query = queries.INSERT_ROWS.format(
            target_table='bcra_final',
            source_table='bcra_temp'
        )
        conn.execute(text(insert_query))
        conn.commit()

        conn.close()

    def run(self):
        
        self.__display_bcra_variables()
        
        if not self.vars:
            variables = self.__ask_for_vars()
        
        else:
            variables = self.vars

        self.__save_vars(variables)
            