import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime
import pandas as pd
import timeit

short_title = "iterrows() and itertuples()"
long_title = "iterrows() and itertuples()"
key = 5
content_date = datetime.datetime(2021, 10, 5).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.write(f"Pandas `iterrows()` and `itertuples()` provide two different ways to `iter`ate over rows in a DataFrame. "
    "If you're working with a data set that contains columns with different data "
    "types, use caution since `iterrows()` and `itertuples()` may not always return the data you expect. Here's an example based on the "
    "Pandas documentation."
    )

    location.write(f"### iterrows()")

    location.write(f"`iterrows()` returns a Pandas `Series`. "
    )

    # this works
    # ser = pd.Series([1,2, 3.0])
    # location.write(ser)
    # ser = pd.Series(['1','2','3.0'])
    # location.write(ser)
    # this fails - seems like a streamlit bug
    #ser = pd.Series(['1', 2, 3])
    #location.write(ser)
    # this also fails
    # ser = pd.Series([1, '2', 3])
    # location.write(ser)

    df = pd.DataFrame([[1, 2.0, 3]], columns=['int', 'float', 'cat'])
    df['cat'] = df['cat'].astype('category')
    
    location.code(
        """
df = pd.DataFrame([[1, 2.0, 3]], columns=['int', 'float', 'cat']) # Create a dataframe with several different data types
df['cat'] = df['cat'].astype('category') # make 'cat' a categorical type
        """
    )  
    location.write(df)

    location.write("You might expect to get back a `Series` containing an `int`, `float` and `category`. But, in this case, `iterrows()` returns a `Series` of `float64`.")
    location.code(
        """
_, row = next(df.iterrows())
row
        """
    )  
    i, row = next(df.iterrows())
    location.write(row)
    location.code(
        """
row['cat'].dtype
        """
    )  
    location.write(row['cat'].dtype)        

    location.write(f"### itertuples()")

    location.write(f"`itertuples()` returns a `NamedTuple`."
    )

    df = pd.DataFrame([[1, 2.0, 3 ,'str', '2021-01-01']], columns=['int', 'float', 'cat', 'str', 'date'])
    df['cat'] = df['cat'].astype('category')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
    location.code(
        """
df = pd.DataFrame([[1, 2.0, 3 ,'str']], columns=['int', 'float', 'cat', 'str'])
df['cat'] = df['cat'].astype('category')        """
    )  
    location.write(df)

    location.code(
        """
_, row = next(df.itertuples())
row
        """
    )  
    row = next(df.itertuples())
    #location.write(row)
    location.code(
        """
type(row.date)
        """
    )  
    location.write(type(row.date))     
    location.write('Returning the date from the tuple works as expected. But returning the category column doesn''t return a category object. It returns an `int` in this case. ')

    location.code(
        """
type(row.cat)
        """
    )  
    location.write(type(row.cat))   

    location.markdown("### Performance")    

    location.markdown("`iterrows()` and `itertuples()` might be useful if you must iterate over a Pandas dataframe. But from a performance perspective, both `iterrows()` and `itertuples()` should be avoided in favor of "
    "code that uses vectorization. Vectorization allows the CPU to work on multiple values at a time and it's what makes numpy operations blazingly fast. "
    "If you must iterate, you'll probably find `itertuples()` to be significantly faster. You should test your code with `timeit` or another performance testing tool to make sure `itertuples()` is actually faster.")

    location.code("""
df = pd.DataFrame([i for i in range(10000)]) # create a dataframe with 1000 rows    
    """)
    
    df = pd.DataFrame([i for i in range(10000)])

    location.code("""
for i in df.iterrows(): pass
    """)

    s = 0
    x = timeit.repeat(
            stmt='for i in df.iterrows(): pass',
            repeat=1,
            number=1,
            globals=dict(globals(), **locals()),
        )

    location.markdown(f"Runtime: {x[0]} s")

    x = timeit.repeat(
            stmt='for i in df.itertuples(): pass',
            repeat=1,
            number=1,
            globals=dict(globals(), **locals()),
        )

    location.code("""
for i in df.itertuples(): pass
    """)

    location.markdown(f"Runtime: {x[0]} s")

    location.markdown("Interestingly, `apply()` seems to be slower than `itertuples()` in some cases such as `apply`ing the function to every row (`axis=1`). "
    "For a long time, I assumed `apply()` was always faster but that's not the case in every situation.")

    x = timeit.repeat(
            stmt='df.apply(lambda row: None, axis=1)',
            repeat=1,
            number=1,
            globals=dict(globals(), **locals()),
        )

    location.code("""
df.apply(lambda row: None, axis=1)
""")

    location.markdown(f"Runtime: {x[0]} s")

    location.markdown("Thanks for reading.")

    location.markdown("### Resources")

    location.write(
        """
    * [iterrows() Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html)
    * [itertuples() Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.itertuples.html)
    * [Pandas Basics](https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html?highlight=vectorize#iteration)
    
"""
    )




