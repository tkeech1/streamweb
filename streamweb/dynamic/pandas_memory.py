import streamlit as st
import datetime
import pytz
from datetime import date
from utils.metrics import log_runtime
import pandas as pd
import timeit

short_title = "Pandas Memory Usage"
long_title = "Pandas Memory Usage"
key = 7
content_date = datetime.datetime(2021, 10, 5).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    #location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.markdown(f"" \
    "The size of a DataFrame in-memory can exceed the size of the file on disk and, "\
    "for certain operations, Pandas can consume 3-5x current memory usage due to intermediate results. "\
    "Specifying the right data types is good best way to reduce memory usage. Below is an"\
    " example dataframe:"
    )

    data = {'addresses': ['53278 Smith Pass','5531 Lane Forks	45','5437 Paul Pine	43','5835 Samuel River','987 Sharon Underpass'],
    'ints': [95,45,43,39,46],
    'floats': [654.869995,-756.500000,45.899994,-441.350006,-582.849976],
    'dates':['2002-06-26','2020-11-14','2005-11-28','2022-04-11','1991-10-19'],
    'currency':['$7555','$6459','$7814','$4156','$759'],
    'unused':['391 David TerraceScotthaven','58212 Glenn IsleSouth Jenniferland','091 Oconnor MountainsWest Raymond','705 Lopez Wells Apt. 443Longfurt','1929 Stephanie PlainEast Andreamouth'],
    'category':['DarkSalmon','LightBlue','MediumPurple','SeaShell','DarkGray'],
    }

    df = pd.DataFrame.from_dict(data)

    location.dataframe(df)

    location.markdown(f"### Inspecting Memory Usage")

    location.markdown(f"The `info()` function provides details about the memory "\
    " footprint of the Dataframe. The `memory_usage='deep'` parameter calculates the real memory usage - it can take a " \
    " long time to run on a large dataset. "
    )

    location.code(
        """
df.info(memory_usage='deep')
        """
    )

    location.code("""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 7 columns):
 #   Column     Non-Null Count   Dtype  
---  ------     --------------   -----  
 0   addresses  100000 non-null  object 
 1   ints       100000 non-null  int64  
 2   floats     100000 non-null  float64
 3   dates      100000 non-null  object 
 4   currency   100000 non-null  object 
 5   unused     100000 non-null  object 
 6   category   100000 non-null  object 
dtypes: float64(1), int64(1), object(5)
memory usage: 36.4 MB
    """)

    location.markdown(f"Although the data file is only 11 MB on disk, the DataFrame uses uses 36.4 MB. We can examine "\
    "the memory usage by column."
    )

    location.code(
        """
def memory_by_column(df):
    meminfo = df.memory_usage(deep=True)
    meminfo_numeric = meminfo.apply(lambda x: round(x / 1024 ** 2,2))
    meminfo = meminfo.apply(lambda x: f'{round(x / 1024 ** 2,2)} MB')
    print(meminfo)
    print()
    print(f'Total Memory Used: {meminfo_numeric.sum()} MB')
"""
    )

    location.code("""
Index         0.0 MB
addresses    7.58 MB
ints         0.76 MB
floats       0.76 MB
dates        6.39 MB
currency      5.9 MB
unused       8.73 MB
category     6.28 MB
dtype: object

Total Memory Used: 36.4 MB
    """)

    location.markdown(f"" \
    "Let's go column-by-column and see what we can do to reduce the memory footprint. "
    )

    location.markdown(f"### Only import the data you need"
    )

    location.markdown(f"We'll start by removing the `unused` column since we don't plan to use it. We can do this when "\
    "we initally read the CSV file using the `usecols` parameter."
    )

    location.code("""
cols = ['addresses','ints','floats','dates','currency','category']
df = pd.read_csv('dataset.csv', usecols=cols)
df.info(memory_usage='deep')
    """)

    location.code("""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 6 columns):
 #   Column     Non-Null Count   Dtype  
---  ------     --------------   -----  
 0   addresses  100000 non-null  object 
 1   ints       100000 non-null  int64  
 2   floats     100000 non-null  float64
 3   dates      100000 non-null  object 
 4   currency   100000 non-null  object 
 5   category   100000 non-null  object 
dtypes: float64(1), int64(1), object(4)
memory usage: 27.7 MB
    """)

    location.markdown(f"""You can also load a subset of data using the `nrows` parameter. This is useful when you 
    have a large dataset and just want to get a feel for the data and types. 
    """      
    )

    location.markdown(f"### Use appropriate data types for numeric columns"
    )
    
    location.markdown(f"""
    Pandas imported several columns as `int64` and `float64` types. These might be too large for what we need. We can examine these
    columns more closely to determine the right data type.
    """      
    )

    location.code("""
print(f"Max value for ints field is {df['ints'].max()}")
print(f"Min value for ints field is {df['ints'].min()}")
    """)

    location.code("""
Max value for ints field is 99
Min value for ints field is 0
    """)

    location.markdown(f"""
    Now we can convert the columns to the appropriate types.
    """      
    )

    location.code("""
df['ints'] = df['ints'].astype(np.uint8)
memory_by_column(df)
    """)

    location.code("""
Index         0.0 MB
addresses    7.58 MB
ints          0.1 MB
floats       0.76 MB
dates        6.39 MB
currency      5.9 MB
category     6.28 MB
dtype: object

Total Memory Used: 27.1 MB
    """)

    location.markdown("We can also use the Pandas `downcast()` function to try to downcast larger types to smaller types.")

    location.code("""
df['ints'] = pd.to_numeric(df['ints'], downcast="unsigned")
df['floats'] = pd.to_numeric(df['floats'], downcast="float")
memory_by_column(df)
    """)

    location.code("""
    <class 'pandas.core.frame.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 6 columns):
 #   Column     Non-Null Count   Dtype  
---  ------     --------------   -----  
 0   addresses  100000 non-null  object 
 1   ints       100000 non-null  uint8  
 2   floats     100000 non-null  float32
 3   dates      100000 non-null  object 
 4   currency   100000 non-null  object 
 5   category   100000 non-null  object 
dtypes: float32(1), object(4), uint8(1)
memory usage: 26.6 MB
    """)

    location.code("""
Index         0.0 MB
addresses    7.58 MB
ints          0.1 MB
floats       0.38 MB
dates        6.39 MB
currency      5.9 MB
category     6.29 MB
dtype: object

Total Memory Used: 26.64 MB
    """)

    location.markdown("The `floats` field was a `float64` and was converted to a `float32`, saving some memory space.")

    location.markdown(f"### Convert `object` types to numeric types when possible"
    )

    location.markdown(f"""
    In this example, the `currency` field is a float but Pandas recognized it as an `object` due to 
    presence of the `$` character.  Since we already have a Dataframe loaded, we can simply replace the 
    `$` with ` ` and then convert it to an 
    unsigned `int` since the values are between 0-9999. 
    """)

    location.code("""
# Vectorized string replacement
df['currency'] = df['currency'].str.replace('$','', regex=False)
df['currency'] = pd.to_numeric(df['currency'], downcast='unsigned')
    """)

    location.code("""
Index         0.0 MB
addresses    7.58 MB
ints          0.1 MB
floats       0.38 MB
dates        6.39 MB
currency     0.19 MB
category     6.29 MB
dtype: object

Total Memory Used: 20.93 MB
    """)

    location.code("""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 6 columns):
 #   Column     Non-Null Count   Dtype  
---  ------     --------------   -----  
 0   addresses  100000 non-null  object 
 1   ints       100000 non-null  uint8  
 2   floats     100000 non-null  float32
 3   dates      100000 non-null  object 
 4   currency   100000 non-null  uint16 
 5   category   100000 non-null  object 
dtypes: float32(1), object(3), uint16(1), uint8(1)
memory usage: 20.9 MB    
    """)

    location.markdown(f"""The `currency` column is now a `uint16` and takes up less memory than it did before. In cases where 
    you'd prefer to perform the conversion prior to loading the Dataframe into memory, you can create a custom Pandas
    converter function to parse the data on import. The downside with converters is that they can be slow since they operate
    one row at a time. Vectorized operations, as in the example above, are usually much faster. Below is an example of a converter 
    function. 
    """)

    location.code("""
# Converter Example
def convert_currency(val, replace_value, replacement_value, final_type):
    return final_type(val.replace(replace_value, replacement_value))

from functools import partial

converters = {'currency': partial(convert_currency, replace_value='$', 
                               replacement_value='', final_type=np.uint16)}

df = pd.read_csv('dataset.csv', usecols=cols, converters=converters)

    """)

    location.markdown("""
    Let's say we don't have enough memory to read the entire data frame into memory before converting the `currency` field
    into a minimal numeric type. We can use a converter OR we can use *chunking*. In the chunking approach, we read the 
    CSV file in chunks, perform a conversion on each chunk (one at a time) and then store the converted data in the 
    Dataframe. Depending on the size of the dataset and the type of conversion, chunking might be faster. 
    """)

    location.code("""
# Chunking Example
df_final = pd.DataFrame()

for df_tmp in pd.read_csv('dataset.csv', usecols=cols, chunksize=10_000):
    df_tmp['currency'] = pd.to_numeric(df_tmp['currency'].str.replace('$','', regex=False), downcast='unsigned')
    df_final = pd.concat([df_final, df_tmp], ignore_index=True)
    
memory_by_column(df_final)
    """)

    location.markdown(f"""### Use the `category` type
    """)

    location.markdown(f"""Categorical fields should use the `category` type. A good rule of thumb is to 
    use a `category` type when less that than 50% of the values are unique.
    """)

    location.code("""
df['category'] = df['category'].astype('category')
    """)

    location.markdown(f"""### Convert dates to `dateTime`
    """)

    location.markdown(f"""Finally, let's convert the `dates` field to a `datetime` type.
    """)

    location.code("""
from datetime import datetime

date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')

df = pd.read_csv("dataset.csv", parse_dates=['dates'], date_parser=date_parser)
    """)

    location.markdown(f"""### Putting it all together
    """)  

    location.markdown(f"""Now we can put all the pieces together in a single code block.
    """)  

    location.code("""

cols = ['addresses','ints','floats','dates','currency','category']
col_types = {"addresses": "object",
             "ints": "uint8",
             "floats": "float32",
             "category": "category"
            }

date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')

def convert_currency(val, replace_value, replacement_value, final_type):
    return final_type(val.replace(replace_value, replacement_value))

from functools import partial

converters = {'currency': partial(convert_currency, replace_value='$', 
                               replacement_value='', final_type=np.uint16)}

df = pd.read_csv('dataset.csv', usecols=cols, dtype=col_types,
                 parse_dates=['dates'], date_parser=date_parser,
                 converters=converters)

    """)   

    location.code("""
memory_by_column(df)
    """)     

    location.code("""
Index         0.0 MB
addresses    7.58 MB
ints          0.1 MB
floats       0.38 MB
dates        0.76 MB
currency     0.19 MB
category      0.2 MB
dtype: object

Total Memory Used: 9.209999999999999 MB
    """)     

    location.markdown("The DataFrame started off using 36 MB and now it uses just 9 MB. Thanks for reading.")

    location.markdown("### Resources")

    location.write(
        """
    * [Practical Business Python - Overview of Pandas Data Types](https://pbpython.com/pandas_dtypes.html)
    * [Dataquest - https://www.dataquest.io/blog/pandas-big-data/](https://www.dataquest.io/blog/pandas-big-data/)    
"""
    )




