# Yelp Dataset Search Application

#### A fully functional search application for Yelp.com’s business review data (https://www.yelp.com/dataset). 
This project was created in order to create an application that allows a user to utilize the yelp business dataset. In this project you can do the following
* Search businesses based on state, city, and zipcode
* Further filter businesses based on category (restaurant, spa etc.)
* Get statistics on selected zipcode
* Find popular and successful business in zipcode

## Dataset into PostgreSQL 
Given the JSON files of data, the parse code in this project was used to turn that data in txt files as INSERT statements to add the data into the database. 

## Project Demo
https://youtu.be/QRVkAM17sW8

## Usage
Since this project was created using a local database, the easiest way to using this project would be the following
1. clone this project
```bash
git clone https://github.com/skyllare/Yelp-Database-Challenge-.git
```
2. create a database using the createtables.txt file
3. use the parse code to create txt files for the data and insert into database
4. connect the database to the database code
5. run database code
