CS-UY 3083 Introduction to Databases Final Project (Part 3)
Matthew Maung mnm9819
Zaf Nazir zan229

Purpose of Project:
* The purpose of this project is to turn the database that we have created and to make it a functioning website.
* This involves creating html files, (Which are shown in views) As well as adding functions that were mentioned in the rubric
* such as buying tickets, adding customer, customer login, etc.
* Additionally, we have additional requirements such as making sure our database is immune to SQL injections ("Delete Customer Tables LLC")
* and has correct authorization.

About each of the files:

index.html
* This is the homepage for our website. It includes buttons to redirect users to different sections of the website or perform specific functionalities.

customer_login.html
* This is the page where customers can log in to the server and perform actions such as booking flights or managing their account.

customer_register.html
* This is the page where new customers can register for an account. It collects information such as username, password, and other necessary details.

staff_login.html
* This is the page where staff members can log in to the server and access their staff-specific functionalities.

staff_register.html
* This is the page where staff members can register for an account. It collects information such as username, password, and other necessary details.

ticket_purchase.html
* This is the page where customers can purchase tickets for flights. It provides a form to enter the necessary details for the ticket purchase.

add_airplane.html
* This is the page where staff members can add a new airplane to the database. It collects information such as the airplane's model, capacity, and other necessary details.

add_airport.html
* This is the page where staff members can add a new airport to the database. It collects information such as the airport's name, location, and other necessary details.

book_flight.html
* This is the page where customers can book a flight. It provides a form to enter the necessary details for the flight booking, such as the departure and arrival airports, date, and number of passengers.

change_status.html
* This is the page where staff members can change the status of a flight. It provides a form to select the flight and update its status, such as "On Time", "Delayed", or "Cancelled".

checkout.html
* This is the page where customers can review and confirm their ticket purchase before making the payment. It displays the details of the selected flight and allows customers to proceed with the payment.

create_flight.html
* This is the page where staff members can create a new flight. It collects information such as the departure and arrival airports, date, time, and other necessary details.

customer_home.html
* This is the homepage for logged-in customers. It provides links to different sections of the website, such as booking flights, managing their account, and viewing their purchase history.

staff_home.html
* This is the homepage for logged-in staff members. It provides links to different staff-specific functionalities, such as managing flights, airports, and maintenance schedules.

schedule_maintenance.html
* This is the page where staff members can schedule maintenance for an airplane. It provides a form to select the airplane and specify the maintenance date and details.

view_airplanes.html
* This is the page where staff members can view the list of airplanes in the database. It displays information such as the airplane's model, capacity, and current status.

view_customers.html
* This is the page where staff members can view the list of customers in the database. It displays information such as the customer's name, email, and other details.

view_flight_rating.html
* This is the page where customers can view and rate their past flights. It displays the details of the flight and allows customers to provide a rating and feedback.

view_flights_customer.html
* This is the page where customers can view their upcoming and past flights. It displays information such as the flight number, departure and arrival airports, date, and status.

view_flights_staff.html
* This is the page where staff members can view the list of flights in the database. It displays information such as the flight number, departure and arrival airports, date, and status.

view_maintenance.html
* This is the page where staff members can view the maintenance schedule for airplanes. It displays information such as the airplane's registration number, maintenance date, and details.

view_purchases.html
* This is the page where customers can view their purchase history. It displays information such as the flight number, departure and arrival airports, date, and ticket price.

view_revenue.html
* This is the page where staff members can view the revenue generated from ticket sales. 

app.py
* This is where all the routes are, as well as any code related to making sure the functionality of the buttons works

Delegation of Responsibilities
* Generally speaking, a majority of the project was done together/simultaneously, but each person did their fair share
* Responsibilities are outlined below based on person and on parts

Part 1:
* Both of us worked simultaneously on creating the ER diagrams together in draw.io
* Work was done together on voice calls while we both worked on drawing arrows as well as outline the different tables

Part 2:
* Both of us worked on the Relational Schemas as well as the queries themselves. 
* I (Matthew) was primarily responsible for creating the relational schemas and the basic outlines for the queries while Zaf 
* focused mainly on the queries themselves, making sure everything fit together including the inserts and the selections

Part 3:

Matthew Maung
* I worked specifically on buildling the html templates and styling them, as well as making sure the paths outlined in flask worked correctly. 
* Additionally, a majority of the coding for rendering views from the database was my work as well. 
* I focused more on the main ui that you're seeing, including the registration and login forms

Zaf Nazir
* Zaf specifically worked on making sure the queries matched the specifications of the project
* as well as made sure that the html correctly functioned with the app.py file
* additionally, he helped a lot with the review and maintenance section