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
                ['MetCon', [
                   ['spotify:track:6xxXrNJnnsQNLdgNk8S4y8','0','125'],
                   ['spotify:track:1JcGNoiwifg0MdJMVgJQYx','0','81'],
                   ['spotify:track:0YPDp1KIxVLTdh3vnvk6wd','11000','103'],
                   ['spotify:track:2VHfyWLlvCvbkIqtS5tqt3','8000','77'],
                   ['spotify:track:4NVKpvX9pcSeoKiNvjmb5X','100000','94'],
                   ['spotify:track:6950ik0V6HCWgnLIFKe8FX','0','133'],
                   ['spotify:track:3bTJRzsVHaL4JOmmNX4Cm3','3000','111'],
                   ['spotify:track:6VR2wTjJGtlBnQztwVCbQM','0','227'],
                   ['spotify:track:26TvTiU4H4OZ3bGvKmHA4L','0','91'],
                   ['spotify:track:26vGXL80873wfoGhBGpFSn','22000','185']
                            ]                                
                ],

                ['Workout', [
                   ['spotify:track:2TK7GCEHBhX0nKZXf6fBGQ','0','116'],
                   ['spotify:track:52LL3IFB8N3PaJmoZ8Xii1','12000','108'],
                   ['spotify:track:5D1oPeuU4sGUwI5obM4bKZ','0','114'],
                   ['spotify:track:2GZbJjsph5LKA0reVwefxH','0','78'],
                   ['spotify:track:3VuwZNTCD0ZNIl3GSnreLC','23000','143'],
                   ['spotify:track:2tgooVPSQx14Od9xzz9Kc3','0','111'],
                   ['spotify:track:7hUKxjrojKK6r4wiO3G9iU','0','194'],
                   ['spotify:track:2j8W67NdrHhYRrCgdBCRMk','0','135']
                                ]
                ] # ,

                # ['Skipper', [
                #    ['spotify:track:2TK7GCEHBhX0nKZXf6fBGQ','5000','10'],
                #    ['spotify:track:52LL3IFB8N3PaJmoZ8Xii1','5000','10'],
                #    ['spotify:track:5D1oPeuU4sGUwI5obM4bKZ','5000','10'],
                #    ['spotify:track:2GZbJjsph5LKA0reVwefxH','5000','10'],
                #    ['spotify:track:3VuwZNTCD0ZNIl3GSnreLC','5000','10'],
                #    ['spotify:track:2tgooVPSQx14Od9xzz9Kc3','5000','10'],
                #    ['spotify:track:7hUKxjrojKK6r4wiO3G9iU','5000','10'],
                #    ['spotify:track:2j8W67NdrHhYRrCgdBCRMk','5000','10']
                #                 ]
                # ]
            ]


# Functions
#################################################################################


# Converting Strings to Base64 Encoding
def GetDeviceID(token):
    headers = {
    'Accept' : 'application/json',
    'Content-Type' : 'application/json',
    'Authorization': f'Bearer {token}'
        }

    response = requests.get('https://api.spotify.com/v1/me/player/devices', headers=headers)

    DeviceID = response.json()['devices']['id']
    print(DeviceID)

    return DeviceID


# Converting Strings to Base64 Encoding
def SetVolume(token, Volume):    
    headers = {
    'Accept' : 'application/json',
    'Content-Type' : 'application/json',
    'Authorization': f'Bearer {token}'
        }
    
    url = f'https://api.spotify.com/v1/me/player/volume?volume_percent={Volume}'

    response = requests.put(url=url, headers=headers)
    # print(response.status_code)
    print(f'Setting volume to {Volume}%.')

    return True


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
