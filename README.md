# SUGO Cycling Club

🚴 **Live Application:**  
https://YOUR-APP.herokuapp.com

SUGO is a full-stack web application that allows members of a cycling club to organise rides, join events, and share route information with the community. The platform enables users to create rides, upload GPX routes, view route maps, interact through comments, and receive notifications about activity on rides.

The project was built using Django and deployed on Heroku, with AWS S3 used for media storage. It focuses on community-driven ride organisation and clear route visualisation.

### Homepage Mockup
![Home Mockup](readme-files/mockups/home%20mockup.png)

### Ride Page Mockup
![Ride Mockup](readme-files/mockups/ride%20mockup.png)

---

---

# Table of Contents

1. [Project Overview](#project-overview)  
2. [User Experience (UX)](#user-experience)  
3. [User Stories](#user-stories)  
4. [Design](#design)  
5. [Database Design](#database-design)  
6. [Features](#features)  
7. [Technologies Used](#technologies-used)  
8. [Testing](#testing)  
9. [Deployment](#deployment)  
10. [Challenges Faced](#challenges-faced)  
11. [Future Improvements](#future-improvements)  
12. [Ai Usage](#ai-usage)
12. [Credits](#credits)

---

# Project Overview

SUGO Cycling Club provides a digital platform for organising and sharing cycling rides within a community.

Users can:

- create rides with route information
- join or leave rides
- upload GPX route files
- visualise routes on an interactive map
- view ride statistics (distance and elevation)
- comment on rides
- receive notifications when activity occurs

The platform aims to make group ride organisation simple and transparent while allowing members to easily visualise routes before joining.

---

# User Experience

The goal of the application is to provide a clear and intuitive interface where cyclists can quickly:

- browse upcoming rides
- view route details
- decide whether to join
- interact with other riders

Key design goals:

- simple navigation
- clear ride information
- visual route preview
- responsive design for mobile and desktop
- lightweight and fast interface

---

# User Stories

## Visitor

- As a visitor I can view the homepage so that I understand what the club does.
- As a visitor I can register for an account so that I can join rides.
- As a visitor I can log in and log out securely.

## Member

- As a member I can view upcoming rides so that I can choose which rides to attend.
- As a member I can view ride details so that I can see the route and ride information.
- As a member I can join a ride so that I can participate in the event.
- As a member I can leave a ride if my plans change.
- As a member I can comment on rides so that I can interact with other riders.
- As a member I can upload a GPX route when creating a ride.

## Ride Creator

- As a ride creator I can create rides so that others can join.
- As a ride creator I can edit my ride if details change.
- As a ride creator I can delete my ride if necessary.

## Notifications

- As a member I receive notifications when users join, leave, or comment on a ride so that I stay informed.

---

# Design

## Wireframes

Wireframes were created to plan the responsive layout of the application before development.

### Laptop
![Laptop Wireframes](readme-files/wireframes/Wireframes%20Laptop.png)

### Tablet
![Tablet Wireframes](readme-files/wireframes/Wireframes%20Tablet.png)

### Mobile
![Mobile Wireframes](readme-files/wireframes/Wireframes%20Mobile.png)

---

## Navigation

The navigation bar includes:

- login / logout
- homepage
- ride list
- user profile menu
- notification dropdown

---

# Database Design

The application uses a relational database designed to support ride management and user interaction.

Core models include:

### User
Stores user authentication and profile data.

### Ride
Stores ride information including:

- title
- description
- date
- time
- discipline
- GPX file
- maximum riders

### Attendance
Links users to rides they have joined.

### Comment
Allows users to comment on rides.

### Notification
Stores activity notifications related to rides.

---

# Features

## Authentication

Users can:

- register
- log in
- log out

Authentication is handled using Django authentication and social login through Google and Strava.

---

## Ride Creation

Users can create rides with:

- title
- description
- date
- time
- discipline
- maximum riders
- GPX route file

---

## GPX Route Visualisation

Routes uploaded as GPX files are parsed and displayed on an interactive map.

Features include:

- route polyline
- start and finish markers
- distance calculation
- elevation gain calculation
- elevation profile chart

Libraries used include **Leaflet.js** and **Chart.js**.

---

## Ride Participation

Members can:

- join rides
- leave rides
- see current rider count

---

## Comments

Users can leave comments on rides to communicate with other riders.

---

## Notifications

Members receive notifications when:

- someone joins a ride
- someone leaves a ride
- someone comments on a ride
- a new ride is created

Notifications appear in a dropdown menu in the navigation bar.

---

# Technologies Used

## Backend

- Python
- Django
- PostgreSQL

## Frontend

- HTML
- CSS
- Bootstrap
- JavaScript

## Maps and Data

- Leaflet.js
- GPX parsing
- Chart.js

## Storage

- AWS S3 for media files

## Deployment

- Heroku

---

# Automated Backend Testing (Python / Django)

Automated tests were implemented using Django’s built-in testing framework. These tests simulate user interactions and verify that views, models, and database operations behave correctly.

The Django test suite was executed using the following command:

`python manage.py test`

This command automatically:

- creates a temporary test database
- runs all test cases
- destroys the test database after completion

This ensures tests do not affect the production or development database.

---

## Ride View Tests

Ride view tests verify that ride pages render correctly and that authenticated users can interact with rides.

These tests confirm that:

- the ride detail page loads successfully
- ride information appears correctly
- the comment form is displayed
- logged-in users can submit comments
- comments are correctly stored in the database

Example of the test implementation:

![Python Test Code](readme-files/tests/python%20tests%20doc.png)

This test simulates the following behaviour:

1. A test user is created.
2. A membership plan and membership purchase are created.
3. A ride is created.
4. The test client logs in the user.
5. A POST request is sent to submit a comment.
6. The test verifies the comment was saved successfully.

---

## Python Test Execution

The following screenshot shows the successful execution of the Django test suite.

All tests passed successfully.

![Python Test Results](readme-files/tests/python%20tests.png)

# HTML Validation

HTML markup was validated using the **W3C Nu HTML Checker**.

Validator link:  
https://validator.w3.org/nu/

Because Django templates contain template tags (`{% %}` and `{{ }}`), validation was performed on the **rendered HTML output** in the browser rather than the raw template files.

This ensures the final HTML delivered to users is standards-compliant.

---

## Home Page Validation

Validator used:  
https://validator.w3.org/nu/

![Home HTML Validation](readme-files/tests/home%20html%20validator.png)

Result:  
No errors or warnings were found.

---

## Ride List Page Validation

Validator used:  
https://validator.w3.org/nu/

![Ride List HTML Validation](readme-files/tests/ride%20list%20html%20validator.png)

Result:  
The page validated successfully with no structural HTML errors.

---

## Ride Detail Page Validation

Validator used:  
https://validator.w3.org/nu/

![Ride Details HTML Validation](readme-files/tests/ride%20details%20html%20validator.png)

Result:  
The ride detail page also validated successfully with no errors.

---

# CSS Validation

CSS stylesheets were validated using the **W3C CSS Validator**.

Validator link:  
https://jigsaw.w3.org/css-validator/

The validator confirmed that the stylesheet contains no syntax errors and complies with **CSS Level 3 + SVG** standards.

![CSS Validation](readme-files/tests/css%20validator.png)


Result:  
No CSS errors were found.


# Challenges Faced

During development several technical challenges were encountered. These challenges required debugging, research, and adjustments to both the application code and configuration.

---

## Google OAuth Security Warning

One of the main challenges encountered was related to **Google OAuth authentication**.

The application uses **django-allauth** to allow users to sign in using their Google account. While the implementation was technically correct and the authentication flow worked as expected, Google initially flagged the application as **"suspicious"** during the OAuth verification process.

This warning appeared because Google's automated security checks interpreted the wording on the login page as potentially misleading, even though the code itself was functioning correctly.

### Resolution

To resolve the issue:

- The login page text was rewritten to clearly explain that users would be redirected to **Google's official authentication page**.
- The wording was simplified to avoid triggering automated security filters.
- A verification request was submitted through Google's OAuth review process.

After these changes, the application passed the review and the warning was removed.

---

## Static Files and Deployment Differences

Another challenge occurred when running tests locally while using **Whitenoise static file storage**.

The project uses **CompressedManifestStaticFilesStorage** in production, which expects all static assets to exist in the collected static files manifest. During automated testing, Django attempted to load certain static assets that were not included in the manifest, causing errors.

### Resolution

The issue was solved by overriding the static file storage configuration in the test settings so that Django uses the standard static file storage during testing.

This allowed the test environment to run without requiring the full static file manifest used in production.

---

## Test Database Behaviour

When writing automated tests, it was important to understand how Django handles test databases.

Running the test suite automatically:

- creates a temporary database
- runs all test cases
- deletes the database afterwards

This behaviour ensures tests are **isolated and do not affect the real database**, but required careful setup of test data within the `setUp()` method to ensure all required objects existed before each test ran.


# Future Improvements

While the current version of the application provides the core functionality required to organise and manage club rides, several additional features could further enhance the user experience and expand the platform.

Potential future improvements include:

### User Profiles
Allow users to create a personal profile including:

- profile picture
- cycling preferences
- short bio
- personal ride statistics

This would help strengthen the community aspect of the platform.

---

### Ride Difficulty Rating

Introduce a difficulty rating system for rides based on factors such as:

- distance
- elevation gain
- average speed

This would help riders quickly understand whether a ride suits their level.

---

### Advanced Ride Filtering

Add filtering options on the ride list page to allow users to filter rides by:

- discipline (road / gravel)
- distance
- elevation
- date

This would make it easier for members to find rides that match their preferences.

---

### Calendar Integration

Provide a calendar view of upcoming rides and allow users to export rides to external calendars such as:

- Google Calendar
- Apple Calendar
- Outlook

---

### Improved Notification System

Enhance the notification system with:

- read/unread indicators
- email notifications
- real-time updates using WebSockets

---

### Enhanced GPX Analytics

Extend GPX data analysis to include:

- average gradient
- climb detection
- estimated ride duration
- ride difficulty calculation

---

# AI Usage

Artificial intelligence tools were used during the development of this project to assist with learning, debugging, and documentation.

AI assistance was used for:

- understanding Django testing practices
- troubleshooting errors during development
- generating ideas for application architecture
- improving documentation clarity
- refining README structure and explanations

All code generated with the assistance of AI was reviewed, tested, and adapted to fit the requirements of the project.

AI tools were used as a **learning aid and productivity tool**, while the final implementation and debugging decisions were made by the developer.

---

# Credits

## Technologies and Libraries

The following technologies and open-source libraries were used in the development of this project:

- **Django** – backend web framework
- **Bootstrap** – responsive frontend layout
- **Leaflet.js** – interactive maps
- **Chart.js** – elevation chart visualisation
- **django-allauth** – authentication and social login
- **PostgreSQL** – relational database
- **AWS S3** – media file storage
- **Heroku** – application deployment platform

---

## Development Tools

- **Visual Studio Code** – development environment
- **Git & GitHub** – version control
- **W3C Validators** – HTML and CSS validation
- **Google Lighthouse** – performance and accessibility testing

---


This project was developed by **Filippo Ciucciomei** as part of the Codeinstitute full-stack web development Bootcamp. Inspiration was drawn from real-world cycling club organisation platforms and community ride management tools.

Special thanks to the open-source community and documentation resources that made this project possible.


