# Crossfit Crossfader

Crossfit Crossfader is a web app that allows you to build playlists that jump in and out of songs at just the right time.   

It's a learning project for me.  I wanted to learn about building apps with Flask, Bootstrap, OAuth 2.0, and Elastic Beanstalk.

At the time of this typing, it needs a lot of cleaning up, but I'm planning on getting it to just good enough and then pull requests are welcome.

## Installation

This is a python project so you'll need that, and the package manager [pip](https://pip.pypa.io/en/stable/) to install Crossfit Crossfader.

In your project directory, start up a virtual environment with:

(Windows)
```bash
python -m venv venv

venv\Scripts\activate
```

(Linux)
```bash
python3 -m venv venv

source venv/bin/activate
```

The install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Start the server using this:
```bash
python webapp.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


Crossfit Crossfade for Spotify

This is another learning project for me.  The goal being to create a spotify playlist with custom song entrances and exits for a workout.

The main things I want to learn are Oath 2.0 authorizations with tokens, relearn Flask for small web apps, AWS for hosting flask apps, and finally commit to venv virtual enviroments.

## Roadmap and Goals

Host on Elastic Beanstalk or other PaaS rather than Lightsail.

Clean away CRUD portions (different branch?)

Multiple Playlists

Threaded or some version that doesn't use sleep()

## Diary and Misc Notes

2/15/21 - Using this as well https://medium.com/technest/build-a-crud-app-with-flask-bootstrap-heroku-60dfa3a788e8

This is helping how bootstrap works: https://getbootstrap.com/docs/3.4/css/

2/14/21 - We've got basic authorizaiton and the spotify API working from their excellent documentation.  Time to start on the Flask App.  We're revisiting this guy https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world to get us off the ground.

# Misc Info
We're hosting it in /srv/www

# Migrating Works Like This
(Source Machine) pip freeze > requirements.txt
Copy requirements.txt to Target Machine
(Target Machine Venv) pip install -r requirements.txt

# Vestigal Notes about CRUD Stuff
This was great, but just not really related to what we're doing.  Come back when you're wanting to learn more about SQL Alchemy, SQLLite, and the like.
https://medium.com/technest/build-a-crud-app-with-flask-bootstrap-heroku-60dfa3a788e8



