# SUGO Cycling Club Web App

## Project Overview

SUGO is a web application for a cycling club that allows members to discover rides, join events, interact with other members, and manage their membership.

The project is being built as a **full-stack portfolio project** using **Django, PostgreSQL, and Bootstrap** to demonstrate backend, database, and frontend development skills relevant for junior developer roles.

---

# Tech Stack

## Backend
- Python
- Django
- PostgreSQL

## Frontend
- HTML
- CSS
- Bootstrap
- Django Templates

## Tools
- Git / GitHub
- GPX files for route data
- Mermaid diagrams for ERD documentation

---

# Core Features Implemented

## Authentication
Users can:

- Register
- Login
- Logout

The project uses **Django's built-in authentication system**.

---

## Rides

Users can:

- View a **list of rides**
- View **ride details**

Ride information includes:

- Title
- Description
- Date
- Location
- Creator

Future rides may include **GPX route files**.

---

## Attendance

Users can:

- Join rides
- Leave rides

Attendance records are stored in a join table between users and rides.

---

# Database Structure

## USER
Uses Django's built-in User model.

---

## MEMBERSHIP

Stores club membership status.

Fields include:

- membership_type
- expiry_date
- status

Relationship:

User → Membership (One-to-One)

---

## RIDE

Represents a cycling event.

Fields include:

- title
- description
- date
- location
- created_by
- gpx_file (planned)

Relationships:

- User → Ride (creator)
- Ride → Attendance
- Ride → Comment
- Ride → Notification

---

## ATTENDANCE

Tracks which users join rides.

Fields include:

- user
- ride
- joined_at

Relationship:

User ↔ Ride (Many-to-Many through Attendance)

---

## COMMENT (planned)

Users can comment on rides.

Fields:

- user
- ride
- content
- created_at

---

## NOTIFICATION (planned)

Users receive notifications about relevant events.

Examples:

- New ride created
- Ride update
- New comment
- Membership expiry reminder

Fields:

- user
- message
- related_ride
- read_status
- created_at

---

# Core Pages

## Home

Landing page showing:

- Club introduction
- Upcoming rides
- Navigation to ride list

---

## Ride List

Displays all rides.

Users can:

- Browse rides
- Click to view ride details

---

## Ride Detail

Displays:

- Ride description
- Date/time
- Location
- Attendees
- Comments
- Join/Leave ride button
- GPX route (planned)

---

## User Dashboard (planned)

Personal user area displaying:

- Membership status
- Joined rides
- Notifications
- Renewal options

---

# Features Currently In Development

## Notifications System

Users will receive notifications when:

- A ride they joined is updated
- Someone comments on a ride
- A new ride is created
- Membership is expiring

---

# Future Features

## Ride Comments
Users will be able to comment on ride pages.

---

## GPX Route Support

Rides will support GPX files.

Planned functionality:

- Upload GPX file
- Display route map
- Extract ride statistics
  - Distance
  - Elevation gain
- GPX download option

---

# Project Goals

The project aims to demonstrate:

- Django backend architecture
- relational database design
- authentication systems
- event participation features
- file upload and processing (GPX)
- frontend UI with Bootstrap
- complete full-stack feature implementation