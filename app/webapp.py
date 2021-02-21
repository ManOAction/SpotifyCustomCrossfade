from flask import Flask, render_template, request, redirect, make_response, session, flash
from urllib.parse import urlencode
import threading

# Custom Imports
from CustomCrossfade import CustomCrossfade

app = Flask(__name__)

app.secret_key = 'nIe8c&Z*coP!DKm2gqZf' # Messing around with flash messaging.

application = app # For beanstalk, officially fucking stupid.  Never used elsewhere.

HostDomain = 'http://127.0.0.1:5000'

# 'http://www.crossfitcrossfader.com'


# Home Route
############################################################################
@app.route('/')
def index():
    
        return render_template('index.html', title='Crossfit Crossfader Home')


def player(ListId):    

    ListId -= 1    

    flash(f'Player loop beginning for Playlist {CustomCrossfade.Playlists[ListId][0]}.')

    render_template('crossfade.html', title='Crossfit Crossfader Home')    

    for Song in CustomCrossfade.Playlists[ListId][1]:
        print('Adding a song to up next.')
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
        CustomCrossfade.AddSongToQueue(Song[0], session.get('token', 'not set'))
        print('Song Added')

    print('Skipping to next song.')
    session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
    CustomCrossfade.SkipToNextSong(session.get('token', 'not set'))

    for Song in CustomCrossfade.Playlists[ListId][1]:
        if int(Song[1]) > 0:
            print(f'Skipping to {Song[1]}')
            session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
            CustomCrossfade.SeekToTime(Song[1], session.get('token', 'not set'))    
        print(f'Sleeping for {Song[2]}')
        CustomCrossfade.sleep(int(Song[2]))
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
        CustomCrossfade.SkipToNextSong(session.get('token', 'not set'))

    print('Bottom of player function.')

    return True



# Playlist Maker Routes
###########################################################################

@app.route('/freqhits') # , methods=['GET', 'POST'])
def freqhits():

    return render_template('freqhits.html', title='Frequency Hits Playlist Maker')


# Crossfrade Routes
###########################################################################

@app.route('/flashtest')
def flashtest():
    flash('You\'ve been flashed.')

    return redirect('/')


@app.route('/crossfade')
def crossfade():

    return render_template('crossfade.html', title='Crossfit Crossfader Home')


@app.route('/playlistplay/<int:ListId>')
def playlistplay(ListId):    
    
    try:
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))    
    
    except Exception as errmsg:
        print(errmsg)        
        flash('We need to get you authorized.')
        return redirect('/crossfade/authorize')

    # x = threading.Thread(target=player, args=(ListId,)) 
    # x.start()       
    
    player(ListId)

    return redirect('/crossfade')


@app.route('/crossfade/authorize')
def authorize():
    client_id = CustomCrossfade.clientId
    redirect_uri = f'{HostDomain}/crossfade/callback/'    
    scope = 'user-read-private user-read-email user-modify-playback-state'

    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    params = {'response_type': 'code', 'client_id': client_id,
            'redirect_uri': redirect_uri, 'scope' : scope 
                }
    query_params = urlencode(params)
    # print(authorize_url + query_params)
    response = make_response(redirect(authorize_url + query_params))    
    return response

@app.route("/crossfade/callback/")
def get_data():
    session['code'] = request.args.get("code")

    redirect_uri = f'{HostDomain}/crossfade/callback/'

    response = CustomCrossfade.GetTokensFromCode(CustomCrossfade.authStr, session['code'], redirect_uri)
    print(response.status_code)
    print(response.content)


    session['token'] = response.json()['access_token']
    session['refreshtoken'] = response.json()['refresh_token']

    flash('You\'ve been reauthorized.')
    flash('Select a playlist now.')

    return redirect('/crossfade')


# Starting the App
##########################################################
if __name__ == "__main__":
    app.debug = False
    app.run()