import logging

import pandas as pd
import plotly.express as px
import statsmodels as sm
import streamlit as st
from sqlalchemy import create_engine

import src.queries as queries

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Visualizer:

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
        df = pd.read_sql(queries.FULL_DF, self.engine)
        df.rename(
            columns={
                'fecha': 'date',
                'valor': 'value'
            }, 
            inplace=True
        )
        df['date'] = pd.to_datetime(df['date'])

        data_set = st.multiselect(
            label="Pick varibles to analyze", 
            options=df['variable'].unique(),
            default='Inflacion mensual (variacion en %)'
        )

        # Date filter
        st.sidebar.subheader('Date Filter')
        start_date = st.sidebar.date_input('Start date', df['date'].min())
        end_date = st.sidebar.date_input('End date', df['date'].max())

        # Filter data based on date range
        if start_date > end_date:
            st.error("Error: End date must fall after start date.")
        else:
            filtered_data = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]


        st.sidebar.subheader('Plot Settings')
        plot_type = st.sidebar.selectbox('Select plot type', ['Line Plot', 'Bar Chart', 'Scatter Plot'])
        add_trendline = st.sidebar.checkbox('Add Trendline')
        
        st.write("## Plot")
        if plot_type == 'Line Plot':
            fig = px.scatter(
                filtered_data[filtered_data['variable'].isin(data_set)], 
                x='date', 
                y='value', 
                color= 'variable',
                title='BCRA Analysis',
                trendline="ols" if add_trendline else None
            )
            fig.update_traces(mode='lines+markers')
        elif plot_type == 'Bar Chart':
            fig = px.bar(
                filtered_data[filtered_data['variable'].isin(data_set)], 
                x='date', 
                y='value'
            )
        elif plot_type == 'Scatter Plot':
            fig = px.scatter(
                filtered_data[filtered_data['variable'].isin(data_set)], 
                x='date', 
                y='value',
                trendline="ols" if add_trendline else None
            )

        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )

        st.plotly_chart(fig, use_container_width=True)

    def run(self):

        st.set_page_config(
            page_title='BCRA Panel',
            layout='wide'
        )

        st.markdown("<h1>BCRA Metrics</h1>", unsafe_allow_html=True)
        
        self.__metrics()

        self.__full_df()
