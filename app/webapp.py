from flask import Flask, render_template, request, redirect, make_response, session
from urllib.parse import urlencode

# Custom Imports
from CustomCrossfade import CustomCrossfade

app = Flask(__name__)


application = app # For beanstalk, officially fucking stupid.  Never used elsewhere.


# Home Route
############################################################################
@app.route('/')
def index():
    
        return render_template('index.html', title='Crossfit Crossfader Home')


# Playlist Maker Routes
###########################################################################

@app.route('/freqhits') # , methods=['GET', 'POST'])
def freqhits():

    return render_template('freqhits.html', title='Frequency Hits Playlist Maker')


# Crossfrade Routes
###########################################################################

@app.route('/crossfade')
def crossfade():

    return render_template('crossfade.html', title='Crossfit Crossfader Home')


@app.route('/playlistplay/<int:ListId>')
def playlistplay(ListId):

    x = ListId
    
    try:
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))

    except:
        return redirect('/crossfade/authorize')
    
    for Song in CustomCrossfade.SongList:
        print('Adding a song to up next.')
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
        CustomCrossfade.AddSongToQueue(Song[0], session.get('token', 'not set'))
        print('Song Added')

    print('Skipping to next song.')
    session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
    CustomCrossfade.SkipToNextSong(session.get('token', 'not set'))

    for Song in CustomCrossfade.SongList:
        if int(Song[1]) > 0:
            print(f'Skipping to {Song[1]}')
            session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
            CustomCrossfade.SeekToTime(Song[1], session.get('token', 'not set'))    
        print(f'Sleeping for {Song[2]}')
        CustomCrossfade.sleep(int(Song[2]))
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))
        CustomCrossfade.SkipToNextSong(session.get('token', 'not set'))

    return redirect('/crossfade')


@app.route('/crossfade/authorize')
def authorize():
    client_id = CustomCrossfade.clientId
    redirect_uri = 'http://www.crossfitcrossfader.com/crossfade/callback/'    
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
    session['code'] = request.args.get("code")

    redirect_uri = 'http://www.crossfitcrossfader.com/crossfade/callback/'

    response = CustomCrossfade.GetTokensFromCode(CustomCrossfade.authStr, CustomCrossfade.code, redirect_uri)
    print(response.status_code)
    print(response.content)


    session['token'] = response.json()['access_token']
    session['refreshtoken'] = response.json()['refresh_token']

    return redirect('/crossfade')


# Starting the App
##########################################################
if __name__ == "__main__":
    app.debug = False
    app.run()