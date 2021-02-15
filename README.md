Crossfit Crossfade for Spotify

This is another learning project for me.  The goal being to create a spotify playlist with custom song entrances and exits for a workout.

The main things I want to learn are Oath 2.0 authorizations with tokens, relearn Flask for small web apps, AWS for hosting flask apps, and finally commit to venv virtual enviroments.

Diary:

2/15/21 - Using this as well https://medium.com/technest/build-a-crud-app-with-flask-bootstrap-heroku-60dfa3a788e8

This is helping how bootstrap works: https://getbootstrap.com/docs/3.4/css/

2/14/21 - We've got basic authorizaiton and the spotify API working from their excellent documentation.  Time to start on the Flask App.  We're revisiting this guy https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world to get us off the ground.




Install and Dependencies

cd /d G:\My Drive\Repos\SpotifyCustomCrossfade\

python -m venv venv

(using Windows)
venv\Scripts\activate

(using Linux)
source venv/bin/activate

# Doing this to enable storing of environmental variables via .flaskenv
pip install python-dotenv

# If you didn't store the enviromental variable in .flaskenv, you can set it with these.
(using Windows)
set FLASK_APP=webapp.py

(using Linux)
export FLASK_APP=webapp.py

# Installing Dependencies
pip install -r requirements.txt

# Start server
flask run
(currently running on http://127.0.0.1:5000/)

# To create the database (run these commands from in the app directory)
python
>>> from app import db
>>> db.create_all()

# To move to a different machine, use these steps
(Source Machine) pip freeze > requirements.txt
Copy requirements.txt to Target Machine
(Target Machine Venv) pip install -r requirements.txt
