import urllib.request, urllib.parse, urllib.error
import requests
import folium
import json
import ssl
from map_packadge import twurl
from collections import defaultdict


def get_json_data(acct):
    """
    (str) -> dict
    Finds info about user using Twitter API by input id

    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    if (len(acct) < 1):
        return None
    url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': '200'})

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)

    return js


def get_cordinates(place):
    """
    (str) -> int, int

    This function return geo cordinates of place which is in input address
    """
    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'sensor': 'false', 'address': place,
                  'key': "AIzaSyCWlF52EqYEPR_bdBQ5VimURihmAtkDTSU"}
        r = requests.get(url, params=params)
        results = r.json()['results']
        location = results[0]['geometry']['location']
        return location['lat'], location['lng']
    except IndexError:
        return None, None


def create_map(js_data, ):
    """
    dict -> None

    This function gets dict in which key is address and value is
    another dict in which key is name for group and value is list
    of films names

    {address:  {group_name:[film1, film2, film3]} }
    """
    d = defaultdict(list)
    map_out = folium.Map()
    for user in range(len(js_data["users"])):
        lt, ln = get_cordinates(js_data["users"][user]["location"])
        if lt == None:
            continue
        d[(lt, ln)].append(js_data["users"][user]["screen_name"])

    for key in d.keys():
        out_str = ""
        for i in d[key]:
            out_str += "<a>" + i + "</a><br> "

        map_out.add_child(folium.Marker(
            popup=out_str,
            location=key))

    map_out.save('static/map.html')
