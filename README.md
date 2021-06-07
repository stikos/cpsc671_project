# Weather data management for motifs detection system

## Introduction
The outcome of this project is a proof-of-concept implementation for a weather data management tool. The purpose of its development is to act as a means for weather scientists to access not only large volumes of weather data and various analytics, but more importantly to discover new knowledge through a series of patterns that have been recognized and stored into that system.
The system in study, developed in python & SQL, consists of a mySQL database tailored to the nature of the available meteorological data, as well as the demands of a collaborating meteorologist, and a variety of python scripts in order to easily implement useful functionalities.

### The Underlying Algorithm
This project is built to support a novel motif detection algorithm, developed by Xylogiannopoulos, Karampelas, and Alhajj [1]. This algorithm can discover patterns in vast amounts of data, among multiple variables.

## Design Decisions
**Python** is a powerful, easy to use scripting language, which makes it a great fit for prototyping purposes. Another advantage of its use in this particular application is its inherent modules for string manipulation. Such modules find great use when handling large amounts of textual and non-textual data. Python also work very well with the mySQL DBMS through the connector module and also has a great set of tools for easily visualizing data and statistics.

As a DBMS for this project I chose **mySQL**. The main reasons behind this decision go as follows:
* It is a very popular DBMS system that is being used for almost 25 years, which means there’s a lot of knowledge and support in the users community, making it a “safe” choice.
* mySQL works great with Linux, onto which I developed this system, while the transition to either Windows or MacOS is almost effortless.
* Open source & Free   

For the design of the database itself, I used **StarUML** which makes it really easy to describe your data through Entity-Relationship diagrams using the Information Engineering notation. Another advantage of using StarUML is that it has an extensive add-ons library, including a tool that produces a DDL script for your database.

## Data Description
The source of the data used is a global dataset from the National Oceanic and Atmospheric Administration (NOAA) [2] which was restricted to specific coordinates that include the wide region of South Balkans and more specifically Greece, as seen in the image below.

![greece_map](https://drive.google.com/uc?export=view&id=1fbPBrLeKOsAa5I_x5mHLHnaQfEvjRbf6)

Out of this vast dataset, for this project I took into consideration the variables of Apparent temperature (K) and geopotential height for the isobaric surface of 500mbar. The time frame of the measurements stretches from Jan 15th, 2015 to Dec 31st, 2016. Measurements were recorded on 6-hour intervals. The measurement grid is defined by 0.25°x 0.25° points (one measurement point on every ¼ of a degree in both directions).

## Development
### Database desgin
The design of the database should both reflect the needs of the weather scientist and also accommodate data in an efficient, non-redundant way.

![db](https://drive.google.com/uc?export=view&id=178Dwthy64c2CUm85IeQKU32b93zZle7P)

### Extract-Transform-Load (ETL)
The first problem that had to be tackled was writing a script to automate the loading of both “raw” weather measurements and pattern data into the database. The data came in a variety of formats, from csv files to partially unstructured text files. A great amount of processing was required to create the individual attributes of the database in the correct form.
A part of the process that added significant delay was the use of a reverse geolocation API (OpenStreetMap’s Nominatim through the **geopy** module), in order to populate the city table by looking only at the coordinates that were provided in the data.

### Queery creation
The value of this tool lies in its ability to provide to the meteorologist the exact pieces of information that are needed. While there’s potentially an abundance of useful queries one can come up with to satisfy the needs of this domain’s expert, for the scope of the courses needs the created queries are rather limited, yet insightful.
One major design decision regarding the queries themselves was defining them as **stored procedures**. There are several reasons behind that:
* It helps distinguish the data functionality from the application, resulting in more comprehensible and “clean” code
* Possible changes in the programming language do not affect the queries/data functionality, and do not require any code to be re-written. This is a problem that would be likely to arise otherwise, since there has been serious consideration of switching from python to another programming language for speed-up.
Regarding the queries themselves, they vary from simple ones e.g. retrieve a list of all the cities in the database for future user input, to slightly more intricate ones e.g *retrieve the top 5 patterns (occurrence) in a radius X from a city Y*.  
The latter consists of 2 component queries: 
The first one gathers the UIDs of all the points on the map that fall within a region that is defined as a square with the city of our user’s choice as it’s center. A slightly challenging problem was the fact that the user input would define distance (area size) in kilometers, whereas in our data we only have geolocations (latitude & longitude). To overcome this I could either use the Haversine formula or use some standard degree-to-distance ratios. For speed and simplicity, I implemented the second solution. 
The size of the area is also defined by the user. The second query then uses that set of point UIDs and can look for the most recurring patterns among them, for a variable of the user’s choice.

### Visualized Results
Using the plotly python module, I was able to visualize some of the results of queries that serve statistics purposes, such as the average daily temperature for May between 2015-2016 in Greece. The result can be seen below:

![viz](https://drive.google.com/uc?export=view&id=15t09Yd430IyO97ALYRejUTLBncdn2k_U)

### User Interface
User Interface
Currently, the tool is offering a simple command line interface, through which the user can either select to rebuild the database or execute queries in order to retrieve information on both the weather variable measurements and the discovered patterns data.

#### Execution Example

![cli](https://drive.google.com/uc?export=view&id=1g6IjsuhBNvEDAhXY9LJ_FsQMvDQChPDg)

## Challenges & Conclusion
One of the biggest challenges of moving the project even further will be incorporating more data (more weather variables, larger time frame). One would have to effectively manage terabytes of data, and achieve realistic response times to ensure the usefulness of the tool.
The results of the algorithm in the original work were very promising. A variety of patterns was discovered among single variable data as well as multivariable data, indicating the possibility of interdependencies. That kind of information can be of great value to  weather analysts, in an effort to not only better understand local weather patterns, but also possibly use such knowledge to improve existing weather prediction models. Expanding that tool with the data management system developed in this project makes it a lot more accessible to the end-user (weather domain expert), and also easily integrable into larger toolsets/systems.

## References
[1] Xylogiannopoulos, K., Karampelas, P., & Alhajj, R. (2019). Multivariate Motif Detection in Local Weather Big Data.

[2] National Centers for Environmental Prediction/National Weather Service/NOAA/U.S. Department of Commerce (2015): NCEP GFS 0.25 Degree Global Forecast Grids Historical Archive. Research Data Archive at the National Center for Atmospheric Research, Computational and Information Systems Laboratory. [https://doi.org/10.5065/D65D8PWK](https://doi.org/10.5065/D65D8PWK)
