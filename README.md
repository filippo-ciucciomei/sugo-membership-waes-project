# SUGO Cycling Club

SUGO is a full-stack web application that allows members of a cycling club to organise rides, join events, and share route information with the community. The platform enables users to create rides, upload GPX routes, view route maps, interact through comments, and receive notifications about activity on rides.

The project was built using Django and deployed on Heroku, with AWS S3 used for media storage. It focuses on community-driven ride organisation and clear route visualisation.

INSERT SCREENSHOT HERE!!!

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
10. [Future Improvements](#future-improvements)
11. [Credits](#credits)

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

## Layout

The interface uses a clean layout with:

- centered content columns
- ride cards with route previews
- simple navigation bar
- responsive Bootstrap grid system

INSERT WIREFRAMES HERE!!!

---

## Navigation

The navigation bar includes:

- login / logout
- homepage
- ride list
- user profile menu
- notification dropdown

---

## Ride List Page

Each ride is displayed as a card showing:

- route preview map
- ride title
- date and time
- discipline
- number of riders
- ride creator

Cards are fully clickable for quick navigation.

INSERT SCREENSHOT HERE!!!

---

## Ride Detail Page

The ride detail page displays:

- ride information
- interactive route map
- elevation chart
- GPX download
- comments section

INSERT SCREENSHOT HERE!!!

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

INSERT ERD HERE!!!

---

# Features

## Authentication

Users can:

- register
- log in
- log out

Authentication is handled using Django authentication.

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

# Testing

Testing was performed throughout development to ensure the application behaves as expected.

Testing included:

- manual feature testing
- user flow testing
- database integrity checks
- form validation testing
- deployment testing

INSERT TESTING TABLE HERE!!!

---

# Deployment

The project is deployed on Heroku.

## Deployment Steps

1. Create a Heroku application.
2. Configure environment variables.
3. Connect the GitHub repository.
4. Configure PostgreSQL database.
5. Configure AWS S3 for media storage.
6. Run migrations.
7. Deploy the application.

INSERT DEPLOYMENT SCREENSHOT HERE!!!

---

# Future Improvements

Potential future features include:

- user profiles
- ride difficulty ratings
- rider avatars
- route filtering
- ride search
- calendar view
- mobile UI improvements
- push notifications
- improved GPX analytics

---

# Credits

## Libraries and Tools

- Django
- Bootstrap
- Leaflet
- Chart.js

## Inspiration

Cycling community platforms and ride organisation tools.

---

# Acknowledgements

Thanks to the cycling community and open-source tools that made this project possible.