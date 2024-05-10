import logging
import os
import requests
import unidecode
import urllib3
from datetime import date, timedelta
from functools import cached_property

import pandas as pd

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

START_DATE = (date.today() + timedelta(days=-60)).strftime('%Y-%m-%d') 
END_DATE = date.today().strftime('%Y-%m-%d')
pd.options.mode.chained_assignment = None
urllib3.disable_warnings()

class BCRAVars:

    def __init__(self, start_date: date = START_DATE, end_date: date = END_DATE):
        self._base_url = 'https://api.bcra.gob.ar'
        self._endpoint_ppal_vars = '{BASE_URL}/estadisticas/v1/PrincipalesVariables'
        self._endpoint_var = '{BASE_URL}/estadisticas/v1/DatosVariable/{ID}/{START_DATE}/{END_DATE}'
        self.end_date = end_date if end_date else END_DATE
        self.start_date = start_date if start_date else START_DATE

    @cached_property    
    def _get_ppal_vars(self) -> dict: 
        '''
        Returns a list with all the variables available in BCRA API.
        '''

        LOGGER.info('Get variables from BCRA')
        r = requests.get(
            self._endpoint_ppal_vars.format(
                BASE_URL=self._base_url
            ), 
            verify=False
        )

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
    
    def _ask_for_vars(self) -> list:
        
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
    
    def _display_bcra_variables(self):
        '''
        Prints variables available in BCRA to users.
        '''
        LOGGER.info('Print BCRA variables')
        for k, v in self._get_ppal_vars.items():
            print(f'ID: {k}, {v}')

    def _save_vars(self, vars):
        '''
        Displays data for each variable selected by the user.
        '''

        final_df = pd.DataFrame()
        LOGGER.info(f'Period of analysis from {self.start_date} to {self.end_date}')

        for i, var in enumerate(vars):

            LOGGER.info(f'Getting data from var_id: {var}')
            
            r = requests.get(
                self._endpoint_var.format(
                    BASE_URL=self._base_url,
                    ID=var,
                    START_DATE=self.start_date,
                    END_DATE=self.end_date
                ), 
                verify=False
            )

            if r.status_code == 200:
                
                results = r.json()['results']
  
                df = pd.DataFrame(results)
                curated_df = df[['fecha', 'valor']]
                curated_df['valor'] = curated_df['valor'].str.replace(',','.').str.replace('.','').astype('float64') 
                new_name = unidecode.unidecode(self._get_ppal_vars[var])  

                curated_df.rename(columns={'valor': f'{new_name}'}, inplace=True)

                if i == 0:
                    final_df = curated_df
                
                else:
                    final_df = final_df.merge(curated_df, on='fecha', how='outer')

                
            else:
                raise Exception("Error during API call")
        
        folder = f'outputs'
        isExist = os.path.exists(folder)

        if not isExist:
            os.makedirs(folder)
        
        final_df.to_csv(f'{folder}/{self.end_date}_bcra_dataset.csv', index=False)

    def run(self):
        
        self._display_bcra_variables()
        variables = self._ask_for_vars()
        self._save_vars(variables)
            