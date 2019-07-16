# TunaForecaster
Forecasting the location of Tuna using SVM (Support Vector Machine) through Python and Dash.
The initial goal of our program is to.....#TODO

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

```
python app.py
```

If all works well this is the console should show the IP address of where the dashboard is hosted. 

![tutorial1](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/running-tut-1.PNG)

Then copy and paste the IP address to your browser in order to access the application's user interface and it should show similar to the image below. 

![tutorial2](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/home-cleaned-data-11km-table.PNG)

By default, the dashboard shows the "actual" data which consists of the real raw data that we have not manipulated in any way. This data is what we used to train our model on. 
You can change this by picking the prediction model from the dropdown menu.

![tutorialPickPredictionModel](#)

You can play around with the dashboard by directly manipulating the slider to pick the date and the map and UI will change accordingly.

![tutorial3](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-slider.gif)

You could also specify the sliders to only go through a specific year by picking the year you want on the dropdown list.

![tutorial4](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-pick-year.gif)

You can also play around with the interactive map by zooming in, picking the points you want, highlighting over the points to see the coordinates and more.

![tutorial6](#)

Last but not least, you can scroll down and view the individual coordinates of each point from the table on the bottom of the page.

![tutorial5](https://raw.githubusercontent.com/jamesadhitthana/TunaForecaster/master/Screenshots/tut-table-coordinates.PNG)

## Explanation

On this section, we will explain the techniques that we have used to achieve our results.

### function1blablablablalaba

blablablalbalbalblalaba 
```
sblablablalbalbalblalaba
```
blablablalbalbalblalaba
```
blablablalbalbalblalaba
```

## Data Cleansing

Before the data is trained, we had to clean the data first in order for our model to not be distorted. 

### tunaDataCleanerSSTChlorophyll.py

This python script is responsible for automatically iterating through the original data source folder, cleaning the data, and then saving the new cleaned data files in a new folder. 

Since our data is a collection of coordinates of boats around Southeast Asia we wanted to make sure that these boats are out to fish and not parked in a sea port. Therefore, to clean the data, we had to search for the coordinates of seaports that surround Southeast Asia and also sea ports along the northern coast of Australia and then compile these coordinates into a .CSV file. 

With this seaport CSV file we can then compare if each of the data in the original source is between 11.132KM from the seaports or not. If a point in our data source is less than 11.132KM from any port in the list, then the data is deleted. If a coordinate point is more than 11.133KM from any sea port in the list, then the data is saved.

The distance of 11.132KM is chosen because according to our research, tuna fish tend to start to appear about 7 miles off-shore or about  11.2654KM. Therefore, we had to make sure that all of the coordinates that are in the data source are at least 11 kilometers away from the shore in order to make sure that these boats are fishing for tuna and not fishing for other sea creatures. 

Since our data source uses the decimal degree geographic information system that looks like this (-6.228427, 106.609744) instead of looking like this (6°13'42.3"S 106°36'35.1"E) , we can then consult a [table](https://en.wikipedia.org/wiki/Decimal_degrees) that has a list of decimal degree precision versus length. According to the table, since the data source we are using is located at the equator, the length for every 0.1 decimal degree is 11.132km. 

Therefore for every coordinate of the source data that we have, if it is ±0.1 decimal degrees from any seaport that is in the seaport.csv file (this means that it is between 11.132km from any seaport), the coordinate point is deleted from the data source.


```
sblablablalbalbalblalaba
```
blablablalbalbalblalaba
```
blablablalbalbalblalaba
```

## Forecasting and SVM

blalalalblalabala....

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
