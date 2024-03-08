# sql-challenge

## Project Overview:
This project involves creating a Flask application to analyze weather data stored in an SQLite database. The database contains two tables: "measurement" and "station". The tasks include performing precipitation analysis, station analysis, and creating API routes to interact with the data.

## Project Structure:
- climate.ipynb: This is the Jupyter Notebook file where you conduct your analysis or develop your project. It contains code, explanations, visualizations, and results.
- app.py: This file contains the Flask application code where you define routes and integrate your analysis from the Jupyter Notebook into a web application.
- templates/: This directory contains HTML templates for rendering web pages in your Flask application.

## Precipitation Analysis:
- The precipitation analysis involves querying the database for precipitation data and displaying it in a plot.
- Ensure the database connection is established, and the necessary SQLAlchemy classes are defined.
- Precipitation data for the last year will be fetched and displayed using Pandas DataFrame and plotted.

## Station Analysis:
- Station analysis involves querying station data to find the most active station and its temperature statistics.
- The number of stations, the most active station, and its temperature statistics will be queried and displayed.

## API SQLite Connection & Landing Page:
- The Flask application will serve as an API to interact with the SQLite database.
- The landing page will display available routes and provide links to access API endpoints.

## API Static Routes:
- The API will have static routes to retrieve precipitation, station, and temperature observation data.
- These routes will return JSONified data based on specified criteria.

## API Dynamic Route:
- The API will have dynamic routes to retrieve temperature statistics based on start and end dates provided in the URL.
- The routes will accept parameters and return calculated temperature statistics accordingly.

## Credits:
This project was developed by Anna Ramer as part of Rutgers Bootcamp: Module 10 Assignment.

### Special Thanks:
I would like to express my gratitude to my Teaching Assistant, James Newman, for his guidance. His assistance was invaluable in the successful completion of this assignment.

I would also like to acknowledge GitHub User: davidwjones/AdvancedDataHomework for providing direction for this project. Although only a small portion of the code was utilized for the structure of the Climate app. The starter approach significantly helped in the development of the API's.
