import datetime
import numpy as np
import pandas as pd
import plotly
import plotly.express as px

TODAY = datetime.date.today()

class Analyzer:

    def __init__(self):
        self.__dataframe = pd.read_csv('outputs/bcra_dataset.csv')

    def __normalize(self):
        
        self.__dataframe['fecha'] = pd.to_datetime(self.__dataframe['fecha'], format='%Y-%m-%d')
        self.__dataframe = self.__dataframe.pivot(index='fecha', columns='variable', values='valor')
        self.__dataframe['lag_1y'] = self.__dataframe['Unidad de Valor Adquisitivo (UVA) (en pesos -con dos decimales-, base 31.3.2016=14.05)'].shift(freq='365D')
        self.__dataframe['UVA vs last year'] = np.round(((self.__dataframe['Unidad de Valor Adquisitivo (UVA) (en pesos -con dos decimales-, base 31.3.2016=14.05)'] / self.__dataframe['lag_1y']) - 1) * 100, 2)
        self.__dataframe.drop(
            columns = [
            'Unidad de Valor Adquisitivo (UVA) (en pesos -con dos decimales-, base 31.3.2016=14.05)',
            'lag_1y'
            ], 
            axis=0, 
            inplace=True
        )

        self.__dataframe = self.__dataframe[TODAY.replace(year=TODAY.year-1).strftime('%Y-%m-%d'):].reset_index()
        
        return self.__dataframe
    
    def visualize(self):

        fig = px.line(self.__normalize(), 
                    x='fecha', 
                    y=[
                        'BADLAR en pesos de bancos privados (en % e.a.)',
                        'Tasa de Politica Monetaria (en % e.a.)',
                        'UVA vs last year'
                    ], 
                    title='BCRA Analysis'
            )

        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        plotly.offline.plot(fig, filename='outputs/bcra_analysis')
