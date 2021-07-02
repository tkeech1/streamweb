import streamlit as st
import datetime
import pytz
import pandas as pd
import numpy as np
import glob
import timeit
import jinja2
from utils.metrics import log_runtime

short_title = "Concatenating CSV Files"
long_title = "Concatenating CSV Files"
key = 1
content_date = datetime.datetime(2021, 4, 15).astimezone(pytz.timezone("US/Eastern"))
output_dir = "./tmp/1/"


def file_aggregation_pandas(aggregated_file: str, num_files: int) -> None:
    header = True
    source_files = [i for i in sorted(glob.glob(f"{output_dir}*.csv"))][0:num_files]

    for file in source_files:
        df = pd.read_csv(f"{file}")
        if header:
            df.to_csv(f"{aggregated_file}", index=False)
            header = False
        else:
            df.to_csv(f"{aggregated_file}", index=False, mode="a", header=False)


def file_aggregation_pandas_concat(aggregated_file: str, num_files: int) -> None:
    source_files = [i for i in sorted(glob.glob(f"{output_dir}*.csv"))][0:num_files]

    df_list = []
    for filename in source_files:
        df_list.append(pd.read_csv(filename))
    pd.concat(df_list).to_csv(f"{aggregated_file}", index=False)


def file_aggregation_fileio(aggregated_file: str, num_files: int) -> None:
    source_files = [i for i in sorted(glob.glob(f"{output_dir}*.csv"))][0:num_files]

    with open(f"{aggregated_file}", "wb") as fout:
        with open(source_files[0], "rb") as fin:
            fout.write(fin.read())
        for file in source_files[1:]:
            with open(file, "rb") as fin:
                next(fin)
                fout.write(fin.read())


def file_aggregation_linux() -> None:
    import subprocess

    subprocess.call(f"{output_dir}linux_agg.sh")


@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(content_date)

    location.markdown(
        " File "
        "concatenation is a common problem in time series data "
        "where a process generates output files on a "
        "periodic basis. To trend data over a larger time window, "
        "you may need to combine data from multiple files "
        "into a single file. "
        "There are a few options to consider when you need to "
        "combine many files into a single large file. "
        "Depending on the number and size of the files, "
        "performance might be a concern. "
    )
    location.markdown(
        "In this post, we'll compare the performance of a few different approaches "
        "for concatenating CSV files. All of the examples can be copied to a "
        "Jupyter notebook for testing. The examples are also available HERE. "
    )

    location.markdown(
        "Since this post runs in [Streamlit](http://streamlit.io), the code that executes "
        "when you click `Run It!` is slightly different from what's displayed. "
        "Instead of using the `%timeit` magic, the interactive code uses direct calls to the timeit module. "
        "The performance numbers reported in this post will vary from what you'll see when you run it in a Jupyter notebook "
        "on your local machine. "
    )

    location.markdown("---")

    location.markdown("### Setup")

    # col1, col2 = location.beta_columns((1, 1))

    location.markdown(
        "Let's begin by generating some test data. "
        "We'll generate files containing a timestamp column and a single column of randomly generated data. "
        "Columns are labeled with a header. The concatenated "
        "file should have a single header so we’ll need to strip the headers "
        "when we process the files. This code generates 2 MB files, each with a unique filename."
    )

    location.markdown(
        "Since this is an interactive blog post, you can decide how many files you want to generate. "
        "It's interesting (and sometimes surprising) to compare the run times for each file aggregation approach for  "
        "differing numbers of input files."
    )

    file_num_selectbox = location.selectbox(
        "How many files do you want to generate?", (2, 5, 10)
    )

    test_data_code_template = jinja2.Template(
        """
import pandas as pd
import numpy as np
import datetime

row_date = datetime.date(2021, 1, 1)
rows_per_file = 86_400
files_to_generate = {{ files_to_generate }}

for i in range(files_to_generate):
    datetime_index = pd.date_range(row_date, periods=rows_per_file, freq="s")    
    df = pd.DataFrame(index=datetime_index)
    df['data'] = np.random.randint(0,999999, size=rows_per_file)    
    df.to_csv(f'{i}.csv', index_label='datetime')
    row_date = row_date + datetime.timedelta(seconds=rows_per_file)
"""
    )

    location.code(
        test_data_code_template.render(files_to_generate=file_num_selectbox),
        language="python",
    )

    gen_data_message = location.empty()
    file_gen_bar = location.progress(0)

    if location.button("Generate Test Data"):
        file_gen_bar.progress(0)
        gen_data_message.markdown("`Generating test data...`")

        row_date = datetime.date(2021, 1, 1)
        rows_per_file = 86_400
        files_to_generate = 3

        for i in range(file_num_selectbox):

            datetime_index = pd.date_range(row_date, periods=rows_per_file, freq="s")
            df = pd.DataFrame(index=datetime_index)
            df["data"] = np.random.randint(0, 999999, size=rows_per_file)
            df.to_csv(f"{output_dir}{i}.csv", index_label="datetime")
            row_date = row_date + datetime.timedelta(seconds=rows_per_file)
            file_gen_bar.progress((i + 1) + (100 // files_to_generate))

        file_gen_bar.progress(100)
        gen_data_message.markdown("`Generating test data... Done.`")

        location.markdown("Here's one of the files you just generated.")

        data = pd.read_csv(f"{output_dir}0.csv", nrows=3)
        location.write(data)

    location.markdown("---")

    location.markdown("### Pandas")

    # pandas_append_code_col1, pandas_append_code_col2 = location.beta_columns((1, 1))

    location.markdown(
        "We'll look at two different methods for aggregating CSV files using [Pandas](https://pandas.pydata.org/). "
        "The first approach uses Python's append file mode to append data to a CSV file. "
        "The `file_aggregation_pandas` function reads each file sequentially. Upon reading the first file, the function "
        "writes the entire file, including the header, to the aggregate file. "
        "For subsequent files, the function writes the file excluding the header. "
    )

    location.markdown(
        "The `mode='a'` parameter of the `to_csv` function works similary to the `mode` parameter of the `open()` built-in function. "
        "Using the `mode` parameter, files can be opened in read-only, append, write, or a combination of modes. The `mode` parameter also "
        "supports reading text or binary files."
    )

    location.markdown(
        "Let's run the function using the `%timeit` magic command. "
        "`timeit` is part of the Python standard library and provides a simple way to time small blocks of Python code. "
        "The `%timeit` line magic allows us to run timeit for a single command in a Jupyter notebook. You "
        " can use the `%%timeit` cell magic to time the execution of an entire notebook cell. "
    )

    location.code(
        """
import glob

def file_aggregation_pandas(source_files:str, aggregate_file:str) -> None:
    header = True
    source_files = [i for i in sorted(glob.glob(source_files))]

    for file in source_files:
        df = pd.read_csv(file)
        if header:
            df.to_csv(aggregate_file, index=False)
            header = False
        else:
            df.to_csv(aggregate_file, index=False, mode="a", header=False)
        """,
        language="python",
    )

    # pandas_append_run_col1, pandas_append_run_col2 = location.beta_columns((1, 1))

    location.markdown(
        "Here, we'll time how long it takes the `file_aggregation_pandas` function. "
        "In performance analysis, it's usually best to time the execution of multiple runs "
        "since a single execution can be affected by other processes running on the machine. "
        " The `-r` switch tells `timeit` to repeat 2 times. the `-n` switch tells `timeit` to execute the function 3 times per run. "
    )

    location.markdown(
        "One more thing... I've taken then advice of the timeit authors and I'm reporting the minimum runtime of the function when you click `Run It`. "
        "From the [Python docs](https://docs.python.org/3/library/timeit.html):"
    )

    location.markdown(
        '"It’s tempting to calculate mean and standard deviation from the result vector and report these. '
        "However, this is not very useful. In a typical case, the lowest value gives a lower bound for how "
        "fast your machine can run the given code snippet; higher values in the result vector are typically "
        "not caused by variability in Python’s speed, but by other processes interfering with your timing "
        "accuracy. So the min() of the result is probably the only number you should be interested in. "
        'After that, you should look at the entire vector and apply common sense rather than statistics."'
    )

    location.code(
        """
%timeit -r 2 -n 3 file_aggregation_pandas('*.csv', 'aggregated_pandas.csv_')
    """
    )

    pandas_append_run_message = location.empty()
    append_bar = location.progress(0)

    if location.button("Run It!", key=1):
        pandas_append_run_message.markdown(f"`Running... `")
        append_bar.progress(0)

        r = 2
        n = 3

        results = []
        for i in range(r):
            results.append(
                timeit.repeat(
                    stmt='file_aggregation_pandas(f"{output_dir}pandas.csv_", file_num_selectbox)',
                    repeat=1,
                    number=n,
                    globals=dict(globals(), **locals()),
                )
            )
            append_bar.progress((i + 1) * (100 // r))

        append_bar.progress(100)

        append_min_time = min(results[0]) / n
        for item in results:
            if min(item) < append_min_time:
                append_min_time = min(item) / n

        location.markdown(
            f"`Running... done. Minimum run time {round(append_min_time,4)} seconds. `"
        )

    location.markdown("---")

    # pandas_concat_code_col1, pandas_concat_code_col2 = location.beta_columns((1, 1))

    location.markdown(
        "An alternative is to use Pandas' `concat()` method. The benefit"
        " of `concat()` is that we don't have to include any logic for "
        " handling the header. `concat()` handles that for us. "
    )

    location.code(
        """
import glob

def file_aggregation_pandas_concat(source_files:str, aggregate_file:str) -> None:    
    source_files = [i for i in sorted(glob.glob(source_files))]
    
    df_list = []
    for filename in source_files:
        df_list.append(pd.read_csv(filename))
    pd.concat(df_list).to_csv(aggregate_file, index=False)
    """
    )

    # pandas_concat_run_col1, pandas_concat_run_col2 = location.beta_columns((1, 1))

    pandas_concat_run_message = location.empty()
    concat_bar = location.progress(0)

    if location.button("Run It!", key=2):
        location.markdown(f"`Running... `")
        concat_bar.progress(0)

        r = 2
        n = 3

        results = []
        for i in range(r):
            results.append(
                timeit.repeat(
                    stmt='file_aggregation_pandas_concat(f"{output_dir}pandas.csv_",file_num_selectbox)',
                    repeat=1,
                    number=n,
                    globals=dict(globals(), **locals()),
                )
            )
            concat_bar.progress((i + 1) * (100 // r))

        concat_bar.progress(100)

        append_min_time = min(results[0]) / n
        for item in results:
            if min(item) < append_min_time:
                append_min_time = min(item) / n

        location.markdown(
            f"`Running... done. Minimum run time {round(append_min_time,4)} seconds. `"
        )

    location.markdown(
        "Although both Pandas approaches have similar run times, there's a significant difference "
        "in memory utilization. If you're running on a machine that's memory-constrained, this "
        "this could make a huge difference in run time."
    )

    location.code(
        """
%timeit -r 2 -n 3 file_aggregation_pandas_concat('*.csv', 'aggregated_pandas.csv_')
"""
    )

    location.markdown("---")

    location.markdown("### Pandas Memory Usage")

    # pandas_memory_code_col1, pandas_memory_code_col2 = location.beta_columns((1, 1))

    location.markdown(
        "We can use the `memory-profiler` package to explore memory usage (`pip install memory-profiler`). "
        "If you're using iPython or a Jupyter notebook, `memory-profiler` can be invoked through "
        "the `%mprun` magic command. "
        "Before we can use `%mprun`, we need to "
        "modify the function code to create a Python module. We can do that using the `%%file` magic which simply takes "
        "all of the code in the cell and writes it to a local file. "
    )

    location.code(
        """
%%file pandas_append.py

import numpy as np
import pandas as pd
import glob

def file_aggregation_pandas(source_files:str, aggregate_file:str) -> None:
    header = True
    source_files = [i for i in sorted(glob.glob(source_files))]

    for file in source_files:
        df = pd.read_csv(file)
        if header:
            df.to_csv(aggregate_file, index=False)
            header = False
        else:
            df.to_csv(aggregate_file, index=False, mode="a", header=False)
    """
    )

    # pandas_memory_run_col1, pandas_memory_run_col2 = location.beta_columns((1, 1))

    location.markdown(
        "Once we've written the cell content to a file, we can load the module and then run `%mprun` as shown. "
        "Make sure you load `mprun` using the `%load_ext memory_profiler` command first."
    )

    location.code(
        """
%load_ext memory_profiler
from pandas_append import file_aggregation_pandas

%mprun -f file_aggregation_pandas file_aggregation_pandas('*.csv', 'aggregated_pandas.csv_')
    """
    )

    location.markdown(
        "To get a feel for "
        "memory utilization, I ran `%mprun` over 100, 2MB CVS files. "
        "The file-append approach maxed-out at about 164 MB of memory usage. "
    )

    location.code(
        """
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
     6    117.3 MiB    117.3 MiB           1   def file_aggregation_pandas(source_files:str, aggregate_file:str) -> None:
     7    117.3 MiB      0.0 MiB           1       header = True
     8    117.3 MiB      0.0 MiB         103       source_files = [i for i in sorted(glob.glob(source_files))]
     9                                         
    10    164.4 MiB   -347.7 MiB         101       for file in source_files:
    11    164.4 MiB   -308.8 MiB         100           df = pd.read_csv(file)
    12    164.4 MiB   -351.0 MiB         100           if header:
    13    129.4 MiB      2.0 MiB           1               df.to_csv(aggregate_file, index=False)
    14    129.4 MiB      0.0 MiB           1               header = False
    15                                                 else:
    16    164.4 MiB   -344.8 MiB          99               df.to_csv(aggregate_file, index=False, mode="a", header=False)
    """
    )

    location.markdown(
        "The `concat()` approach maxed-out at 912 MB of memory usage. In line 11 below, you can see "
        "there's significant overhead in storing 100 Pandas DataFrames in a single list. Essentially, all 100 CSV files "
        "are being loaded into memory at once. This differs from the append approach where each file is read into memory then "
        "immediately written to disk. "
    )

    location.code(
        """
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
     6    296.3 MiB    296.3 MiB           1   def file_aggregation_pandas_concat(source_files:str, aggregate_file:str) -> None:    
     7    296.3 MiB      0.0 MiB         103       source_files = [i for i in sorted(glob.glob(source_files))]
     8                                             
     9    296.3 MiB      0.0 MiB           1       df_list = []
    10    885.4 MiB      0.0 MiB         101       for filename in source_files:
    11    885.4 MiB    588.6 MiB         100           df_list.append(pd.read_csv(filename))
    12    912.8 MiB     27.4 MiB           1       pd.concat(df_list).to_csv(aggregate_file, index=False)
    """
    )

    location.markdown("### File IO")

    # fileio_code_col1, fileio_code_col2 = location.beta_columns((1, 1))

    location.markdown(
        "I like Pandas but it's not always necessary. To concatenate CSV files, we don't really need a DataFrame "
        "object. We can avoid the overhead associated with parsing CSVs into DataFrames. "
        "Instead of using Pandas, we can use simple Python file operations. "
    )

    location.markdown(
        "The `file_aggregation_fileio` function reads each CSV file in binary mode, "
        "writes the header from the first file, then writes the remaining lines for all CSV files. "
        "It uses standard Python file operations which are written in C and have very good performance. "
    )

    location.code(
        """
import glob

def file_aggregation_fileio(source_files:str, aggregate_file: str) -> None:
    source_files = [i for i in glob.glob(source_files)]

    with open(aggregate_file, "wb") as fout:
        with open(source_files[0], "rb") as fin:
            fout.write(fin.read())
        for file in source_files[1:]:
            with open(file, "rb") as fin:
                next(fin)
                fout.write(fin.read())
"""
    )

    # fileio_run_col1, fileio_run_col2 = location.beta_columns((1, 1))

    location.code(
        """
%timeit -r 2 -n 3 file_aggregation_fileio('*.csv', 'aggregated_fileio.csv_')
"""
    )

    fileio_run_message = location.empty()
    fileio_bar = location.progress(0)

    if location.button("Run It!", key=3):
        fileio_run_message.markdown(f"`Running... `")
        fileio_bar.progress(0)

        r = 2
        n = 3

        results = []
        for i in range(r):
            results.append(
                timeit.repeat(
                    stmt='file_aggregation_fileio(f"{output_dir}aggregated_fileio.csv_",file_num_selectbox)',
                    repeat=1,
                    number=n,
                    globals=dict(globals(), **locals()),
                )
            )
            fileio_bar.progress((i + 1) * (100 // r))

        fileio_bar.progress(100)

        append_min_time = min(results[0]) / n
        for item in results:
            if min(item) < append_min_time:
                append_min_time = min(item) / n

        location.markdown(
            f"`Running... done. Minimum run time {round(append_min_time,4)} seconds. `"
        )

    location.markdown(
        "The `file_aggregation_fileio` function is significantly faster than Pandas because each row doesn't need to be parsed as "
        "a DataFrame. "
    )

    location.markdown(
        "When run on 100 files, memory usage is also far less that the Pandas versions."
    )

    location.code(
        """
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
     4     91.1 MiB     91.1 MiB           1   def file_aggregation_fileio(source_files:str, aggregate_file: str) -> None:
     5     91.1 MiB      0.0 MiB         103       source_files = [i for i in glob.glob(source_files)]
     6                                         
     7     91.1 MiB      0.0 MiB           1       with open(aggregate_file, "wb") as fout:
     8     91.1 MiB      0.0 MiB           1           with open(source_files[0], "rb") as fin:
     9     91.1 MiB      0.0 MiB           1               fout.write(fin.read())
    10     91.1 MiB      0.0 MiB         100           for file in source_files[1:]:
    11     91.1 MiB   -180.7 MiB          99               with open(file, "rb") as fin:
    12     91.1 MiB   -180.7 MiB          99                   next(fin)
    13     89.3 MiB   -182.5 MiB          99                   fout.write(fin.read())
    """
    )

    location.markdown("### Linux Tools")

    # linux_code_col1, linux_code_col2 = location.beta_columns((1, 1))

    location.markdown(
        "Another alternative is to use Linux OS tools to perform file concatenation. "
        "Many Linux tools are highly optimized and can make use of the multiple "
        "cores and processors found on modern machines. If you don't mind writing a little bash, "
        "you may be able to squeeze out even more performance depending on the number and size of your "
        "files. "
    )

    location.code(
        """
%%timeit -r 2 -n 3

%%bash

head -n 1 0.csv > aggregated_linux.csv_
for FILE in *.csv; do 
    tail -n +2 "$FILE" 
done >> aggregated_linux.csv_
"""
    )

    # linux_run_col1, linux_run_col2 = location.beta_columns((1, 1))

    linux_run_message = location.empty()
    linux_bar = location.progress(0)

    if location.button("Run It!", key=4):
        linux_run_message.markdown(f"`Running... `")
        linux_bar.progress(0)

        r = 2
        n = 3

        results = []
        for i in range(r):
            results.append(
                timeit.repeat(
                    stmt="file_aggregation_linux()",
                    repeat=1,
                    number=n,
                    globals=dict(globals(), **locals()),
                )
            )
            linux_bar.progress((i + 1) * (100 // r))

        linux_bar.progress(100)

        append_min_time = min(results[0]) / n
        for item in results:
            if min(item) < append_min_time:
                append_min_time = min(item) / n

        location.markdown(
            f"`Running... done. Minimum run time {round(append_min_time,4)} seconds. `"
        )

    location.markdown(
        "Unfortunately, running a bash script through Python incurs some overhead that wouldn't normally be present "
        "if you were running the script from the command line. Even so, The Linux tools approach seems "
        "to perform much better than the Python file operations for more than a handful of files. "
    )

    location.markdown("### Unscientific Results")

    location.markdown(
        "Here's a summary of the results when running on my local machine. Your results may vary. "
    )

    results_df = pd.DataFrame(
        {
            "Files": [2, 5, 10],
            "Pandas append": [0.338, 0.811, 1.624],
            "Pandas concat()": [0.346, 0.896, 2.083],
            "Python file operations": [0.023, 0.071, 0.213],
            "Linux tools": [0.052, 0.055, 0.062],
        }
    )

    location.write(results_df)

    from bokeh.plotting import figure

    # prepare some data
    x = results_df["Files"]
    y1 = results_df["Pandas append"]
    y2 = results_df["Pandas concat()"]
    y3 = results_df["Python file operations"]
    y4 = results_df["Linux tools"]

    # create a new plot with a title and axis labels
    p = figure(
        title="File Aggregation Run Times",
        x_axis_label="Number of Files",
        y_axis_label="Run Time",
    )

    # add multiple renderers
    p.line(x, y1, legend_label="Pandas append", line_color="blue", line_width=2)
    p.line(x, y2, legend_label="Pandas concat()", line_color="red", line_width=2)
    p.line(
        x, y3, legend_label="Python file operations", line_color="purple", line_width=2
    )
    p.line(x, y4, legend_label="Linux tools", line_color="green", line_width=2)

    location.bokeh_chart(p, use_container_width=False)

    location.markdown("### Conclusion")

    location.markdown(
        "Clearly, Linux tools are the winner of this unscientific test. "
        "Python file operations are not far behind. "
        "Although, in this case, the Linux tools approach isn't overly complicated, some would argue that you "
        "lose the readability and maintainability that Python offers. "
        "As with all performance analysis, you need to test and profile on your specific "
        "dataset to determine which approach is right for you. "
    )
