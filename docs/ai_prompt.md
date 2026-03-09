Project: SUGO Cycling Club Web App

Stack:
- Django
- Python
- PostgreSQL
- Bootstrap
- Django Templates

Purpose:
Full-stack portfolio project for a cycling club platform.

Current Features:
- User authentication (register/login/logout)
- Ride list page
- Ride detail page
- Ride attendance (join/leave rides)

Database:
User → Membership (1:1)
User → Ride (creator)
User ↔ Ride via Attendance
Ride → Comment (planned)
Ride → Notification (planned)

Next Feature:
Notifications system.

Future Features:
- Comments on rides
- User dashboard with membership info
- GPX upload + route visualisation
- GPX data extraction (distance, elevation)
- GPX download