# WHEN2EAT: USER'S MANUAL
Made by: Nadine Han and Julianna Zhao

Class: CS50 Fall 2021
 
Table of Contents
0: Preface
1: Running the Application
 
SECTION 0. Preface
This project is titled When2Eat, and is a spinoff of When2Meet, a website that allows users to coordinate meeting times by creating events and having participants indicate their availabilities in order to determine the best meeting time. In this document, we will discuss the main functions of each document, as well as what role they play in the overall program.

You can find our Youtube video going over the same information at: https://youtu.be/rW-PQt81LeM

#### <b>VERY IMPORTANT NOTE:</b> The program is meant to be run in the CS50 VSCode compiler! Running it elsewhere will lead to problems, as the main program app.py relies on Flask, which uses functions imported from the cs50 library.
 
SECTION 1. Running the Application
   Part A. Startup
       To run the application:
       1. Upload the entire csfinal folder to a codespace for running/compiling
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
       A: Once you have clicked on "Register", simply enter in any login information you want to make to test it out. Then, click the "Register" button at the bottom to submit your information. If the registration was successful, you should then be redirected to the Log In page. (Keep in mind that you cannot have a duplicate username, meaning that if you try to register with a username that already exists, you will throw an error!)
 
       Q: Once I log in, how can I navigate around?
       A: Utilize the navigation bar, which is the strip at the top of the website. It includes the Homepage/Account link (click on the logo, the options to Create/Join an event, and the option to Log Out. Other functions, like viewing events you have already joined, deleting them, and/or changing your password, can be done on the Homepage/Account page.
 
       Q: How can I create an event?
       A: In the navigation bar, click on “Create Event”. You should then be redirected to a page with relevant information on creating an event - fill it out, making sure to have at least one Location and to fill out every other field (or you will get an error), and then click the “Confirm” button to create it! Upon creation, you should receive a confirmation message with the code corresponding to the event. This can be entered in Join Event to add one’s scheduling availability.
 
       Q: How can I join an event?
       A: In the navigation bar, click on “Join Event”. You should then be redirected to a page with relevant information on joining an event. Fill it out, making sure to check at least one Location and one timeslot (or you will get an error), and then click the “Confirm” button to create it! Upon creation, you should receive a confirmation message, and be able to view Group Availability.
 
       Q: How can I view events I have already joined or created?
       A: Go to the Account page by clicking on the logo at the top left corner, which will list out links to each event, and click on the event of interest. You will then be redirected to a page that shows the statistics on the event. Note that this CANNOT be edited; if you want to edit the event, you must click on Join Event in the navigation bar and re-enter the event code.
 
       Q: How can I view who is available in the events that I joined or created?
       A: You can view Group Availability by going to your Account Page and clicking on an event. The website will then return the Group Availability for locations and times. There are two buttons on the Group Availability page for further information: “Show When Some Available” “Show When All Available”. Clicking either one will highlight fields in the Time and Location grids in green based on availability.
      
       Q: How can I delete an event that I created?
       A: If you want to delete an event that you created: Navigate to the Account Page and click "Delete Event" under settings. You can then check off the events under "Created Events" that you wish to delete, and click the "Delete" button at the bottom to confirm. This will delete the ENTIRE event!
 
       Q: How can I delete my availability in an event?
       A: If you want to delete your entry in an event that you joined: Navigate to the Account Page and click "Delete Event" under settings. You can check off the events under "Joined Events", and click the "Delete" button at the bottom to confirm. This will delete ONLY YOUR AVAILABILITY ENTRY in an event! (N.B. Since you can join an event that you created, doing these steps on an event that was created by your account will still only delete your availability entry for this event.)