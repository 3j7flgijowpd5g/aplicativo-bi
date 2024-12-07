import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import io

# Preparar la aplicación Dash con tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout del Dashboard
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Dashboard de Análisis de Pacientes",
                className="text-center text-primary mb-4"), width=12)
    ),

    # Sección para cargar archivos
    dbc.Row(
        dbc.Col([
            html.H3("Cargar Archivo CSV", className="text-secondary"),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Arrastra o selecciona un archivo CSV']),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px 0'
                },
                multiple=False
            ),
            html.Div(id='upload-status', className="text-info")
        ], width=12)
    ),

    # KPIs
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total de Pacientes",
                            className="card-title text-center"),
                    html.H2(id='total-pacientes',
                            className="card-text text-center text-primary")
                ])
            ], className="shadow-sm mb-4")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Promedio de Edad",
                            className="card-title text-center"),
                    html.H2(id='edad-promedio',
                            className="card-text text-center text-primary")
                ])
            ], className="shadow-sm mb-4")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Centros Médicos",
                            className="card-title text-center"),
                    html.H2(id='total-centros',
                            className="card-text text-center text-primary")
                ])
            ], className="shadow-sm mb-4")
        ], width=4)
    ]),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-genero'), width=6),
        dbc.Col(dcc.Graph(id='grafico-historial-medico'), width=6)
    ]),

    # Tabla de datos
    dbc.Row([
        dbc.Col([
            html.H3("Detalle de Pacientes", className="text-secondary mt-4"),
            dash_table.DataTable(
                id='tabla-detalle',
                columns=[],
                data=[],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center'}
            )
        ], width=12)
    ]),

    # Almacenamiento interno
    dcc.Store(id='data-store')
], fluid=True)

# Callback para procesar el archivo CSV cargado


@app.callback(
    [Output('upload-status', 'children'),
     Output('data-store', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def cargar_csv(content, filename):
    if content is None:
        return "No se ha cargado ningún archivo.", None

    # Leer y decodificar el archivo
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Leer CSV
        df_cargado = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return f"Archivo '{filename}' cargado con éxito.", df_cargado.to_dict('records')
    except Exception as e:
        return f"Error al cargar el archivo: {str(e)}", None

# Callback para actualizar métricas y gráficos


@app.callback(
    [Output('total-pacientes', 'children'),
     Output('edad-promedio', 'children'),
     Output('total-centros', 'children'),
     Output('grafico-genero', 'figure'),
     Output('grafico-historial-medico', 'figure')],
    [Input('data-store', 'data')]
)
def actualizar_resumen(data):
    if data is None or len(data) == 0:
        return "-", "-", "-", px.pie(values=[], names=[], title="Esperando datos..."), px.bar(x=[], y=[], title="Esperando datos...")

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Calcular métricas
    total_pacientes = len(df)
    edad_promedio = round(df['Edad'].mean(), 1)
    total_centros = df['Centro_Medico'].nunique()

    # Gráficos
    grafico_genero = px.pie(
        df, names='Genero', title="Distribución por Género")
    grafico_historial = px.bar(
        df, x='Historial_Medico', title="Frecuencia por Diagnóstico")

    return total_pacientes, edad_promedio, total_centros, grafico_genero, grafico_historial


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
