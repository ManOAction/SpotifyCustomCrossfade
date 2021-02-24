from flask import Flask, render_template, request, redirect, make_response, session, flash, copy_current_request_context
from urllib.parse import urlencode
import threading

# Custom Imports
from CustomCrossfade import CustomCrossfade

app = Flask(__name__)

app.secret_key = 'nIe8c&Z*coP!DKm2gqZf' # Messing around with flash messaging.

application = app # For beanstalk, officially fucking stupid.  Never used elsewhere.

HostDomain = 'http://www.crossfitcrossfader.com'

global ThreadReset

ThreadReset = False

# 'http://www.crossfitcrossfader.com'
# 'http://127.0.0.1:5000'


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

@app.route('/flashtest')
def flashtest():
    flash('You\'ve been flashed.')

    return redirect('/')

@app.route('/crossfade/killplayer')
def killplayer():

    global ThreadReset
    
    print(f'ThreadReset was {ThreadReset}')
    flash('Attempting to stop player.')
    ThreadReset = True
    CustomCrossfade.sleep(1)    
    print(f'ThreadReset is now {ThreadReset}')

    return redirect('/crossfade')

@app.route('/crossfade')
def crossfade():

    playlists = CustomCrossfade.Playlists        

    return render_template('crossfade.html', title='Crossfit Crossfader Home', playlists=playlists)


@app.route('/playlistplay/<int:ListId>')
def playlistplay(ListId):    

    @copy_current_request_context
    def player(ListId):    

        global ThreadReset 

        print(f'Beginning playlist {CustomCrossfade.Playlists[ListId][0]}')
        
        ThreadReset = False
        SleepTime = 0        
        
        for Song in CustomCrossfade.Playlists[ListId][1]:
            if ThreadReset == False:

                SleepTime = int(Song[2])

                VolumeDown()
                
                CustomCrossfade.AddSongToQueue(Song[0], CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')))
                
                CustomCrossfade.SkipToNextSong(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')))

                if int(Song[1]) > 0:
                    print(f'Skipping to {Song[1]}')                
                    CustomCrossfade.SeekToTime(Song[1], CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')))

                VolumeUp()

                print(f'Sleeping for {SleepTime}')

                SleepTime = SleepTime * 2

                while ThreadReset == False and SleepTime > 0:
                    CustomCrossfade.sleep(.5)
                    SleepTime -= 1                
        
        print('Leaving Player Function.')

        VolumeDown()
        CustomCrossfade.SkipToNextSong(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')))
        VolumeUp()

        return True


    @copy_current_request_context
    def VolumeDown():
        print('Dropping Volume.')
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 70)
        # CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 60)
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 50)
        # CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 40)
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 30)
        # CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 20)
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 10)        

        return True

    @copy_current_request_context
    def VolumeUp():    
        print('Raising Volume.')                    
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 20)
        # CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 30)
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 40)
        # CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 50)
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 60)
        # CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 70)
        CustomCrossfade.SetVolume(CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set')), 80)

        return True

    try:
        session['token'] = CustomCrossfade.GetNewAccessToken(session.get('refreshtoken', 'not set'))    
    
    except Exception as errmsg:
        print(errmsg)        
        flash('We need to get you authorized.')
        return redirect('/crossfade/authorize')  

    ListId -= 1 
    
    PlayerThread = threading.Thread(target=player, args=(ListId,)) 
    PlayerThread.start() 

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