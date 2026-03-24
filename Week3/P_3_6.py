import pandas as pd
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State

data = pd.read_csv("./assets/clinical_analytics.csv")
print(data.shape)
data.head()

# Convertimos las columnas de fechas a tipo fecha
data['Appt Start Time'] = pd.to_datetime(data['Appt Start Time'], format='%Y-%m-%d %I:%M:%S %p')
data['Check-In Time'] = pd.to_datetime(data['Check-In Time'], format='%Y-%m-%d %I:%M:%S %p')

data['Encounter Status'] = data['Encounter Status'].fillna('Information not available')
data['Diagnosis Primary'] = data['Diagnosis Primary'].fillna('Information not available')
data['Admit Source'] = data['Admit Source'].fillna('Information not available')




app = dash.Dash(external_stylesheets=[dbc.themes.MORPH])  

app.layout =dbc.Container([
    #NAVBAR COMO TITULO
    dbc.NavbarSimple(
        children=[],
        brand=dbc.Row(
            [
                dbc.Col(html.Img(src="/assets/logoPic.png", height="40px")),
                dbc.Col("Ejercicio Práctico - GRUPO 6 - Clinical Analytics",
                        style={"color": "white", "fontWeight": "bold", "paddingLeft": "20px"})
            ],
            align="center",
            className="g-0",
        ),
        color="primary",

    ),

    
    dash.html.Br(),

    ################################################################# FILA FILTROS
    html.H6("SELECCIONE LOS FILTROS:", className="text-primary-emphasis",style={"fontWeight": "bold"}),
    dbc.Row([ 
        #CLINIC NAME
        dbc.Col([
            dash.html.Label("Seleccionar Clínica:"),
            dash.dcc.Dropdown(id="clinic-filter", options=data["Clinic Name"].unique(),value=data["Clinic Name"].unique().tolist(),
                             multi=True, className="text-primary")    
        ],md=3),

        #DEPARTMENT
        dbc.Col([
            dash.html.Label("Seleccionar Departamento:"),
            dash.dcc.Dropdown(id="department-filter", options=data["Department"].unique(),value=data["Department"].unique().tolist(),
                             multi=True, className="text-primary")
            
        ],md=3),
        
        #CARE SCORE
       dbc.Col([
            dash.html.Label("Calificación de Atención:"),
            dash.dcc.Dropdown(id="careScore-filter", options=data["Care Score"].unique(),value=data["Care Score"].unique().tolist(),
                               multi=True, className="text-primary")  
            
        ],md=3),

        #Check-In Time
        dbc.Col([
            dash.html.Label("Periodo Check-In:"),
            dcc.DatePickerRange(
               id='dateRange-filter',
                min_date_allowed=data["Check-In Time"].min(),
                max_date_allowed=data["Check-In Time"].max(),
                initial_visible_month=data["Check-In Time"].min(),
                end_date=data["Check-In Time"].min(),
                display_format='YYYY-MM-DD',
            )
        ],md=3)
        
    ],justify="center"),
    dash.html.Br(),
    
    ################################################################# FILA CONTADORES PRINCIPALES
    html.H6("CONTADORES PRINCIPALES", className="text-primary-emphasis",style={"fontWeight": "bold"}),
    dbc.Row([
        #////////////////////CARD NUMERO DE PACIENTES
        dbc.Col(dbc.Card([
           dbc.Row([
               dbc.Col(dbc.CardImg(src="/assets/pacientePic.png", top=True,style={"width": "64px", "height": "64px"}),className="col-md-3"),
               dbc.Col(
                   dbc.CardBody([
                       html.H6("Pacientes atendidos", className="text-primary-emphasis",style={"fontWeight": "bold"}),
                       html.H4(id='avg-paciente', className="text-success"),            
                   ])
               )
           ],className=" g-0 d-flex align-items-center")
        ]),md=3), 
        #////////////////////CARD CALIFICACION PROMEDIO
        dbc.Col(dbc.Card([
           dbc.Row([
               dbc.Col(dbc.CardImg(src="/assets/carePic.png", top=True,style={"width": "64px", "height": "64px"}),className="col-md-3"),
               dbc.Col(
                   dbc.CardBody([
                       html.H6("Calificación Promedio", className="text-primary-emphasis",style={"fontWeight": "bold"}),
                       html.H4(id='avg-care', className="text-success"),            
                   ])
               )
           ],className=" g-0 d-flex align-items-center")
        ]),md=3), 
        #////////////////////CARD TIEMPO DE ESPERA PROMEDIO
        dbc.Col(dbc.Card([
           dbc.Row([
               dbc.Col(dbc.CardImg(src="/assets/TimePic.png", top=True,style={"width": "64px", "height": "64px"}),className="col-md-3"),
               dbc.Col(
                   dbc.CardBody([
                       html.H6("Tiempo de Espera Promedio", className="text-primary-emphasis",style={"fontWeight": "bold"}),
                       html.H4(id='avg-time', className="text-success"),            
                   ])
               )
           ],className="g-0 d-flex align-items-center")
        ]),md=4), 
        

    ],justify="center"),
    dash.html.Br(),

     ################################################################# FILA  GRAFICOS
    dbc.Row([
        dbc.Col(dcc.Graph(id="scatter-TimeCare"),md=6),
        dbc.Col(dcc.Graph(id="bar-WTime-APPStart"),md=6),
        
    ],justify="center"),
    dash.html.Br(),
    ################################################################# FILA  GRAFICOS
    dbc.Row([

        dbc.Col(dcc.Graph(id="bar-DiagnosisPrimary"),md=6),
        dbc.Col(dcc.Graph(id="bar-EncounterStatus"),md=6),
        
    ],justify="center"),
    dash.html.Br(),
    ################################################################# FILA  GRAFICOS
    dbc.Row([

        dbc.Col(dcc.Graph(id="heat-Clinic-Department"),md=12),
        
    ],justify="center"),
    dash.html.Br(),
        ################################################################# FILA  GRAFICOS
    dbc.Row([

        dbc.Col(dcc.Graph(id="heat-admType-Diagnosis"),md=12),
        
    ],justify="center"),
    dash.html.Br(),
     ################################################################# FILA INFO EXTRA
    #dbc.Row([
    #    dbc.Col([dbc.Alert("Click en un punto para visualizar más información", color="info"),
    #            dash.html.Div(id='point-info')],md=6),
    #])
    
])

#CALLBACK PARA FILTROS GENERALES
@app.callback(
    [
        Output("scatter-TimeCare", "figure"),
        Output("bar-WTime-APPStart", "figure"),
        Output("bar-DiagnosisPrimary", "figure"),
        Output("bar-EncounterStatus", "figure"),
        Output("heat-Clinic-Department", "figure"),
        Output("heat-admType-Diagnosis", "figure"),
  
        
        Output("avg-care", "children"),
        Output("avg-time", "children"),
        Output("avg-paciente", "children"),
    ],
    [
        Input("clinic-filter","value"),
        Input("department-filter","value"),
        Input("careScore-filter","value"),
        #Input("dateRange-filter","value"),
        Input('dateRange-filter', 'start_date'),
        Input('dateRange-filter', 'end_date')
    ]
)
def update_dash(clinic,department,careScore,startdate, enddate):        
    #if bill_range:  controlar si no tiene valores o poner valores como arriba
    if startdate is None or enddate is None:
        raise dash.exceptions.PreventUpdate # No actualiza nada hasta que haya fechas validas

    dataf=data[
        (data["Clinic Name"].isin(clinic))&
        (data["Department"].isin(department))&
        (data["Care Score"].isin(careScore))&
        #(data["Check-In Time"].between(dateRange[0],dateRange[1]))
        (data["Check-In Time"].between(startdate,enddate))
        #(data['Check-In Time'] >= startdate) & (data['Check-In Time'] <= enddate)
    ]

    #***************************************************** SCATTER x="Wait Time Min", y="Care Score"
    scatterTimeCare_var = px.scatter(dataf,x="Care Score", y="Wait Time Min",size="Care Score",
                                     title='Calificaciones por tiempo de espera')
    scatterTimeCare_var.update_layout(xaxis_title='Calificación', yaxis_title='Tiempo de espera',
                  showlegend=False, hovermode='closest')

    #***************************************************** Appointments por dia de semana
    dataf['DayOfWeek'] = dataf['Appt Start Time'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Obtenemos las frecuencias por día de la semana
    weekly_counts = dataf['DayOfWeek'].value_counts().reset_index()
    weekly_counts.columns = ['DayOfWeek', 'AppoinmentCount']
    
    # Gráfica BAR
    barWTimeAPPStart_var = px.bar(weekly_counts, x='DayOfWeek', y='AppoinmentCount',
                 title='Número de citas por día de la semana',
                 color='DayOfWeek')
    
    barWTimeAPPStart_var.update_layout(xaxis_title='Día de la semana', yaxis_title='Frecuencia de citas',
                  showlegend=False, hovermode='closest',xaxis=dict(categoryorder='array', categoryarray=day_order))
   
    #***************************************************** Histograma TOP 10 de Diagnostico
    top_10_diagnostics = dataf['Diagnosis Primary'].value_counts().head(10).index.tolist()
    # Filtrar el DataFrame para incluir solo estas 10 categorías principales de cada columna
    data_diag_filtered = dataf[dataf['Diagnosis Primary'].isin(top_10_diagnostics)]
    
    barDiagnosisPrimary_var = px.histogram(data_diag_filtered,
                                           x='Diagnosis Primary', 
                                          title='Dolencias tratadas(TOP10)')

    barDiagnosisPrimary_var.update_layout(xaxis_title='Dolencias', yaxis_title='Frecuencia',
                  showlegend=False, hovermode='closest',xaxis={'categoryorder': 'total descending'})

     #*****************************************************  Histograma de Estado 

    barEncounterStatus_var = px.histogram(dataf, x='Encounter Status',
                                         title='Estado de ALTA de pacientes')

    barEncounterStatus_var.update_layout(xaxis_title='Estado de alta', yaxis_title='Frecuencia',
                  showlegend=False, hovermode='closest',xaxis={'categoryorder': 'total descending'})
    
    #*****************************************************  HEATMAP CLINICA VS DEPARTMAENTO 
    # Crear matriz cruzada
    matriz = pd.crosstab(dataf["Clinic Name"], dataf["Department"])
    
    # Graficar heatmap
    heat_Clinic_Department_var = px.imshow(
        matriz,
        text_auto=True,  # ← muestra los números dentro de cada celda
        labels=dict(
            x="Department",
            y="Clinic Name",
            color="Cantidad de Atenciones"   # ← título de la leyenda
        ),
        title="Heatmap: Clínica vs Especialidad"
    )
    heat_Clinic_Department_var.update_layout(xaxis_title='Especialidad solicitada', yaxis_title='Clínica',
                  hovermode='closest')
    
    #*****************************************************  HEATMAP TIPO DE CONSULTA VS DIAGNOSTICO
    # Crear matriz cruzada
    
    top10_diag = dataf["Diagnosis Primary"].value_counts().nlargest(10).index
    
    matriz2 = pd.crosstab(
        dataf["Admit Type"],
        dataf[dataf["Diagnosis Primary"].isin(top10_diag)]["Diagnosis Primary"]
    )

   
    # Graficar heatmap
    heat_admType_Diagnosis_var = px.imshow(
        matriz2,
        text_auto=True,  # ← muestra los números dentro de cada celda
        labels=dict(
            x="Diagnosis Primary",
            y="Admit Type",
            color="Cantidad de Atenciones"   # ← título de la leyenda
        ),
        title="Heatmap: Dolencias (TOP10) vs tipo de consulta"
    )
    heat_admType_Diagnosis_var.update_layout(xaxis_title='Dolencia', yaxis_title='Tipo de consulta',
                  hovermode='closest')
    
    #*****************************************************  CONTADORES
    avg_care=f"{dataf['Care Score'].mean():.2f}" if not dataf.empty else "No hay valores"
    avg_time=f"{dataf['Wait Time Min'].mean():.2f}" if not dataf.empty else "No hay valores"
    avg_paciente=(dataf['Encounter Status'] != 'Cancelled').sum() if not dataf.empty else "No hay valores"


    return scatterTimeCare_var,barWTimeAPPStart_var,barDiagnosisPrimary_var,barEncounterStatus_var,heat_Clinic_Department_var,heat_admType_Diagnosis_var,avg_care,avg_time, avg_paciente



#@app.callback(
#    Output ("point-info", "children"),
#    Input ("scatter-plot", "clickData")
#)

#def update_by_click(data):
#    if data:
#        point=data["points"][0]
#        return dash.html.Div(f"data: {point['x']} y {point['y']}")

app.run()