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
config = toml.load('CustomCrossfade/config.toml')

# Constants
clientId = config['ClientInfo']['clientId']
clientSecret = config['ClientInfo']['clientSecret']


# Playlist Key, Playlist Name, List of Songs [SpotifyURI, JustTo, Wait]
Playlists = [
                ['Garage Revival', [
                    ['spotify:track:0YPDp1KIxVLTdh3vnvk6wd', '11000', '10'], 
                    ['spotify:track:1JcGNoiwifg0MdJMVgJQYx', '0', '10'], 
                    ['spotify:track:6tedQ1ZmbygqhbdcfJL7Xb', '9000', '5']
                                        ]
                ],

                ['The Who Mix', [
                    ['spotify:track:3qiyyUfYe7CRYLucrPmulD', '11000', '10'], 
                    ['spotify:track:0LN5gIsS5tQSmRzQrHSaTR', '0', '10'], 
                    ['spotify:track:23IJ5wLRhEZ9DOuia5mPiZ', '9000', '5']
                                ]
                ]            
            ]


# Functions
#################################################################################

# Converting Strings to Base64 Encoding
def strToBase64(StrToConvert):
    StrInBytes = StrToConvert.encode('ascii')
    Base64Bytes = base64.b64encode(StrInBytes)
    StrConverted = Base64Bytes.decode('ascii')

    return StrConverted

authStr = strToBase64(f'{clientId}:{clientSecret}')

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

    # print('Getting new access token.')
    response = requests.post(url, headers=headers, data=data)
    # print(response.status_code)
    # print(response.content)

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

    try:
        print(json.dumps(response.json(), indent=2))
    except:
        None

    return True
