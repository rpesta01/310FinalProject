
import random
import urllib.parse, urllib.request, urllib.error, json
import requests
from requests.exceptions import ReadTimeout
import keys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable



def geocode(place):
    geolocator = Nominatim(user_agent="Learning Python")
    location = geolocator.geocode(place)
    if location != None:
        coords = (location.latitude, location.longitude)
    else:
        coords = None
    return(coords)


def isitwater(coords):

    baseurl = "https://isitwater-com.p.rapidapi.com/"
    lat = coords[0]
    lng = coords[1]

    latlng = {"latitude":lat,"longitude":lng}

    headers = {
        "X-RapidAPI-Key": keys.isitwater_key,
        "X-RapidAPI-Host": "isitwater-com.p.rapidapi.com"
    }

    response = requests.get(baseurl, headers=headers, params=latlng)
    
    return(response.json())


def get_state(response_dict):
    return(response_dict["water"])



# print((isitwater(geocode("175 5th Avenue NYC"))))

# print(get_state(isitwater(geocode("175 5th Avenue NYC"))))

# print(geocode("175 5th Avenue NYC"))

def searchsound(term):
    baseurl = "https://freesound.org/apiv2/search/text/"
    
    

    headers = {
        "Authorization": "Token " + keys.freesound_key
    }
    params = {"query": term, "page_size": 30, "fields": "name,previews,images"}

    response = requests.get(baseurl, headers=headers, params=params)
    data = response.json()
    results = data["results"]
    sound_dict = {}
    for sound in results:
        infolist = []
        sound_dict[sound["name"]] = infolist
        infolist.append(sound["previews"]["preview-hq-mp3"])
        infolist.append(sound["images"]["waveform_l"])
        

    mp3s = []
    for i in sound_dict.values():
        mp3s.append(i)
    
    return mp3s[random.randint(0,28)]

def rightformat(coords):
    try:
        if len(coords) == 2:
            lat = float(coords[0])
            lng = float(coords[1])
            if (-90 <= lat <= 90) and (-90 <= lng <= 90):
                return True
    except (ValueError):
        pass

    return False

def wrongformat(place):
    try:
        geocode(place)
    except GeocoderUnavailable:
        return False
    
    return True