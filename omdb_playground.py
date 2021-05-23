#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 19:54:08 2021

@author: TDSwayzee22
"""

import requests
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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
        print(SEASON)
        ALL_EPISODES.append(data)
            
        next_season = int(data['Season']) + 1
        total_seasons = int(data['totalSeasons'])
        if next_season > total_seasons:
            return add_season_and_rating_heat_to_episodes(ALL_EPISODES)
        return get_and_save_season(URL, KEY, SHOW, next_season, ALL_EPISODES)
    
    return add_season_and_rating_heat_to_episodes(ALL_EPISODES)

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

def add_season_and_rating_heat_to_episodes(DATA):
    for episodes in DATA:
        number_in_season = 1
        for episode in episodes['Episodes']:
            episode['numberInSeason'] = number_in_season
            episode['Season'] = episodes['Season']
            episode['Heat'] = colorize_rating(episode['imdbRating'])
            number_in_season = number_in_season+1
    return create_episode_dataframe(DATA)


import pandas as pd

def create_episode_dataframe(DATA):
    episode_list = [episode for episodes in DATA for episode in episodes['Episodes']]
    df = pd.DataFrame(episode_list)
    df = convert_column_to_numeric(df, ['imdbRating', 'Season', 'Episode'])
    
    return df.sort_values(['Season', 'Episode'], ascending=[True, True])

def convert_column_to_numeric(DATA, COLUMN_LIST):
    for i in COLUMN_LIST:
        DATA[i] = pd.to_numeric(DATA[i])
    return DATA
    

# TODO: see if clickable links can be added (click a cell to go to imdb ep page)
df = get_and_save_season(URL, KEY, SHOW)
ratings = pd.pivot_table(df, 'imdbRating', 'Season', 'numberInSeason')


#
plt.figure(figsize=(24,20))
ax = sns.heatmap(ratings, annot=True, linewidths=1, cmap=mpl.cm.get_cmap('RdYlGn'))
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax.tick_params(length=0)
ax.tick_params(axis='both', which='major', labelsize=24)
ax.tick_params(axis='both', which='minor', labelsize=24)
plt.rc('font', size=font_size)
plt.rc('axes', titlesize=font_size)
label_style = {'fontname':'Helvetica','fontsize':'24'}
plt.xlabel('Episode Number', **label_style)
plt.ylabel('Season', **label_style)
plt.yticks(rotation=0)
plt.show()
