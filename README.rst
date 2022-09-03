Here is the repository powering the backend of getimmi.app. If you were redirected here from the website,
you can refer to opt/views.py to see how your data is handled. You will see that all the personal information
is only used to fill in the form and its not stored anywhere.

Instructions for setting up the backend:

1. Clone the repo

2. cd into repo folder and create a virtualenv using "python3 -m venv env"

3. Activate venv. "source env/bin/activate"-

4. Install all dependencies. "pip install -r requirements.txt"

5. Run django server. "python manage.py runserver"

6. Profit. $$$

Note: To push to heroku, use "git push heroku master"