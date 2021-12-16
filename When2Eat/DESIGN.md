# WHEN2EAT: DESIGN DOC
Made by: Nadine Han and Julianna Zhao
Class: CS50 Fall 2021
 
Table of Contents
1: Files Explanation
2: Implementation
3: Additional Design Choices
4: Limitations that we would have taken care of if we had more time:
 
SECTION 1. Files Explanation
   Part A. Overview
       This program runs on Flask, and takes inspiration from the CS50 PSet 9 on Finance, which means that it incorporates several languages, including but not limited to: Python, SQL, Javascript, HTML, and CSS. The main file that connects all of the other files in this project is called app.py, and it contains much of the back-end programming for W2E to work. The rest of the folders group files mostly by language and by function.
 
       The overall structure of this project is based off of Finance from PSet 9 because we found it to be the most intuitive and comprehensive for websites, hence the configuration of a main app and sub-folders containing HTML pages and CSS. 
 
   Part B. Main Folder
       The main applications in the main directory (not a sub-folder) are: app.py, database.db, and helpers.py. app.py contains all of the functions relating to: calling and updating data from databases using SQL, creating a page route for different parts of the program, and returning different HTML pages to users based on requests.

       helpers.py refers to other helper functions to ensure that Flask runs smoothly in app.py. This is pulled from the Finance PSet.
      
       database.db runs on PHPLite, and contains all of the information that is entered into the system by the user. Here is a rundown of each database within the .db document - the entire directory can be found by clicking on the preview link provided by the database.db file in CS50's VSCode:
	
	    CREATE EVENT DATABASES:
           event_dates: logs all the dates included for an event when created, with each entry referring to a specific date (date) and the event it corresponds to (event_id)
 
           event_locations: logs all the locations included for an event when created, with each entry referring to a specific location (location) and the event it corresponds to (event_id); similar structure to event_dates
 
           events: contains other data about events when created, with each entry referring to a unique event name (event_name) with a unique event_id and records of the user who made it (event_creator_id), as well as the start_time and end_time
 
           hours_24: logs all of the hours available for an event to run in, later used in a helper function in app.py that essentially calculates time differences and makes it easier for the program to run based on times entered — the reason why we have this is so we will not have to have a table where each event shows up for each hour between the start time and end time.
 
	    JOIN EVENT DATABASES:
           event_availability: logs all the data on each user's availability for an event that they join, with each entry under the date and time columns representing a specific timeslot on a specific day that the user (user_id) is available for a certain event (event_id)
 
           location_availability: logs all the data on each user's availability for an event that they join, with each entry under the location column representing a specific location (location) that the user (user_id) is available for a certain event (event_id); very similar structure to event_availability
 
	    OTHER DATABASES:
           users: standard user database, logs unique username and password (hashed) whenever a user registers for an account

 
   Part C. Sub-folders
       There are various sub-folders that the app.py calls upon for help; __pycache__ and flask_session are just helper folders containing files to make sure that Flask runs and data is saved.
 
       The pics sub-folder contains any relevant pictures to the program, but for now is mostly unused; the logo of When2Eat references a picture uploaded to a public picture hosting website, although the logo is original (created by us).
 
       The static sub-folder contains all of the CSS code, or documents meant to prettify the website; styles.css is the main sheet used to prettify the pages.
 
       The templates sub-folder contains all of the HTML code, or display/formatting for each page that calls on variables defined from app.py. Here is an explanation of each one:
 
	    HELPER HTMLS:
           layout.html: parent HTML sheet that contains most of the primary formats, like footer, navigation bar, and any functions that are carried through each page; this was inspired by Finance PSet
 
           apology.html: the error page that appears whenever a user submits an incomplete form or does something wrong
 
 
	    MAIN FUNCTION HTMLS:
           account.html: displays the home page of the website, which are account details. Here, one can delete events that they have joined, change their password, and view events that they have joined and created. NOTE:
 
           create.html: displays the page for creating an event, including all of the input boxes for event details
 
           join.html: displays the input page for inserting event code to join event
 
           schedule.html: displays the page for joining an event, allows users to update their availability
 
           delete.html: displays the page for deleting events joined or created
 
	    LOGIN/REGISTRATION HTMLS:
           login.html: displays the login page for logged out users

           register.html: displays the registration page

           changePassword.html: displays the page for changing password, accessed through Account Page
 
SECTION 2. Implementation 
	When brainstorming functions to implement for When2Eat, we decided there were a few main ones that we needed: Create Event, Join Event, and View Event. In order to access this information, we decided that it would be helpful to keep track of all created/joined events in one place per user, which would dictate a Log In/Register function. Hence, it then follows that we should make a Change Password function as well for users who are interested.
 
	Using this framework, we designed databases to store relevant information: a users database for users; event_availability and location_availability for Join Event to store data on users’ availabilities; events, event_dates, and event_locations to store data on a created event, with helper databases like hours_24 to manage times inputted.
 
	We mainly focused for each page on retrieving data through SQL queries in the app.py program, and then displaying those variables in the HTML pages, using JavaScript and jinja when applicable (or when we thought was most appropriate/convenient). The CSS simply grouped together any information and placed them in containers to make things clearer.
 
	The Login/Registration/Change Password design is rather trivial, so we will not go into too much detail on implementation here. Within Join/Create Event, we decided what event parameters would be most useful and settled on: name, date/time, and location; functions were then implemented so that users could select a date (based on the When2Meet interface, which provides a calendar to click on in the Create Event page), enter in time (AM/PM), and then at least one location. Before joining an event, one must be able to input a unique ID to let the server know what event the user is looking for, hence we generated a unique code for each event once it is created. Join mirrors Create, as the user simply indicates their available time and location by clicking on them (also as per When2Meet interface for time; for locations, we just thought checkboxes were the most intuitive). We then realized being able to View Event would be helpful, as well as keeping track of account information, hence we created an Account Page containing links to displays on events joined/created. The View Event mirrors Join and Create. 
 
SECTION 3. Additional Design Choices
	This is in bullet point format, as they refer to smaller design choices - the overall purpose of each document is written above:
 
	    - app.py: All of the program's errors are coded in this file in the format of an apology page being returned (similar to the one from Finance) with the reason for the failure. Hence, the user must refresh/go back to the original page and then re-enter their information while fixing the error in order to bypass the page.
 
	    - create: The maximum of seven dates to choose is implemented in order to maintain the quality of the CSS. We realized while testing that it would be impractical to let a user select a lot of days, as the interface would be overwhelming to any users joining the event (just think about being sent a When2Meet where you have to fill in 30 days’ worth of availability for meals) 
 
	    - two buttons on display pages: Although the users can see how many people are available at specific time slots and locations from the numbers in the tables, we added two buttons (“when/where some are available” and “when/where all are available”) that will change the colors of slots to two different shades of green to make it easier to visualize the information.
 
SECTION 5. Limitations that we would have taken care of if we had more time:
 
	    - The current When2Eat cannot deal with an unlimited number of dates/locations for an event. This is a problem in two parts: 1) giving the user a way to select as many dates and input as many locations as they would like, and 2) formatting it on the page where other users must input availability.
 
	    - In the display of an event, users cannot see which users signed up for what times/locations. We wanted to implement a hover function in Javascript that would allow the user to see which people are available at a specific time slot or location, but we kept running into problems using Jinja in our Javascript. We talked to Nadine’s TF Jason, and after attempting to debug the program with him, we found that the function may be too difficult to implement within the project’s short timeframe. Hence, we decided to provide an alternative option for availability, which were the two buttons highlighting timeslots where Some or All were free. 
 
	    - Event dates are limited to the same month. While the original When2Meet lets the creator of an event scroll down the weeks so they can look at whatever dates they want, When2Eat only allows the creator to look at one month at a time, and so all dates for an event would have to be on that month. If we want to keep the way When2Eat works and also allow users to pick dates from multiple months, we would have to figure out a way for dates on the currently viewed to be saved when the creator moves to another month.