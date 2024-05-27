import logging

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

import src.queries as queries

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Analyzer:

    def __init__(self):
        self.engine = create_engine('sqlite:///outputs/bcra.db')

    def __metrics(self):

        LOGGER.info('Define key measures')
        metrics_dict = {
            'Inflacion mensual (variacion en %)': 'Monthly Inflation Rate',
            'Inflacion interanual (variacion en % i.a.)': 'YOY Inflation Rate',
            'Tipo de Cambio Minorista ($ por USD) Comunicacion B 9791 - Promedio vendedor': 'Exchange Rate',
            'BADLAR en pesos de bancos privados (en % e.a.)': 'BADLAR Rate',
            'Indice para Contratos de Locacion (ICL-Ley 27.551, con dos decimales, base 30.6.20=1)': 'ICL Index'
        }

        metrics_cols = st.columns(len(metrics_dict))

        for col, metric in zip(metrics_cols, metrics_dict):

            df = pd.read_sql(
                queries.LAST_AVAILABLE_VALUE.format(
                    variable=metric
                    ),
                    self.engine
                )

            col.metric(label=metrics_dict[metric] + ' (' + str(df['date'].values[0]) + ')', value=str(df['last_value'].values[0]) + str(' %' if '%' in metric else ''))

    def __full_df(self):

        LOGGER.info('Tile with the complete list of variables')
        full_df = pd.read_sql(queries.FULL_DF, self.engine)
        full_df.rename(
            columns={
                'fecha': 'date',
                'valor': 'value'
            }, 
            inplace=True
        )

        data_set = st.multiselect(
            label="Pick varibles to analyze", 
            options=full_df['variable'].unique(),
            default='Inflacion mensual (variacion en %)'
        )

        fig = px.line(
            full_df[full_df['variable'].isin(data_set)], 
            x='date', 
            y='value', 
            color='variable',
            title='BCRA Analysis'
        )

        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        st.plotly_chart(fig, use_container_width=True)

    def visualize(self):

        st.set_page_config(
            page_title='BCRA Main Variables Dashboard',
            layout='wide'
        )

        st.markdown("<h1 style='color: #1b89de;'>BCRA Dashboard</h1>", unsafe_allow_html=True)
        
        self.__metrics()

        self.__full_df()
