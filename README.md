# mantas

Full description: http://asimaitis.lt/?app=mantas
Test app on: http://www.asimaitis.lt/mantas

*Description:

A website for organizing and dividing bills for groups. App was named after my brother Mantas who was briliant with numbers since childhood.

*Features:

Create/join groups
You can create and join groups (up to 7) where any member can add bills
Balance
At the bottom of the page you see your full balance including how much you owe, how much is owed to you and your final balance

*Files' tree:

./main.py - main script, used to launch the back-end server

./website/__init__.py - script for initializing Flask application and database

./website/models.py - used for creating SQLAlchemy models

./website/balance.py - script for counting user's balance

./website/auth.py - script for receiving requests and sending responses for registration/login

./website/views.py - script for rendering Flask pages and handling HTTP requests

./website/static/ - folder for front-end files as CSS and images

./website/templates/ - folder for templates for rendering HTML pages
