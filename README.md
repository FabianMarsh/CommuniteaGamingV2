# CommuniTea Gaming Platform

A community-powered booking and scheduling platform tailored for tabletop gaming and group events. Built with Django and enhanced by FullCalendar, this application offers users a simple, responsive interface to book spaces, view availability, and manage their accounts.

## Overview

CommuniTea is designed to balance functionality with narrative atmosphere. Its modular structure and clear scheduling logic make it ideal for tabletop venues, board game cafés, or similar community hubs.

Features include:
- Interactive weekly calendar with precise time slots
- Role-based user authentication via Django Allauth
- Custom asset integration for thematic clarity
- Responsive styling for multiple screen sizes
- Scalable deployment via Heroku and Gunicorn

Sensitive information such as credentials, API keys, and media sources are handled securely via environment variables and server-side config. No secrets are exposed in this repository.

## Tech Stack

- Django 4.2
- PostgreSQL
- FullCalendar (JS-based frontend calendar)
- SCSS for responsive design
- Django Allauth for login/signup
- Gunicorn for WSGI deployment
- Heroku as hosting provider
- Whitenoise for static asset serving

## Dependencies and Licenses

This project uses open-source packages governed by permissive licenses. Core dependencies include:

| Dependency                | License        |
|--------------------------|----------------|
| Django                   | BSD-3-Clause   |
| django-allauth           | MIT            |
| FullCalendar             | MIT            |
| Gunicorn                 | MIT            |
| Whitenoise               | MIT            |
| dj-database-url          | BSD-3-Clause   |
| OAuthlib / Requests      | BSD / Apache   |
| Pillow                   | PIL License    |
| Meeple SVG Asset         | Attribution noted below if externally sourced |

Refer to `requirements.txt` for the complete list of dependencies.

### Asset Attribution

If the Meeple SVG asset is sourced from a third-party, its use complies with either CC BY 4.0 or the licensing specified by the original creator. Attribution will be provided in documentation or site footer if required.

FullCalendar is maintained by Adam Shaw and licensed under MIT: [https://fullcalendar.io/license](https://fullcalendar.io/license)

## Setup

To run locally:

```bash
git clone https://github.com/your-repo-name/communitea.git
cd communitea
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver