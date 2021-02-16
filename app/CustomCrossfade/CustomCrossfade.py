""" Custom Crossfade needs documentation.

"""

# PSL Imports
import base64
import json
from time import sleep

# 3rd Party Imports
import requests
import toml

# Project Imports
secrets = toml.load('CustomCrossfade/secrets.toml')

# Constants
clientId = secrets['ClientInfo']['clientId']
clientSecret = secrets['ClientInfo']['clientSecret']

# Loading Old Token
with open('CustomCrossfade/oldtoken.txt', 'r') as reader:
    refreshtoken = reader.read()
reader.close()


# https://accounts.spotify.com/authorize?client_id=e35e8d9e13754f3389657a3ded64b4ea&response_type=code&redirect_uri=https%3A%2F%2Fwintermindgroup.com%2F&scope=user-read-private%20user-read-email%20user-modify-playback-state
code = 'AQA8D2oGd31yechZ06IjvEDD3pRVw5c5TiH4XFKFj2lxDecFLdOW8iD02XK4Sdoykr_C20Eyvhry20tCWtVCART9E0H57WR-OVeV6obho5TfvFvRGTr0G5EKqP45bs0ydu9mJRUozcR7TVUfuAGQ_i5Tbd-XTj0Bg90kQf9VF-5ek2zwjzhwZ_4zSU5w9GjmApMp6AokfO3p5JncGPq3KWkdRTk'
token = 'BQBv8gAgd5C5J1-dH3tfBPofWQFIUHNwFbDNTdAibQWhgwCAbcc4VrxabjifUPXcH3CAarZ5fOwkjBITuDdlV2Cvw_fMNmL4guFRpj4FcyVS7RtTVVvCbZSHJKY9nObhB_MCY1rvjyIUJyCbysZlbPOvl9qOfdD53Q'

# Song List [URI, Skip, Wait]

SongList = [
    ['spotify:track:0YPDp1KIxVLTdh3vnvk6wd', '11000', '20'], 
    ['spotify:track:1JcGNoiwifg0MdJMVgJQYx', '0', '30'],
    ['spotify:track:6tedQ1ZmbygqhbdcfJL7Xb', '9000', '21']
        ]


# Functions
#################################################################################

# Converting Strings to Base64 Encoding
def strToBase64(StrToConvert):
    StrInBytes = StrToConvert.encode('ascii')
    Base64Bytes = base64.b64encode(StrInBytes)
    StrConverted = Base64Bytes.decode('ascii')

    return StrConverted


# Get token from code
def GetTokensFromCode(authStr, code, RedirectURI):

    url = 'https://accounts.spotify.com/api/token'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization' : f'Basic {authStr}'
        }

    data = {
    'grant_type': 'authorization_code',
    'code': f'{code}',
    'redirect_uri': f'{RedirectURI}'
    }

    response = requests.post(url, headers=headers, data=data)
    
    return response

# Refresh Token
def GetNewAccessToken(RefreshToken):

    url = 'https://accounts.spotify.com/api/token'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization' : f'Basic {authStr}'
        }

    data = {
    'grant_type': 'refresh_token',
    'refresh_token': f'{RefreshToken}'
    }

    print('Getting new access token.')
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    print(response.content)

    return response.json()['access_token']



# Adding song to queue. user-modify-playback-state
def AddSongToQueue(SpotURI, token):

    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': f'Bearer {token}'
            }
    
    params = (
        ('uri', f'{SpotURI}'),
            )

    response = requests.post('https://api.spotify.com/v1/me/player/queue', headers=headers, params=params)
    
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        None

    return True


# Adding song to queue. user-modify-playback-state
def SkipToNextSong(token):

    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': f'Bearer {token}'
            }

    response = requests.post('https://api.spotify.com/v1/me/player/next', headers=headers)

    try:
        print(json.dumps(response.json(), indent=2))
    except:
        None

    return True

# Skip to spot in track. user-modify-playback-state
def SeekToTime(TimeMS, token):

    url = f'https://api.spotify.com/v1/me/player/seek?position_ms={TimeMS}'

    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': f'Bearer {token}'
            }             
    
    print(url)

    response = requests.put(url=url, headers=headers)
    # print(response.status_code)
    # print(response.content)

    try:
        print(json.dumps(response.json(), indent=2))
    except:
        None

    return True




authStr = strToBase64(f'{clientId}:{clientSecret}')
RedirectURI = 'https://wintermindgroup.com/'


def playlistplay():

    try:
        with open('CustomCrossfade/oldtoken.txt', 'r') as reader:
            refreshtoken = reader.read()
            reader.close()
        token = GetNewAccessToken(refreshtoken)
    except:
        code = GetNewCode()
        response = GetTokensFromCode(authStr, code, RedirectURI)

        token = response.json()['access_token']
        refreshtoken = response.json()['refresh_token']

        with open('CustomCrossfade/oldtoken.txt', 'w') as writer:
            writer.write(refreshtoken)
        writer.close()

    # Adding Songs to Queue
    for Song in SongList:
        print('Adding a song to up next.')
        token = GetNewAccessToken(refreshtoken)
        AddSongToQueue(Song[0], token)
        print('Song Added')

    print('Skipping to next song.')
    token = GetNewAccessToken(refreshtoken)
    SkipToNextSong(token)

    for Song in SongList:
        if int(Song[1]) > 0:
            print(f'Skipping to {Song[1]}')
            token = GetNewAccessToken(refreshtoken)
            SeekToTime(Song[1], token)    
        print(f'Sleeping for {Song[2]}')
        sleep(int(Song[2]))
        token = GetNewAccessToken(refreshtoken)
        SkipToNextSong(token)
