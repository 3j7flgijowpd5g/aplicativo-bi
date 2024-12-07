import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
import base64
import io

# Preparar la aplicación Dash
app = dash.Dash(__name__)

# Layout del Dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análisis de Pacientes", style={'text-align': 'center'}),

    # Sección para cargar archivos
    html.Div([
        html.H3("Cargar Archivo CSV"),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Arrastra o selecciona un archivo CSV']),
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
        html.Div(id='upload-status'),
    ]),

    # Filtros (deshabilitados inicialmente)
    html.Div([
        html.Label("Filtrar por Centro Médico:"),
        dcc.Dropdown(
            id='centro-medico-dropdown',
            options=[],
            value=None,
            placeholder="Selecciona un Centro Médico",
            disabled=True
        ),
        html.Label("Rango de Fechas:"),
        dcc.DatePickerRange(
            id='date-picker',
            start_date=None,
            end_date=None,
            disabled=True
        ),
    ], style={'margin-bottom': '20px'}),

    # Sección de métricas clave
    html.Div([
        html.Div([
            html.H4("Total de Pacientes"),
            html.P(id='total-pacientes', style={'font-size': '24px'})
        ], style={'display': 'inline-block', 'width': '30%'}),
        html.Div([
            html.H4("Edad Promedio"),
            html.P(id='edad-promedio', style={'font-size': '24px'})
        ], style={'display': 'inline-block', 'width': '30%'}),
        html.Div([
            html.H4("Distribución por Género"),
            dcc.Graph(id='grafico-genero')
        ], style={'display': 'inline-block', 'width': '40%'}),
    ]),

    # Gráficos principales
    html.Div([
        dcc.Graph(id='grafico-historial-medico'),
        dcc.Graph(id='grafico-imc'),
        dcc.Graph(id='grafico-costo'),
    ]),

    # Tabla de datos
    html.Div([
        html.H3("Detalle de Pacientes"),
        dash_table.DataTable(
            id='tabla-detalle',
            columns=[],
            data=[],
            page_size=10,
            style_table={'overflowX': 'auto'}
        )
    ]),

    # Almacenamiento interno para datos cargados
    dcc.Store(id='data-store')
])

# Callback para procesar el archivo CSV cargado
@app.callback(
    [Output('upload-status', 'children'),
     Output('data-store', 'data'),
     Output('centro-medico-dropdown', 'options'),
     Output('centro-medico-dropdown', 'disabled'),
     Output('date-picker', 'start_date'),
     Output('date-picker', 'end_date'),
     Output('date-picker', 'disabled'),
     Output('tabla-detalle', 'columns')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def cargar_csv(content, filename):
    if content is None:
        return "No se ha cargado ningún archivo.", None, [], True, None, None, True, []

    # Leer y decodificar el archivo
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Leer CSV
        df_cargado = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Validación de columnas requeridas
        required_columns = ['Centro_Medico', 'Fecha_Registro', 'Genero', 'Historial_Medico', 'IMC', 'Costo_Tratamiento', 'Costo_Citas_Anuales']
        if not all(col in df_cargado.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df_cargado.columns]
            raise ValueError(f"El archivo no contiene las columnas requeridas: {', '.join(missing)}")
        
        # Convertir 'Fecha_Registro' a formato datetime
        df_cargado['Fecha_Registro'] = pd.to_datetime(df_cargado['Fecha_Registro'], errors='coerce')
        if df_cargado['Fecha_Registro'].isnull().any():
            raise ValueError("El archivo contiene valores inválidos en 'Fecha_Registro'.")
        
        # Configurar filtros y columnas de tabla
        opciones_centro = [{'label': c, 'value': c} for c in df_cargado['Centro_Medico'].unique()]
        columnas_tabla = [{"name": i, "id": i} for i in df_cargado.columns]

        return (
            f"Archivo cargado: {filename}",
            df_cargado.to_dict('records'),
            opciones_centro,
            False,
            df_cargado['Fecha_Registro'].min(),
            df_cargado['Fecha_Registro'].max(),
            False,
            columnas_tabla
        )
    except Exception as e:
        return f"Error al cargar el archivo: {str(e)}", None, [], True, None, None, True, []

# Callback para actualizar el dashboard
@app.callback(
    [Output('total-pacientes', 'children'),
     Output('edad-promedio', 'children'),
     Output('grafico-genero', 'figure'),
     Output('grafico-historial-medico', 'figure'),
     Output('grafico-imc', 'figure'),
     Output('grafico-costo', 'figure'),
     Output('tabla-detalle', 'data')],
    [Input('centro-medico-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')],
    [State('data-store', 'data')]
)

def actualizar_dashboard(centro_medico, start_date, end_date, data):
    # Placeholder DataFrame vacío para gráficos
    placeholder_df = pd.DataFrame({'x': [], 'y': []})

    if data is None or len(data) == 0:
        # Gráficos placeholders
        fig_placeholder = px.scatter(placeholder_df, x='x', y='y', title="Esperando datos...")
        return "-", "-", fig_placeholder, fig_placeholder, fig_placeholder, fig_placeholder, []

    # Convertir datos almacenados a DataFrame
    dff = pd.DataFrame(data)
    dff = dff[(dff['Fecha_Registro'] >= start_date) & (dff['Fecha_Registro'] <= end_date)]
    if centro_medico:
        dff = dff[dff['Centro_Medico'] == centro_medico]

    # Total de pacientes y edad promedio
    total_pacientes = len(dff)
    edad_promedio = round(dff['Edad'].mean(), 1)

    # Gráficos
    grafico_genero = px.pie(dff, names='Genero', title="Distribución por Género")
    grafico_historial = px.bar(dff, x='Historial_Medico', title="Historial Médico")
    grafico_imc = px.histogram(dff, x='IMC', title="Distribución del IMC")
    grafico_costo = px.scatter(dff, x='Costo_Tratamiento', y='Costo_Citas_Anuales', title="Costo de Tratamiento vs Citas")

    return total_pacientes, edad_promedio, grafico_genero, grafico_historial, grafico_imc, grafico_costo, dff.to_dict('records')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
