import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime

short_title = "What's my age?"
long_title = "What's My Age On Each Planet (assuming you were born on Earth)?"
key = 4
content_date = datetime.datetime(2021, 9, 5).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    today = datetime.date.today()
    birth_date = location.date_input('What\'s your birth date?', datetime.date(2000,1,1), datetime.date(1900,1,1), today)
    
    places = {
        'Mercury': 
            {
                'year_length_earth_days': 88,
                'day_length_earth_hours': 1408,
                'planet_name': 'Mercurian'
            },
        'Venus': 
            {
                'year_length_earth_days': 225,
                'day_length_earth_hours': 5832,
                'planet_name': 'Venutian'
                
            },
        'Earth': 
            {
                'year_length_earth_days': 365,
                'day_length_earth_hours': 24,
                'planet_name': 'Terrestrial'
            },
        'Mars': 
            {
                'year_length_earth_days': 687,
                'day_length_earth_hours': 25,
                'planet_name': 'Martian'
            },
        'Jupiter': 
            {
                'year_length_earth_days': 4333,
                'day_length_earth_hours': 10,
                'planet_name': 'Jovian'
            },            
        'Saturn': 
            {
                'year_length_earth_days': 10759,
                'day_length_earth_hours': 11,
                'planet_name': 'Saturnian'
            },  
        'Uranus': 
            {
                'year_length_earth_days': 30687,
                'day_length_earth_hours': 17,
                'planet_name': 'Uranian'
            },  
        'Neptune': 
            {
                'year_length_earth_days': 60190,
                'day_length_earth_hours': 16,
                'planet_name': 'Neptunian'
            },  
    }

    earth_days_alive = (today - birth_date).days
        
    for k in places.keys():
        place_years = round(earth_days_alive  / places[k]['year_length_earth_days'], 2)
        place_days = round(place_years * places[k]['year_length_earth_days'] * 24 / places[k]['day_length_earth_hours'], 2)
        location.write(f"You're {place_years} {places[k]['planet_name']} years old ({place_days} days on {k}).")    
    



