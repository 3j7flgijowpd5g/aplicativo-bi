# Importar librerías necesarias
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import io
import base64

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout del Dashboard
app.layout = html.Div([
    html.H1("Dashboard de Segmentación de Pacientes", style={'text-align': 'center'}),

    html.Div([
        html.H3("Cargar archivo CSV"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastra o selecciona un archivo CSV'
            ]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px auto'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload')
    ]),

    html.Div([
        html.Label("Selecciona las variables para visualizar:"),
        dcc.Dropdown(
            id='xaxis-dropdown',
            options=[],
            value=None,
            placeholder="Selecciona una variable para el eje X"
        ),
        dcc.Dropdown(
            id='yaxis-dropdown',
            options=[],
            value=None,
            placeholder="Selecciona una variable para el eje Y"
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='scatter-plot'),

    html.Hr(),

    html.Div([
        html.H3("Promedios por Cluster"),
        dcc.Graph(id='bar-chart')
    ]),

    # Almacenamiento interno para los datos cargados
    dcc.Store(id='data-store')
])

# Callback para procesar el archivo CSV cargado
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('xaxis-dropdown', 'options'),
     Output('yaxis-dropdown', 'options'),
     Output('data-store', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(content, filename):
    if content is None:
        return "No se ha cargado ningún archivo.", [], [], None

    # Leer el archivo CSV
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Opciones para dropdowns
    options = [{'label': col, 'value': col} for col in df.columns]

    # Actualizar la salida
    return f"Archivo cargado: {filename}", options, options, df.to_dict('records')

# Callback para actualizar el gráfico de dispersión
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('xaxis-dropdown', 'value'),
     Input('yaxis-dropdown', 'value')],
    [State('data-store', 'data')]
)
def update_scatter(xaxis, yaxis, data):
    if not xaxis or not yaxis or not data:
        return px.scatter(title="Esperando datos y selección de variables...")

    df = pd.DataFrame(data)
    fig = px.scatter(df, x=xaxis, y=yaxis, title=f"Gráfico: {xaxis} vs {yaxis}")
    return fig

# Callback para actualizar el gráfico de barras
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('data-store', 'data')]
)
def update_bar_chart(data):
    if not data:
        return px.bar(title="Esperando datos para mostrar...")

    df = pd.DataFrame(data)

    # Ejemplo: promedio por alguna columna de clusters si existe
    if 'cluster' in df.columns:
        df_grouped = df.groupby('cluster').mean().reset_index()
        fig = px.bar(df_grouped, x='cluster', y=df_grouped.columns[1:], barmode='group',
                     title="Promedios por Cluster")
        return fig

    return px.bar(title="No se encontraron clusters para agrupar.")

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
