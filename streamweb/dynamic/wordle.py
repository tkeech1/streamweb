import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime
import streamlit.components.v1 as components

short_title = "Wordle Assist"
long_title = "Need some help on Wordle?"
key = 9
content_date = datetime.datetime(2023, 5, 19).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    #location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.write("""I really liked Wordle until I wrote this app. I used to look forward to seeing a new puzzle each day. 
    Now, Wordle Assist has killed that fun. Each daily Wordle puzzle has become a chance to test/tweak/tune 
    Wordle Assist. If you're having trouble with today's Wordle, give Wordle Assist a try and let it kill your fun too. 
    """)

    location.write("""Wordle Assist is my first attempt at using Rust. More and more Python projects are 
    using Rust (Pydantic, Polars, Ruff, etc.) because of it's speed and memory safety 
    features. It was past time for me to give Rust a shot. 
    """)

    location.write("""I've used statically typed languages in the past and I've always sort-of missed 
    the perceived safety of compile-time checks when writing Python. Python's type hints are great but 
    they're just not the same. Rust is hard. I don't yet have a great mental model for working with ownership and 
    the borrow-checker but this project gave me some good quality time with the language. The Rust "ecosystem" (I don't like that term
    but can't think of anything better) including **cargo** provide a nice integrated developer experience for building, testing and 
    packaging code. 
    """)

    location.markdown("""
A few interesting things about this project:
* There's no backend - it's hosted on S3. Everything runs in the browser.
* The Rust code is compiled to WASM using wasm-pack and is about 1.4 MB (this includes the list of >14K 5-letter words). That's pretty big
for a web app but, once it's loaded, it's pretty snappy. I didn't compare performance to a similar app written in PyScript or Javascript but that might be interesting. 
* I spent the most time on the Javascript UI to make it responsive and build a custom keyboard that looked and worked better on mobile than the native keyboard.
I used TailWind CSS for the first time and I really like it. 
* The "Suggested Next Guess" is a simple algorithm - no AI or anything fancy. It calculates the next guess by scoring words in the dictionary
based on the letters that have been guessed. It seems to work pretty well but there are some rough edges.  
    """)

    location.markdown("""
Overall, it was a fun project and I'm looking forward to seeing what else is possible with Rust in the browser. There are a lot of 
intersting front-end frameworks written in Rust (Leptos, Sycamore, Yew) I'd like to try. I have a 
long way to go with Rust but that's part of the fun. 

* Demo: [http://tkeech.s3-website-us-east-1.amazonaws.com/](http://tkeech.s3-website-us-east-1.amazonaws.com/)
* Code: [https://github.com/tkeech1/wordleassist](https://github.com/tkeech1/wordleassist)
    """)    

    components.iframe("http://tkeech.s3-website-us-east-1.amazonaws.com/", width=375,height=667)   







