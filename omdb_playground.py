#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 19:54:08 2021

@author: TDSwayzee22
"""

import requests
import json

key=KEY
url = 'http://www.omdbapi.com/'
all_episodes = []
show='south park'
season=1

def urlify_string(string):
    return string.replace(' ', '+')

def get_season_episodes(URL, KEY, SHOW, SEASON):
    params = {
        'apikey': KEY,
        't': urlify_string(SHOW),
        'Season': SEASON,
        'r': 'json'
    }
    
    response = requests.get(url, params=params)
    return json.loads(response.text)

def save_season(SEASON):
    if SEASON['Response']:
        episodes = data['Episodes']
        for episode in episodes:
            all_episodes.append(episode)
    return False



data = json.loads(sp.text)
if data['Response']:
    episodes = data['Episodes']
    for episode in episodes:
        all_episodes.append(episode)
    season = season + 1
    

# break needs to be response = False

for episode in sp:
   for key, value in episode.items():
       print(value)
       
my_json = sp.decode('utf8').replace("'", '"')