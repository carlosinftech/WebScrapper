== Overview
The objective of this project is to obtain data
from a web source. 

== Requirements
This project is developed with python 3.8 in mind. 
The list of required packages can be found in Requirements.txt file

== Scripts

CreateTables.py : This script deletes existing tables in the
test database and creates a new one from scratch. 

ServePriceAverage : Module in progress not yet functional
whose purpose is to serve data to another application. 
At the present moment it consumes the data from the database
and prints it on console

ServePriceRange : Module in progress not yet functional
whose purpose is to serve data to another application. 
At the present moment it consumes the data from the database
and prints it on console

Launch

To launch the project execute python3 WebScrapper.py from the
project directory. 

== TODO

There are some tasks that are important and have not been 
implemented yet. Such as.
    proper log functionality
    transformation pipeline definition from yaml file
    precise error handling
    flask api interaction.
    add command line arguments functionality
    add unitary testing
