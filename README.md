<h1 align="center">
    Tuna Forecaster
</h1>
<p align="center">
<sup>
<b>Forecasting the location of 🐟 Tuna using SVM (Support Vector Machine) through Python and Dash.</b>
</sup>
</p>


## Introduction

The initial goal of our program is to..... **TODO DEAN KERJAIN INI**

## Getting Started

To be able to run this app, you will need to have the following prerequesites and have to follow the instructions below.

### Prerequisites

Python 3 with the following additional libraries:
- pandas
- dash
- dash-table
- dash-bootstrap-components
- plotly


### Running the application

Make sure you have all the prerequisites installed and you are connected to the internet.
Then clone/download the folder, open terminal/cmd and navigate to the folder and run app.py:

```bash
python app.py
```

If all works well this is the console should show the IP address of where the dashboard is hosted. 

![tutorial1](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/running-tut-1.PNG)

Then copy and paste the IP address to your browser in order to access the application's user interface and it should show similar to the image below. 

![tutorial2](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/home-cleaned-data-11km-table.PNG)

By default, the dashboard shows the "actual" data which consists of the real raw data that we have not manipulated in any way. This data is what we used to train our model on. 
You can change this by picking the prediction model from the dropdown menu.

![tutorialPickPredictionModel](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-pick-model.gif)

You can play around with the dashboard by directly manipulating the slider to pick the date and the map and UI will change accordingly.

![tutoriaSlider](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-slider.gif)

You could also specify the sliders to only go through a specific year by picking the year you want on the dropdown list.

![tutoriaYear](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-pick-year.gif)

You can also play around with the interactive map by zooming in, picking the points you want, highlighting over the points to see the coordinates and more.

![tutoriaMap](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-map.gif)

Last but not least, you can scroll down and view the individual coordinates of each point from the table on the bottom of the page.

![tutorial5](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-table-coordinates.PNG)

## Explanation

On the following sections, we will explain the techniques that we have used to achieve our results.

## Data Cleansing

Before the data is trained, we had to clean the data first in order for our model to not be distorted. 

### tunaDataCleanerSSTChlorophyll.py

This python script is responsible for automatically iterating through the original data source folder, cleaning the data, and then saving the new cleaned data files in a new folder. 

Since our data is a collection of coordinates of boats around Southeast Asia we wanted to make sure that these boats are out to fish and not parked in a sea port. Therefore, to clean the data, we had to search for the coordinates of seaports that surround Southeast Asia and also sea ports along the northern coast of Australia and then compile these coordinates into a .CSV file. 

With this seaport CSV file we can then compare if each of the data in the original source is between 11.132KM from the seaports or not. If a point in our data source is less than 11.132KM from any port in the list, then the data is deleted. If a coordinate point is more than 11.133KM from any sea port in the list, then the data is saved.

The distance of 11.132KM is chosen because according to our research, tuna fish tend to start to appear about 7 miles off-shore or about  11.2654KM. Therefore, we had to make sure that all of the coordinates that are in the data source are at least 11 kilometers away from the shore in order to make sure that these boats are fishing for tuna and not fishing for other sea creatures. 

Since our data source uses the decimal degree geographic information system that looks like this (-6.228427, 106.609744) instead of looking like this (6°13'42.3"S 106°36'35.1"E) , we can then consult a [table](https://en.wikipedia.org/wiki/Decimal_degrees) that has a list of decimal degree precision versus length. According to the table, since the data source we are using is located at the equator, the length for every 0.1 decimal degree is 11.132km. 

Therefore for every coordinate of the source data that we have, if it is ±0.1 decimal degrees from any seaport that is in the seaPort.csv file (this means that it is between 11.132km from any seaport), the coordinate point is deleted from the data source.

#### #--How to use--#
1. Place this python file in the same folder that contains the seaPort.csv file.
2. Place the folder that contains the data to clean into a new folder inside the folder and change the "folderOfDataToClean" variable to the name of your chosen folder you placed previously to clean
3. Change the "cleanedFolderPath" variable to a new folder name you want to have the cleaned files to be put in
4. Modify the checkPort(... 0.2) function and change the number to the desired decimal degree
5. Run the script. The results should appear in the folder you have configured in the "cleanedFolderPath" variable.

#### Functionalities

```python
 cleanFile(defaultFolderDirectory+folderOfDataToClean + listOfFiles[i], cleanedFolderPath, "seaPorts.csv")
```

The function above takes the original folder that contains the files to clean and then a list of files that are in the folder and the output folder directory along with the seaPorts.csv files that contains all the coordinates for the seaports to clean from. This is the main function that we created in order to clean a single file and save it in the target file. Therefore to clean all the files in the folder, in the script we created a for loop to call this function according to all of the files that exists in our folder.

```python
        listOfLat, listOfLng, listOfSST, listOfChlorophyll = checkPort(dataFrameIndoSeaPorts["Latitude"][i], dataFrameIndoSeaPorts["Longitude"][i], listOfLat, listOfLng, listOfSST, listOfChlorophyll, 0.1)
```

This function above returns four lists that contains the latitude, longitude, SST, and chlorophyll of the current coordinate input. The function takes a single point's latiitude and longitude and takes the current list of latitude, longitude, sst, and chlorophyll along with the decimal degree (in the example above it is 0.1 which results to 11.132km).

```python
latChecked, lngChecked, sstChecked, chlorophyllChecked = checkLatLng(portLat, portLong, listOfLat, listOfLng, listOfSST, listOfChlorophyll, decimalToCheck)
```
This function checkLatLng(...) returns the result of the checked latitude, longitude, SST, and chlorophyll if it is not in the 11.132km radius of any port in the seaPort.csv file. This function needs the current port's lat and long along with the list of latitude, longitude, sst, list of chlorophyll and the decimal degree to check.

This function contains the main calculation that it needs to check whether it is ±0.1 decimal degrees from the port. It works by checking the latitude and longitude of a coordinate point with the latitude of the port's latitude longitude. If the current coordinate it is less than -0.1 of the any port or more than +0.1 of any port it will add the coordinate to the final file. This is because it means that it is at least 1.132km further north, east, south, and west than any seaport in the seaPort.csv file.


## Dash Dashboard with Bootstrap

Dash is a framework that allows us to build beautiful, web-based analytics applications. Through dash and its dash-core-components, we are able to create interactive elements that build up our interactive dashboard. In addition to that, this project also implements the bootstrap framework through the dash-bootstrap-components additional module in order to assist with the front-end development of the layout and design of the dashboard.

### Setting up the Dash app

In order to show the data that we have produced into a map, we used MapBox's map API which needs an access token that can be requested on [this link](https://docs.mapbox.com/api/). Then with the API token, replace the variable below to your API token.

```python
mapbox_access_token = "INSERT ACCESS TOKEN HERE"
```

The first part of the dash app consists of scanning the chosen folder that contains all of the coordinate information and then placing it into a list "listOfFiles[]. By default the folder loaded is the actual data (not trained) because that is the default first data that is shown on the dashboard.

```python
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
```

Next is the essential part where we create the variables that contains the components that will be placed into the dashboard. These components are made of the dash-core-components and dash-bootstrap-components that are provided in the modules we imported previously. In the snippet below the dash-core-components can be seen by the prefix "dcc." and the dash-bootstrap-components can be seen with the prefix "dbc.". Dash also supports html elements such as html.P, html.H1, html.Div,html.Hr, and more and so certain HTML elements are used to create the overall layout of the dashboard.

```python
logoTuna = dbc.Navbar(
    dbc.Container(
        [html.A(
            ...
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    ...
                        ...
                    ], c...
                ),
topCards = dbc.Container(
    [dbc.Row(
            [..    dbc.Col(dbc.Card(...
                    dbc.CardBody(...
body = dbc.Container(
    [dbc.Row(
            [...
                dbc.Col(...
                    [       ..[               
tableBottom = dbc.Container(
    [dbc.Row(
            [dbc.Col([
                    html.Div([
                        html.Hr(),
                        html.H3("Coordinates Table"),
                        ....
```

After creating the variables that will house the components for the dashboard, we need to setup dash to recognize the python script as a dash app. Since Dash supports the use of CSS, and since we are also using the bootstrap framework, we used an external CSS file in order to help make the application more user friendly. Also we can change the title that appears on the browser to a custom title which we changed accordingly.

```python
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = "Tuna Fish Forecaster"
```

Now that dash recognizes that the python script is a dash app, we can then input all of the variables that contained the components created previously into the dash app's layout. At the end, we also added an additional html.Div with extra information to demonstrate that it is also possible to add components wihtout creating a variable.

```python
app.layout = html.Div([  
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
```

Now that the layout and view is all set up, we must create the callbacks which basically handles all of the main functionality of each of the interactable components in the app and sets where the output is for each callback. For every callback, it must first start with an "@app.callback"() function that contains the parameters for at least one dash.dependencies.Output component which are components such as labels/tables/maps/graphs/any other component that needs to receive input data. The function also must recieve at least one dash.dependencies.Input component such as a slider/dropdown/any other component that can be manipulated by the user.

After every "@app.callback()" function, it must then be directly followed underneath by a function that recieves the parameters of the inputs that we have set up in the dash.dependencies.Input values. Then this function can be filled with the intended functionalities. By the end of this function, it must return the variables according to the dash.dependencies.Output we hav previously set up according to the order given.

```python
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
    ...
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
    ...
      return maxDate, minDate
      
#---------Callback Mapbox---------#      
@app.callback(
    dash.dependencies.Output("map-graph", "figure"),  # output to map graph
    [dash.dependencies.Input("tableFish", "data"),
     dash.dependencies.Input("labelChosenDate", "children"), ])  # input from dropdown list
def update_graph(data, labelChosenDate):      
      ...
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
```

Now that all of the essential functionality of the app is created, this snippet essentially runs the dash app when the python script is executed.

```python
if __name__ == "__main__":
    app.run_server(debug=True)
```

## Forecasting and SVM

### function1blablablablalaba

blablablalbalbalblalaba 
```python
sblablablalbalbalblalaba
```
blablablalbalbalblalaba
```python
blablablalbalbalblalaba
```

## Built With
* [Python](https://www.python.org/) - Python Programming Language
* [Dash](https://plot.ly/dash/) - Dash
* [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) - Bootstrap components on Dash
* [Plotly](https://plot.ly/) - Plotly graph
* [Mapbox](https://www.mapbox.com/) - Mapbox Map API

## Authors

* **James Adhitthana** - [jamesadhitthana](https://github.com/jamesadhitthana)
* **Christopher Yefta** - [ChrisYef](https://github.com/ChrisYef)
* **Deananda Irwansyah** - [hikariyoru](https://github.com/hikariyoru)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments
* Fish data by [Global Fishing Watch](https://globalfishingwatch.org/)
