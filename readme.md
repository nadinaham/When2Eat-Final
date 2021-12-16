# WHEN2EAT: USER'S MANUAL
Made by: Nadine Han and Julianna Zhao

Class: CS50 Fall 2021

Table of Contents
0: Preface
1: Running the Application
2: Files Explanation
3: Additional Notes

SECTION 0. Preface
This project is titled When2Eat, and is a spinoff of When2Meet, a website that allows users to coordinate meeting times by creating events and having participants indicate their availabilities in order to determine the best meeting time. In this document, we will discuss the main functions of each document, as well as what role they play in the overall program.
 
#### <b>VERY IMPORTANT NOTE:</b> The program is meant to be run in the CS50 VSCode compiler! Running it elsewhere will lead to problems, as the main program app.py relies on Flask, which uses functions imported from the cs50 library.

SECTION 1. Running the Application
    Part A. Startup
        To run the application: 
        1. Upload the csfinal folder to a codespace for running/compiling
        2. In terminal, navigate to csfinal, then run "flask run"
        3. The codespace will then generate a link through which you may copy paste into any browser to pull up the website - it should first show the login page.

    Part B. Navigating the Front-End Website
        Frequently Asked Questions:
        Q: How can I log in?
        A: If you already have an account, simply enter your login information into the form. If not, you can click on the "Register" button in the top right corner.

        If you are interested in using a test account, you can try logging in with the credentials:
            Username: julianna
            Password: password

        Q: How can I register? 
        A: Once you have clicked on "Register", simply enter in any login information you want to make to test it out. Then, click the "Register" button at the bottom to submit your information. If the registration was successful, you should then be redirected to the Log In page.
            Keep in mind that you cannot have a duplicate username, meaning that if you try to register with a username that already exists, you will throw an error!

        Q: Once I log in, how can I navigate around?
        A: Utilize the navigation bar, which is the strip at the top of the website. It includes the Homepage/Account link (click on the logo, the options to Create/Join an event, and the option to Log Out. Other functions, like viewing events you have already joined, deleting them, and/or changing your password, can be done on the Homepage/Account page.

        Q: How can I create an event?
        A: 

        Q: How can I join an event? 

        Q: How can I view events I have already joined or created?
        A: Go to the Account page by clicking of the logo at the top left corner, which will list out links to each event, and click on the event of interest. You will then be redirected to a page that shows the statistics on the event. Note that this CANNOT be edited; if you want to edit the event, you must click on Join Event in the navigation bar and re-enter the event code.
        
        Q: How can I delete an event or my entry in an event that isn't mine?
        A: If you want to delete an event that you created: Navigate to the Account Page and click "Delete Event" under settings. You can then check off the events under "Created Events" that you wish to delete, and click the "Delete" button at the bottom to confirm. This will delete the ENTIRE event!

        If you want to delete your entry in an event that you joined/isn't yours: Navigate to the Account Page and click "Delete Event" under settings. You can check off the events under "Joined Events", and click the "Delete" button at the bottom to confirm. This will delete ONLY YOUR AVAILABILITY ENTRY in an event!

SECTION 2. Files Explanation
    Part A. Overview
        This program runs on Flask, and takes inspiration from the CS50 PSet 9 on Finance, which means that it incorporates several languages, including but not limited to: Python, SQL, Javascript, HTML, and CSS. The main file that connects all of the other files in this project is called app.py, and it contains much of the back-end programming for W2E to work. The rest of the folders group files mostly by language and by function. 

    Part B. Main Folder
        The main applications in the main directory (not a sub-folder) are: app.py, database.db, and helpers.py. app.py contains all of the functions relating to: calling and updating data from databases using SQL, creating a page route for different parts of the program, and returning different HTML pages to users based on requests. 
        
        database.db runs on PHPLite, and contains all of the information that is entered into the system by the user. Here is a rundown of each database within the .db document - the entire directory can be found by clicking on the preview link provided by the database.db file in CS50's VSCode:
            event_availability: logs all the data on each user's availability for an event that they join, with each entry under the date and time columns representing a specific timeslot on a specific day that the user (user_id) is available for a certain event (event_id)

            location_availability: logs all the data on each user's availability for an event that they join, with each entry under the location column representing a specific location (location) that the user (user_id) is available for a certain event (event_id); very similar structure to event_availability

            event_dates: logs all the dates included for an event when created, with each entry referring to a specific date (date) and the event it corresponds to (event_id)

            event_locations: logs all the locations included for an event when created, with each entry referring to a specific location (location) and the event it corresponds to (event_id); similar structure to event_dates

            events: contains other data about events when created, with each entry referring to a unique event name (event_name) with a unique event_id and records of the user who made it (event_creator_id), as well as the start_time and end_time

            hours_24: logs all of the hours available for an event to run in, later used in a helper function in app.py that essentially calculates time differences and makes it easier for the program to run based on times entered

            users: standard user database, logs unique username and password (hashed) whenever a user registers for an account

        helpers.py refers to other helper functions to ensure that Flask runs smoothly in app.py. This is pulled from the Finance PSet.

    Part C. Sub-folders
        There are various sub-folders that the app.py calls upon for help; __pycache__ and flask_session are just helper folders containing files to make sure that Flask runs and data is saved.

        The pics sub-folder contains any relevant pictures to the program, but for now is mostly unused; the logo of When2Eat references a picture uploaded to a public picture hosting website, although the logo is original (created by us). 

        The static sub-folder contains all of the CSS code, or documents meant to prettify the website; styles.css is the main sheet used to prettify the pages.

        The templates sub-folder contains all of the HTML code, or display/formatting for each page that calls on variables defined from app.py. Here is an explanation of each one:

            account.html: displays the home page of the website, which are account details. Here, one can delete events that they have joined, change their password, and view events that they have joined and created. NOTE: 

            apology.html: the error page that appears whenever a user submits an incomplete form or does something wrong

            create.html: displays the page for creating an event, including all of the input boxes for event details

            delete.html: 

SECTION 3. Additional Notes
This is in bullet point format, as they refer to parts of the code here and there:
- app.py: All of the program's errors are coded in this file in the format of an apology page being returned (similar to the one from Finance) with the reason for the failure. Hence, the user must refresh/go back to the original page and then re-enter their information while fixing the error in order to bypass the page.



