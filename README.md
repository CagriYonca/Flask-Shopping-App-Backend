# Xccellerated Technical Case

## Problem Statement
Building a Flask Backend application for a shepherd that responsible from a tribe of yaks.

## Tools We Used
Our solution has 3 sections as database, backend and containerizing. We are using:
- Python Flask microframework for the backend
- MongoDB Atlas for the database
- Docker for the containerizing

# Installation
The installation of the project is really easy. 
First, build docker image to use:
- `docker build -t flask-app`

Second, run this image with exposing ports:
- `docker run -p 5000:5000 flask-app`

It should be running after the installation of required tools.

# Usage
## YAK 1
In this requirement, we should be able to load and read the data from xml file. First, we should use '/setup' endpoint to load data into the MongoDB(currently I'm using my own database from Atlas). You can use curl to send request directly:
- `curl 0.0.0.0:5000/setup`

#### Note: Old database information will be removed after setup function worked.
<br>

### Our program should include 2 parameters:
- The XML file to read (It's used as 'herd.xml' by default)
- An integer T, representing the elapsed time in days

This feature added into the `/yak-shop/herd/T` endpoint in the second requirement.
<br>

## YAK 2
The following are the requests we wish to make:
- GET /yak-shop/stock/T , Returns a view of our stock after T days
- GET /yak-shop/herd/T , Returns a view of our herd after T days

Now we can test these endpoints:
- With `curl 0.0.0.0:5000/yak-shop/stock/13` command, we can see total milk and skin information
- With `curl 0.0.0.0:5000/yak-shop/herd/13` command, we can see the tribe information

Also, you can see the 'In Stock' and 'Herd' information on the command line as requested.
<br>

## YAK 3
We want to be able to get orders due to our stock capacity. The following endpoint should be added for this purpose:
- POST /yak-shop/order/T
- Body: {"customer": "Medyedev", "order": {"milk": 1100,  "skins": 3}}

With the command below, we can try this endpoint:
- `curl -X POST 0.0.0.0:5000/yak-shop/order/14 -H "Content-Type: application/json" -d '{"customer": "Medyedev", "order": {"milk": 1100,  "skins": 3}}'`
<br>

## YAK 4
Our 4th question is open-ended so we could make improvements in any part we want. For this purpose, 
- I've added test cases for some of service functions
- Containerized our web server
- Used MongoDB as a cloud database
