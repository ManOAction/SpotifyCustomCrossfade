from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from urllib.parse import urlencode

# Custom Imports
from CustomCrossfade import CustomCrossfade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name

# Home Route
############################################################################
@app.route('/')
def index():
    
        return render_template('index.html', title='WebApp Home')


# CRUD Routes
###########################################################################

@app.route('/crud/', methods=['GET', 'POST'])
def crudhome():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Grocery(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/crud/')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('crudhome.html', groceries=groceries, title='CRUD Home')

@app.route('/crud/delete/<int:id>')
def delete(id):
    grocery = Grocery.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/crud/')
    except:
        return "There was a problem deleting data."


@app.route('/hello')
def hello():    
    return render_template('index.html', title='Hello Style Title')



# Crossfrade Routes
###########################################################################

@app.route('/crossfade')
def crossfade():

    return render_template('crossfade.html', title='Crossfit Crossfader Home')


@app.route('/playlistplay/<int:ListId>')
def playlistplay(ListId):

    x = ListId

    token = CustomCrossfade.token
    refreshtoken = CustomCrossfade.refreshtoken

    try:
        token = CustomCrossfade.GetNewAccessToken(refreshtoken)

    except:
        return redirect('/crossfade/authorize')

    render_template('crossfade_playing.html', title='Crossfit Crossfader Home')

    for Song in CustomCrossfade.SongList:
        print('Adding a song to up next.')
        token = CustomCrossfade.GetNewAccessToken(refreshtoken)
        CustomCrossfade.AddSongToQueue(Song[0], token)
        print('Song Added')

    print('Skipping to next song.')
    token = CustomCrossfade.GetNewAccessToken(refreshtoken)
    CustomCrossfade.SkipToNextSong(token)

    for Song in CustomCrossfade.SongList:
        if int(Song[1]) > 0:
            print(f'Skipping to {Song[1]}')
            token = CustomCrossfade.GetNewAccessToken(refreshtoken)
            CustomCrossfade.SeekToTime(Song[1], token)    
        print(f'Sleeping for {Song[2]}')
        CustomCrossfade.sleep(int(Song[2]))
        token = CustomCrossfade.GetNewAccessToken(refreshtoken)
        CustomCrossfade.SkipToNextSong(token)

    return redirect('/crossfade')


@app.route('/crossfade/authorize')
def authorize():
    client_id = CustomCrossfade.clientId
    redirect_uri = 'http://127.0.0.1:5000/crossfade/callback/'    
    scope = 'user-read-private user-read-email user-modify-playback-state'

    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    params = {'response_type': 'code', 'client_id': client_id,
            'redirect_uri': redirect_uri, 'scope' : scope 
                }
    query_params = urlencode(params)
    print(authorize_url + query_params)
    response = make_response(redirect(authorize_url + query_params))
    return response

@app.route("/crossfade/callback/")
def get_data():
    CustomCrossfade.code = request.args.get("code")

    redirect_uri = 'http://127.0.0.1:5000/crossfade/callback/'

    response = CustomCrossfade.GetTokensFromCode(CustomCrossfade.authStr, CustomCrossfade.code, redirect_uri)
    print(response.status_code)
    print(response.content)


    CustomCrossfade.token = response.json()['access_token']
    CustomCrossfade.refreshtoken = response.json()['refresh_token']

    return redirect('/crossfade')