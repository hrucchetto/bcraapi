import pandas as pd
import plotly
import plotly.express as px

df = pd.read_csv('outputs/2024-05-13_bcra_dataset.csv')
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

fig = px.line(df, 
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

plotly.offline.plot(fig, filename='analysis/bcra_analysis_test.html')
