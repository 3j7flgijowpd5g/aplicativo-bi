# Importar librerías necesarias
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Crear un conjunto de datos simulado de pacientes
np.random.seed(42)
data = {
    "Edad": np.random.randint(18, 80, 200),
    "Visitas_Medicas": np.random.randint(1, 10, 200),
    "Gasto_Anual": np.random.randint(500, 5000, 200),
    "Indice_Salud": np.random.uniform(0.5, 1.0, 200),
}
df = pd.DataFrame(data)

# Preprocesar los datos: estandarización
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Aplicar el algoritmo K-Means
kmeans = KMeans(n_clusters=4, random_state=42)
df["Cluster"] = kmeans.fit_predict(scaled_data)

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout del Dashboard
app.layout = html.Div([
    html.H1("Dashboard de Segmentación de Pacientes", style={'text-align': 'center'}),

    html.Div([
        html.Label("Selecciona las variables para visualizar:"),
        dcc.Dropdown(
            id='xaxis-dropdown',
            options=[
                {'label': 'Edad', 'value': 'Edad'},
                {'label': 'Visitas Médicas', 'value': 'Visitas_Medicas'},
                {'label': 'Gasto Anual', 'value': 'Gasto_Anual'},
                {'label': 'Índice de Salud', 'value': 'Indice_Salud'},
            ],
            value='Edad',
            placeholder="Selecciona una variable para el eje X"
        ),
        dcc.Dropdown(
            id='yaxis-dropdown',
            options=[
                {'label': 'Edad', 'value': 'Edad'},
                {'label': 'Visitas Médicas', 'value': 'Visitas_Medicas'},
                {'label': 'Gasto Anual', 'value': 'Gasto_Anual'},
                {'label': 'Índice de Salud', 'value': 'Indice_Salud'},
            ],
            value='Gasto_Anual',
            placeholder="Selecciona una variable para el eje Y"
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='scatter-plot'),

    html.Hr(),

    html.Div([
        html.H3("Promedios por Cluster"),
        dcc.Graph(
            id='bar-chart',
            figure=px.bar(
                df.groupby('Cluster').mean().reset_index(),
                x='Cluster',
                y=['Edad', 'Visitas_Medicas', 'Gasto_Anual', 'Indice_Salud'],
                barmode='group',
                title="Promedios por Cluster"
            )
        )
    ])
])

# Callbacks para la interactividad
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('xaxis-dropdown', 'value'),
     Input('yaxis-dropdown', 'value')]
)
def update_scatter(xaxis, yaxis):
    fig = px.scatter(
        df,
        x=xaxis,
        y=yaxis,
        color='Cluster',
        hover_data=['Edad', 'Visitas_Medicas', 'Gasto_Anual', 'Indice_Salud'],
        title=f"Segmentación de Pacientes: {xaxis} vs {yaxis}"
    )
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
