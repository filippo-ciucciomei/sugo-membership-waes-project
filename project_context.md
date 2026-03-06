Project Context — SUGO Cycling Club
==================================

Purpose
-------
SUGO is a cycling club platform where members can organise rides, join rides, and discuss ride details.

Only users with an active membership can access ride features.


Core features
-------------

Users can:

- register
- login
- purchase membership
- view rides
- create rides
- join rides
- comment on rides
- receive notifications


Technology Stack
----------------

Backend

Python  
Django  
PostgreSQL

Frontend

Bootstrap 5  
FontAwesome icons  
Minimal JavaScript

Future features

Leaflet.js (map rendering)  
Chart.js (elevation profile)


Database Schema
---------------

USER
----

user_id (PK) int  
username varchar  
email varchar  
is_admin boolean


MEMBERSHIP
----------

member_id (PK) int  
user_id (FK → USER.user_id)  
start_date datetime  
renew_date datetime NULL 
price float


RIDE
----

ride_id (PK) int  
user_id (FK → USER.user_id)  

title varchar  
description text  
date datetime  
time datetime
max_riders int  
gpx_file file  
distance float  
elevation float  
pace int  
discipline varchar  


ATTENDANCE
----------

id (PK) int  
user_id (FK → USER.user_id)  
ride_id (FK → RIDE.ride_id)  


COMMENT
-------

comment_id (PK) int  
user_id (FK → USER.user_id)  
ride_id (FK → RIDE.ride_id)  

content text  
created_at datetime


Relationships
-------------

User creates many rides

User joins many rides through Attendance

Ride has many comments

Ride has many participants through Attendance

User has one membership


Pages
-----

Home page

Rides list

Ride detail


Home Page
---------

Visible to everyone.

Contains:

- SUGO logo
- short description
- join button

Join button opens login/signup modal.


Rides Page
----------

Members-only page.

If user is not authenticated:

page is greyed out  
login/signup modal shown


If user is logged in but not active member:

redirect to membership purchase page


If user is active member:

display ride list.


Ride List
---------

Vertical list of ride cards.

Sorting:

nearest ride date first  
oldest ride at bottom


Ride card shows:

title  
ride date  
discipline  
short description  
joined count  
comment count


Floating button:

"+ New Ride"


Button is fixed position.

Must never overlap footer.


Ride Creation
-------------

Ride creation happens in a modal.

Fields:

title  
description  
date_time  
discipline  
max_riders  
gpx file upload


GPX file processing:

distance calculation  
elevation gain  
route coordinates


Ride Detail Page
----------------

Shows:

title  
date  
discipline  
distance  
elevation  
pace  
participants list


Users can:

join ride  
leave ride  
comment


Ride creator can:

edit ride  
delete ride


Comments
--------

Displayed chronologically.

Users can:

create comment  
edit own comment  
delete own comment


Attendance
----------

User can join ride if:

ride is not full  
user not already attending


Unique constraint:

user_id + ride_id



Membership
----------

Users must have an active membership to access rides.

Membership duration:

1 year


Payment provider:

Stripe


Stripe flow:

checkout session  
success webhook  
membership created  
expiry date set


Future Features
---------------

Map rendering with Leaflet.js

Elevation chart with Chart.js

GPX visualisation

Notifications

Membership renwal


Project Structure
-----------------

sugo_project/

manage.py

sugo_project/
    settings.py
    urls.py
    wsgi.py

apps/

users/
rides/
membership/


templates/

base.html
home.html
rides_list.html
ride_detail.html


static/

css/
js/
images/


Deployment
----------

Gunicorn  
WhiteNoise  
PostgreSQL


Environment variables

SECRET_KEY  
DATABASE_URL  
STRIPE_SECRET_KEY