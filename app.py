import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import plotly.graph_objs as go
import os
from datetime import datetime
#---API Keys---#
mapbox_access_token = "pk.eyJ1IjoicHJpeWF0aGFyc2FuIiwiYSI6ImNqbGRyMGQ5YTBhcmkzcXF6YWZldnVvZXoifQ.sN7gyyHTIq1BSfHQRBZdHA"
#END OF: API Keys---#

# ---Load Tuna CSV File Folder---#
listOfFiles = []
# by default the "." value will make it the current working directory of the py file
defaultFolderDirectory = "."
currentChosenPredictionModel = "\\actual\\"
try:
    # change me
    for folderName, subFolders, fileNames in os.walk(defaultFolderDirectory+currentChosenPredictionModel):
        # print("The filenames in "+folderName+" are: "+str(fileNames))
        for files in fileNames:
            listOfFiles.append(files)
    print("\nSuccessfuly loaded List of Files:",
          len(listOfFiles), "files total")
except Exception as e:
    print("ERROR kykny filenya ga ada deh di Current working directorynya: ", os.getcwd())
    print(e)
    print("\nI stopped the app for you :)")
    raise SystemExit
# END OF: Load Tuna CSV File Folder---


#------------------------ COMPONENTS ----------------------------------#
# ---Navigation Bar---#
LOGO_IKAN = "https://png.pngtree.com/element_origin_min_pic/17/07/12/d37204e6a536b491a15d9b1f7baea95f.jpg"
logoTuna = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO_IKAN, height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Tuna Forecaster", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="#",  # TODO: CHANGEME
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/jamesadhitthana/TunaForecaster")),
                     dbc.DropdownMenu(
                         children=[
                             dbc.DropdownMenuItem(
                                 "Deananda Irwansyah", href="https://github.com/hikariyoru"),
                             dbc.DropdownMenuItem("Christopher Yefta", href="https://github.com/ChrisYef"),
                            #  dbc.DropdownMenuItem(divider=True),
                             dbc.DropdownMenuItem("James Adhitthana", href="https://github.com/jamesadhitthana"),
                         ],
                         nav=True,
                         in_navbar=True,
                         label="Contributors",
                    ),
                    ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
    className="mb-5",
)
#END OF: Navigation Bar---#

# ---Top Cards---#
topCards = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(
                                "Loading..", id="labelChosenDate", className="card-title"),
                            html.P(
                                "is the current chosen date",
                                className="card-text",
                            ),
                        ]
                    ),
                    color="success", inverse=True)),
                # Inverse the colors
                dbc.Col(dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Loading...", id="labelChosenPredictionModel",
                                    className="card-title"),
                            html.P(
                                "is the chosen prediction model",
                                className="card-text",
                            ),
                        ]
                    ),
                    color="danger", outline=True)),
                dbc.Col(dbc.Card(dbc.CardBody(
                    [
                        html.H5(
                            "Loading..", id="numberOfTunaLocationsInSelection", className="card-title"),
                        html.P(
                            "total tuna locations in the selected date",
                            className="card-text",
                        ),
                    ]
                ),
                    color="info", outline=True)),

                dbc.Col(dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(str(len(listOfFiles)),
                                    className="card-title"),
                            html.P(
                                "days worth of data",
                                className="card-text",
                            ),
                        ]
                    ),
                    color="primary", outline=True)),
                # ---
            ],
        )

    ],
    # className="mt-4",
)
#END OF: Top Cards---#

# ---BODY---#
body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Choose Settings"),
                        html.P('''
                                    Pick the year and then play around with the sliders to select the date on the map. You can also view the individual latitude and longitude on the table below.
                                '''),
                        # =-=-=-HTML DIv for Dropdown for prediction model picker=-=-=-
                        html.Hr(),
                        html.H5("Pick the prediction model:",),
                        html.Div([
                            dcc.Dropdown(
                                id="dropdownPredictionModel",
                                options=[  # actual, predicted60, predicted70, predicted80
                                    {'label': 'actual', 'value': 'actual'},
                                    {'label': 'cleaned_data_22kmV2',
                                        'value': 'cleaned_data_22kmV2'},
                                    {'label': 'cleaned_data_22km',
                                     'value': 'cleaned_data_22km'},
                                    {'label': 'cleaned11kmOLD',
                                        'value': 'cleaned11kmOLD'}
                                ],
                                value='actual', clearable=False),
                            dbc.Tooltip(
                                "Choose the prediction model or dataset to show on the map.",
                                target="dropdownPredictionModel",
                            ),

                        ],  # className="nine columns"
                        ),

                        # =-=-=-HTML DIv for Dropdown=-=-=-
                        html.H5("Pick the year:",),
                        html.Div([
                            dcc.Dropdown(
                                id="dropdownYear",
                                options=[
                                    {'label': 'All Years',
                                     'value': 'All Years'},
                                    {'label': '2012', 'value': '2012'},
                                    {'label': '2013', 'value': '2013'},
                                    {'label': '2014', 'value': '2014'},
                                    {'label': '2015', 'value': '2015'},
                                    {'label': '2016', 'value': '2016'}
                                ],
                                value='All Years', clearable=False),
                            dbc.Tooltip(
                                "Select the year in order to limit the slider to only pick the selected year.",
                                target="dropdownYear",
                            ),
                        ],  # className="nine columns"
                        ),

                        # =-=-=-HTML DIv for Slider=-=-=-
                        html.H5("Pick your date:",
                                className="three columns"),
                        html.Div([
                            dcc.Slider(
                                id="dateSlider",
                                min=0,
                                max=len(listOfFiles)-1,
                                value=0)
                        ], className="nine columns"),
                    ],
                    md=4,
                ),
                dbc.Tooltip(
                    "Slide me to change the date!",
                    target="dateSlider",
                ),
                # -----Mapbox Column----- #
                dbc.Col(
                    [
                        html.H2("Map"),
                        dcc.Graph(
                            id="map-graph"
                        ),
                    ],  # md=8,
                ),
            ]
        )
    ],
    className="mt-4",
)
#END OF: Body---#

# ---Table Bottom---#
tableBottom = dbc.Container(
    [
        dbc.Row(
            [
                # =-=-=-HTML DIv for Data Table=-=-=-
                dbc.Col([


                    html.Div([
                        html.Hr(),
                        html.H3("Coordinates Table"),
                        dbc.Alert(
                            "Note: Some fields may be empty because there are data that are not available.", color="info"),
                        html.P(
                            "Each row represents a coordinate of a predicted location of tuna."),
                        dt.DataTable(
                            id="tableFish",
                            columns=[
                                {"name": "lat", "id": "lat"},
                                {"name": "lon", "id": "lon"}],
                        )
                    ], className="ten columns offset-by-one"),
                ]),


                # ----

                # ---
            ],
        )

    ],
    # className="mt-4",
)
#END OF: Table Bottom---#

#---------------------------APP LAYOUT-------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = "Tuna Fish Forecaster"
app.layout = html.Div([  # TODO: EDIT ME!
    logoTuna,
    topCards,
    body,
    tableBottom,

    # -----
    html.Div([
        html.P('Developed by Deananda Irwansyah, Christopher Yefta, & James Adhitthana',
               style={'display': 'inline'})
    ], className="twelve columns", style={'fontSize': 18, 'padding-top': 20, 'textAlign': 'center'}
    ),
])


#----------Callbacks---------#


#---Callback Slider to Data Table---#
@app.callback(
    # set the output as the checkbox's options
    [dash.dependencies.Output("tableFish", "data"),
     dash.dependencies.Output("labelChosenDate", "children"),
     dash.dependencies.Output("numberOfTunaLocationsInSelection", "children"),
     # dash.dependencies.Output("datePicker", "date"),
     ],
    # set the iniput as the radiobutton's values
    [dash.dependencies.Input("dateSlider", "value"),
     dash.dependencies.Input("dropdownPredictionModel", "value"), ]
    #     [dash.dependencies.Input("tableFish", "data"),
    #  dash.dependencies.Input("labelChosenDate", "children"), ])
)
def changeDate(selector, valueDropdown):
    selectedDate = listOfFiles[selector]
    currentChosenPredictionModel = "\\"+valueDropdown + \
        "\\"  # valueDropdown is the value of the folder name
    #---Load Datasets---#
    try:  # load the CSV file (file has to be in the current working directory)
        dataBaru = pd.read_csv(
            defaultFolderDirectory+currentChosenPredictionModel+selectedDate)  # 2012-01-01.csv
        print("File "+defaultFolderDirectory+currentChosenPredictionModel+selectedDate +
              " from listOfFiles["+str(selector)+"]"+" loaded successfully ")
        # -4 because we want to get rid of the ".csv" file extension
        labelBaru = selectedDate[: -4]
    except Exception as e:
        print(
            "ERROR kykny filenya ga ada deh di Current working directorynya: ", os.getcwd())
        print(e)
        print("\nI stopped the app for you :)")
        raise SystemExit
    # --
    data = dataBaru.to_dict("rows")  # get the rows for each columns
    labelNumberOfTunaLocationsInSelection = str(len(data))
    # Change the datePicker date
    yearConverted = int(labelBaru[0: 4])

    if(labelBaru[5: 7][0] == "0"):
        monthConverted = int(labelBaru[5: 7].lstrip("0"))
    else:
        monthConverted = int(labelBaru[5: 7])

    if(labelBaru[8: 10][0] == "0"):
        dateConverted = int(labelBaru[8: 10].lstrip("0"))
    else:
        dateConverted = int(labelBaru[8: 10])
    dateBaru = datetime(yearConverted, monthConverted, dateConverted)
    # --

    return data, labelBaru, labelNumberOfTunaLocationsInSelection  # ,dateBaru


#---------Callback Dropdown to Slider---------#
@app.callback(
    # set the output as the checkbox's options
    [  # dash.dependencies.Output("dateSlider", "marks"),
        dash.dependencies.Output("dateSlider", "max"),
        dash.dependencies.Output("dateSlider", "min")],
    # set the iniput as the radiobutton's values
    [dash.dependencies.Input("dropdownYear", "value"),
     # dash.dependencies.Input("datePicker", "date")
     ]
)
def changeYear(selector):  # , datePickerDate):
    selectedYear = selector
    if(selectedYear != "All Years"):
        print("\nChanged Year to: "+selectedYear)
        selectedYearFileIndexesLocations = []
        try:
            for i in range(len(listOfFiles)):
                if(listOfFiles[i].startswith(selectedYear)):
                    # print("["+str(i)+"] ", end='')
                    # print(listOfFiles[i])
                    selectedYearFileIndexesLocations.append(i)
        except Exception as e:
            print("ERROR: in dropdown menu. - ", e)

        maxDate = selectedYearFileIndexesLocations[len(
            selectedYearFileIndexesLocations)-1]
        minDate = selectedYearFileIndexesLocations[0]
        # marks = {
        #     i: listOfFiles[i]
        #     for i in range(minDate, maxDate)
        # }
    else:
        print("All Years Chosen In Dropdown Menu")
        maxDate = len(listOfFiles)-1
        minDate = 0
        # marks = {
        #     i: listOfFiles[i]
        #     for i in range(0, len(listOfFiles))
        # }
    return maxDate, minDate


#---------Callback Mapbox---------#
@app.callback(
    dash.dependencies.Output("map-graph", "figure"),  # output to map graph
    [dash.dependencies.Input("tableFish", "data"),
     dash.dependencies.Input("labelChosenDate", "children"), ])  # input from dropdown list
def update_graph(data, labelChosenDate):
    # --Place all the data from the Data Table into an array for latitude and longitude--
    try:
        currentLat = []
        currentLon = []
        for i in range(len(data)):
            # List for current chosen table's latitudes
            currentLat.append(data[i]["lat"])
            # List for current chosen table's longitude
            currentLon.append(data[i]["lon"])
    except Exception as e:
        print("ERROR: Data is empty: ", e)
        print("I skipped the data file for you :)\n")
    # END OF: lace all the data from the Data Table into an array for latitude and longitude--

    # -=-=-=ScatterMapBox-=-=-=
    coordinateLabels = []
    for i in range(len(currentLat)):
        # coordinateLabels.append(i)
        latAndLong = "("+str(currentLat[i]) + " , " + str(currentLon[i])+")"
        coordinateLabels.append(latAndLong)

    trace1 = [go.Scattermapbox(
        lat=currentLat,
        lon=currentLon,
        mode='markers',
        hoverinfo='text', showlegend=True,
        marker={'symbol': "circle", "opacity": 0.8,
                'size': 6, "color": "#c51b8a"},  # plane symbol
        text=coordinateLabels)  # TODO: CHANGE ME
    ]
    try:
        if(labelChosenDate != None):
            dateForMap = labelChosenDate
        else:
            dateForMap = ""

        layout1 = go.Layout(  # map layout
            title=f'Fish Locations for ' + dateForMap, autosize=True, hovermode='closest', showlegend=False, height=550,
            mapbox={'accesstoken': mapbox_access_token, 'bearing': 0, 'center': {'lat': -5.194638, 'lon': 115.241028},
                    'pitch': 0, 'zoom': 2.5, "style": 'mapbox://styles/mapbox/light-v9'}, )
    except Exception as e:
        print("Error getting map date", e)

    return {"data": trace1, "layout": layout1}


#---Callback dropdown prediction model---#
@app.callback(
    # set the output as the checkbox's options
    dash.dependencies.Output("labelChosenPredictionModel", "children"),
    # set the iniput as the radiobutton's values
    [dash.dependencies.Input("dropdownPredictionModel", "value"), ]
)
def changeLabelChosenPredictionModel(selector):  # , datePickerDate):
    labelBaru = selector  # change label
    return labelBaru


#---Main---#

if __name__ == "__main__":
    app.run_server(debug=True)
