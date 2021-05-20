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
show='south park'
season=1

def urlify_string(string):
    return string.replace(' ', '+')

def get_and_save_season(URL, KEY, SHOW, SEASON=1, ALL_EPISODES=[]):
    params = {
        'apikey': KEY,
        't': urlify_string(SHOW),
        'Season': SEASON,
        'r': 'json'
    }
    
    response = requests.get(URL, params=params)
    data = json.loads(response.text)
    if SEASON == 1:
        ALL_EPISODES = []
    if data['Response']:
        ALL_EPISODES.append(data)
            
        next_season = int(data['Season']) + 1
        total_seasons = int(data['totalSeasons'])
        if next_season > total_seasons:
            return ALL_EPISODES
        return get_and_save_season(URL, KEY, SHOW, next_season)
    
    return ALL_EPISODES

def colorize_rating(RATING):
    rating = float(RATING)
    if rating >= 9:
        return 'darkgreen'
    elif rating >= 8:
        return 'green'
    elif rating >= 7:
        return 'yellow'
    elif rating >= 6:
        return 'orange'
    else:
        return 'red'

def add_rating_heat_to_episodes(DATA):
    for episodes in DATA:
        for episode in episodes['Episodes']:
            episode['Heat'] = colorize_rating(episode['imdbRating'])
    return DATA