import logging

import pandas as pd
import plotly.express as px
import statsmodels as sm
import streamlit as st
from sqlalchemy import create_engine

import src.queries as queries

logging.basicConfig(level=logging.INFO)

class Visualizer:

    def __init__(self):
        self.__engine = create_engine('sqlite:///outputs/bcra.db')
        self.__full_df_raw = pd.read_sql(queries.FULL_DF, self.__engine)
        self.__full_df = self.__df_normalization()
        self.__bcra_variables = self.__full_df['variable'].unique()

    def __correlation_matrix(self):
        
        st.write('## Correlation Matrix')
        data_set = st.multiselect(
            label="Choose varibles to compare", 
            options=self.__bcra_variables,
            default=['Inflacion mensual (variacion en %)', 'Tasa de Politica Monetaria (en % e.a.)']
        )

        pivoted_df = self.__df_pivot()
        fig = px.scatter_matrix(
            pivoted_df,
            dimensions=data_set,
        )

        st.plotly_chart(fig, use_container_width=True)

    def __df_normalization(self):

        full_df = self.__full_df_raw.rename(
            columns={
                'fecha': 'date',
                'valor': 'value'
            }
        )
        full_df['date'] = pd.to_datetime(full_df['date'])

        return full_df

    def __df_pivot(self):

        pivoted_df = self.__full_df.pivot(
            index=['date'], 
            columns=['variable'], 
            values='value'
        ).reset_index()

        return pivoted_df

    def __full_plot(self):

        st.sidebar.subheader('Evolution Plot Settings')
        start_date = st.sidebar.date_input('Start date', self.__full_df['date'].min())
        end_date = st.sidebar.date_input('End date', self.__full_df['date'].max())
        plot_type = st.sidebar.selectbox('Select plot type', ['Line Plot', 'Bar Chart', 'Scatter Plot'])
        add_trendline = st.sidebar.toggle('Add Trendline')

        st.write("## Evolution Plot")
        data_set = st.multiselect(
            label="Choose varibles to display", 
            options=self.__bcra_variables,
            default='Inflacion mensual (variacion en %)'
        )

        # Filter data based on date range
        if start_date > end_date:
            st.error("Error: End date must fall after start date.")
        else:
            filtered_data = self.__full_df[(self.__full_df['date'] >= pd.Timestamp(start_date)) & (self.__full_df['date'] <= pd.Timestamp(end_date))]
        
        if plot_type == 'Line Plot':
            fig = px.scatter(
                filtered_data[filtered_data['variable'].isin(data_set)], 
                x='date', 
                y='value', 
                color= 'variable',
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

    def __metrics_plot(self):

        metrics_dict = {
            'Inflacion mensual (variacion en %)': 'Monthly Inflation Rate',
            'Inflacion interanual (variacion en % i.a.)': 'YOY Inflation Rate',
            'Tipo de Cambio Minorista ($ por USD) Comunicacion B 9791 - Promedio vendedor': 'Exchange Rate',
            'BADLAR en pesos de bancos privados (en % e.a.)': 'BADLAR Rate',
            'Indice para Contratos de Locacion (ICL-Ley 27.551, con dos decimales, base 30.6.20=1)': 'ICL Index'
        }

        st.write("## Main Metrics")
        metrics_cols = st.columns(len(metrics_dict))

        for col, metric in zip(metrics_cols, metrics_dict):

            df = pd.read_sql(
                queries.LAST_AVAILABLE_VALUE.format(
                    variable=metric
                    ),
                    self.__engine
                )

            col.metric(label=metrics_dict[metric] + ' (' + str(df['date'].values[0]) + ')', value=str(df['last_value'].values[0]) + str(' %' if '%' in metric else ''))

    def run(self):

        st.set_page_config(
            page_title='BCRA Dashboard',
            layout='wide'
        )

        st.markdown('<h1>BCRA Dashboard</h1>', unsafe_allow_html=True)
        st.write('#### Sections')
        main_metrics = st.checkbox('Main Metrics', value=True)
        evolution_plot = st.checkbox('Evolution Plot', value=True)
        corr_matrix = st.checkbox('Correlation Matrix', value=True)
        
        if main_metrics:
            self.__metrics_plot()

        if evolution_plot:
            self.__full_plot()

        if corr_matrix:
            self.__correlation_matrix()
