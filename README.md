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
[MIT License ](https://choosealicense.com/licenses/mit/)
A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.


# Roadmap and Goals

Add playlist maker

Clean up project structure (maybe rename to application for beanstalk)

Add user created playlists?

Bring Back CRUD to store user playlists (maybe loaded by csv)


## Done Recently
2/21 - Threaded or some version that doesn't use sleep()
2/20 - Multiple Playlists
2/16 - Security update and session tokens
2/16 - Unnecessary bootstrap facelift
2/15 - Clean away CRUD portions (different branch?)
2/15 - Host on Elastic Beanstalk or other PaaS rather than Lightsail.



## Diary and Misc Notes

2/24 - Might finish the playlist maker and then put this down for a while.

2/20/21 - Finally got threadded playing of playlists up and going.  Quick bootstrap skin.  Time to start working on multiple playlists and playlist uploading.
  We're using this for variable control in the href of the templates  
  ```html
  <a href="{{ '/view_assessment_result/%s'%a.id|urlencode }}">{{ a.id }}</a>
  ```

2/15/21 - Using this as well https://medium.com/technest/build-a-crud-app-with-flask-bootstrap-heroku-60dfa3a788e8

This is helping how bootstrap works: https://getbootstrap.com/docs/3.4/css/

2/14/21 - We've got basic authorizaiton and the spotify API working from their excellent documentation.  Time to start on the Flask App.  We're revisiting this guy https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world to get us off the ground.

## Migrating Works Like This
(Source Machine) pip freeze > requirements.txt
Copy requirements.txt to Target Machine
(Target Machine Venv) pip install -r requirements.txt

## Vestigal Notes about CRUD Stuff
This was great, but just not really related to what we're doing.  Come back when you're wanting to learn more about SQL Alchemy, SQLLite, and the like.
https://medium.com/technest/build-a-crud-app-with-flask-bootstrap-heroku-60dfa3a788e8



