import pandas as pd
import plotly
import plotly.express as px


class Analyzer:

    def __init__(self):
        self.__dataframe = pd.read_csv('outputs/bcra_dataset.csv')

    def __normalize(self):
        
        self.__dataframe['fecha'] = pd.to_datetime(self.__dataframe['fecha'], format='%Y-%m-%d')

        return self.__dataframe

    def visualize(self):
    
        fig = px.line(self.__normalize(), 
                    x='fecha', 
                    y='valor', 
                    color='variable',
                    title='BCRA Analysis'
            )

        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        plotly.offline.plot(fig, filename='outputs/bcra_analysis')
