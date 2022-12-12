import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

short_title = "What's My Age?"
long_title = "What's My Age On Each Planet?"
key = 4
content_date = datetime.datetime(2021, 9, 15).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    #location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    col1, _ = st.columns((1,3))

    birth_date = col1.date_input('What\'s your birth date?', value=datetime.date(2000,1,1), min_value=datetime.date(1900,1,1), max_value=yesterday)
    
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
    
    if birth_date is not None:

        try:

            earth_days_alive = (today - birth_date).days
            df = pd.DataFrame()
            df['Planet'] = places.keys()    

            df['Age_in_Years'] = df['Planet'].apply(lambda x: round(earth_days_alive  / places[x]['year_length_earth_days'], 2))
            df['Age_in_Days'] = df.apply(lambda x: round(x['Age_in_Years'] * places[x['Planet']]['year_length_earth_days'] * 24 / places[x['Planet']]['day_length_earth_hours'], 2), axis=1)

            #for k in places.keys():
            #    place_years = round(earth_days_alive  / places[k]['year_length_earth_days'], 2)
            #    place_days = round(place_years * places[k]['year_length_earth_days'] * 24 / places[k]['day_length_earth_hours'], 2)
            #    location.write(f"You're {place_years} {places[k]['planet_name']} years old ({place_days} days on {k}).")    

            plt.style.use('seaborn')
            fig, ax = plt.subplots(figsize=(8,5))
            fig.suptitle('Age On Each Planet', fontsize=14)
            plt.xlabel('Planet', fontsize=10)
            plt.ylabel('Age In Years', fontsize=10)
            ax.bar(df['Planet'], df['Age_in_Years'])
            
            buf = BytesIO()
            fig.savefig(buf, format="png")

            ylabels = ax.get_yticklabels()
            first_tick = float(ylabels[1].get_text())
            last_tick = float(ylabels[-1].get_text())

            for i, v in enumerate(df['Age_in_Years']):
                if v > first_tick:
                    ax.text(i-.35, v - last_tick * .05, str(round(v,2)), color='black', fontweight="bold")        
                else:
                    ax.text(i-.35, v + last_tick * .03, str(round(v,2)), color='black', fontweight="bold")        
            
            buf = BytesIO()
            fig.savefig(buf, format="png")
            location.image(buf)
        except Exception as e:
            location.write("Try a different date.")

    
    



