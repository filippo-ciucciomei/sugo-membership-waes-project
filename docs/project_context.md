# SUGO Cycling Club Web App

## Overview

SUGO is a Django full-stack web application for a cycling club.

Members can discover rides, join events, interact with other cyclists, and manage their membership.

The project is being built as a a **portfolio project** to demonstrate backend, database, and frontend skills relevant for junior developer roles.

---

# Tech Stack

Backend
- Python
- Django
- PostgreSQL

Frontend
- HTML
- CSS
- Bootstrap
- Django Templates

Infrastructure
- Heroku deployment
- Stripe payments
- Stripe webhooks

Tools
- Git / GitHub
- Mermaid diagrams for ERD documentation
- GPX files (planned for route data)

---

# Core Features Implemented

## Authentication

Users can:

- Register
- Login
- Logout

The application uses **Django's built-in authentication system**.

---

## Membership System

The application is **membership gated**.

Users must purchase a membership to access rides.

Payment flow:

User signup  
↓  
Redirect to membership purchase page  
↓  
Stripe Embedded Checkout  
↓  
Stripe webhook  
↓  
MembershipPurchase created  
↓  
User gains access to rides  

Membership status is verified using a helper function:

user_has_active_membership(user)

Users without an active membership are redirected to the membership purchase page.

---

## Stripe Integration

Payments are handled using **Stripe Embedded Checkout**.

Architecture:

membership_checkout_page  
↓  
create_checkout_session  
↓  
Stripe Embedded Checkout  
↓  
Stripe webhook  
↓  
MembershipPurchase created  

Webhook endpoint:

/membership/webhook/

Stripe keys are stored in environment variables.

---

## Rides

Users can:

- View a list of rides
- View ride details
- Join rides
- Leave rides

Ride information includes:

- title
- description
- date
- location
- creator

---

## Attendance

Tracks which users joined rides.

Relationship:

User ↔ Ride (through Attendance)

Fields:

- user
- ride
- joined_at

---

## Comments

Users can comment on rides.

Fields:

- user
- ride
- content
- created_at

Comments appear on the ride detail page.

---

# Database Overview

## User

Uses Django's built-in User model.

---

## MembershipPlan

Defines available membership plans.

Fields:

- name
- price
- is_active

---

## MembershipPurchase

Stores membership purchases created by the Stripe webhook.

Fields:

- user
- plan
- price_paid
- created_at
- expiry_date

---

## Ride

Cycling event created by a user.

Fields:

- title
- description
- date
- location
- user (creator)

Relationships:

User → Ride  
Ride → Attendance  
Ride → Comment  
Ride → Notification  

---

## Attendance

Join table between users and rides.

Fields:

- user
- ride
- joined_at

---

## Comment

Ride comments.

Fields:

- user
- ride
- content
- created_at

---

## Notification (in development)

Notifications are stored in the database.

Fields:

- recipient
- actor
- ride
- type
- is_read
- created_at

---

# Notifications System (Current Work)

Notifications are generated when:

- A ride is created
- A user joins a ride
- A user leaves a ride
- A user comments on a ride

Implementation uses **Django signals** so notifications are triggered automatically when model events occur.

---

# Future Features

## User Dashboard

Personal user area showing:

- membership status
- joined rides
- notifications
- membership renewal options

---

## GPX Route Support

Planned functionality:

- upload GPX files
- map route visualisation
- extract route statistics
- GPX download