## Streamweb

Streamweb is a template for creating a blog or portfolio site based on [Steamlit](http://streamlit.io). Streamweb allows you to combine multiple Streamlit dashboards into a single web site. It also enables interactive blog posts that allow users to modify content using Streamlit widgets. Issues and PRs for improvements are welcome!

### Quickstart

#### Step 1: Clone the repo
    git clone https://github.com/tkeech1/streamweb
    cd streamweb

#### Step 2: Run Streamlit
    cd streamweb
    streamlit run layout_clean_sidebar.py

#### Step 3: Browse to http://localhost:8501/

### ocumentation

#### Layouts
The `streamweb` directory contains the entry point to the application. An application can have multiple layouts, although only one can be enabled at a time. The layout determines how content will be displayed on the main screen. A layout uses standard [Streamlit syntax](https://docs.streamlit.io/en/stable/api.html) (`st.write()`, `st.markdown()`, `st.title()`, etc.) to build the display.

Layouts are responsible for loading and displaying content. Content is stored separately (for the most part) from the layout although there are some conventions to which content must conform. These are covered in the *Content* section. 

##### Changing the layout
To change to a different layout, use a different layout file:
    
    streamlit run layout_clean_no_sidebar.py

##### Creating a new layout
To create a new layout, copy one of the existing layouts and add it to the `streamweb` directory. Then, run streamlit using the new layout as shown above. 

    streamlit run layout_my_new_layout.py

#### Content
Streamweb was built to mimic static site generators such as [Hugo](https://gohugo.io/). Content is stored in Python modules which are stored in Python packages under the `streamweb` directory on the filesystem; a database isn't necessary. In the examples, content is separated into two types, static content and dynamic content. Static content, stored in the `static` package, is intended for content that doesn't change frequently such as an "About Me" page. Dynamic content, stored in the `dynamic` package is intended for content that's updated frequently such as blog posts. Users can create new Python packages containing content under the `streamweb` and load them as described below.

##### Content Loading
In a layout, content modules are loaded by calling the `load_content('package_name')` function. This function returns a list of Python modules which can be iterated over and displayed in the layout.

In the example layouts, the content packages `static` and `dynamic` packages are loaded by the layout in the following lines. 

    static_content = load_content("static", environment)
    dynamic_content = load_content("dynamic", environment)

`environment` is a flag that indicates whether or not to dynamically reload content modules. If `environment=='prd'`, the dynamic content reloading is disabled. 

All content modules are cached using Streamlit's [st.cache()](https://docs.streamlit.io/en/stable/caching.html) decorator and are dynamically reloaded if the module changes. Dynamic reloading makes it easy to develop new content without having to restart Streamlit after each edit. Dynamic module reloading can be disabled by running Streamlit as shown below:
    
    streamlit run layouts/clean_no_sidebar.py -- prd

##### Creating New Content
A new content module can be created by copying and existing content module and renaming it. You need to restart Streamlit to load new content modules. 

##### Creating New Content Packages
To create a new content package, create a new directory under the `streamweb` directory. Create an `__init__.py` file inside the directory so Python knows it's a package. Then, create new content modules as noted above. 

To load the content inside a layout:

    my_new_content = load_content("mynewpackage")

##### Displaying Content
Once you've loaded module content, you can display the content by calling the render() function of the content module.

    my_new_content[i].render()

To display a list of button links to the content:

    button_click_flags = []
    for c in content:
        button_click_flags.append(st.button(c.short_title, key=c.key))

This creates a list, `button_click_flags`, of `bools` that indicate which button was clicked. Unfortunately, [Streamlit doesn't appear to support getting the key of the button that was clicked](https://discuss.streamlit.io/t/how-to-use-the-key-field-in-interactive-widgets-api/1007) so this is a workaround.

There are two helper methods for displaying content, `render_content_by_click` and `render_content_by_key`. Below is an example of rendering content based on a button click.

    if any(button_click_flags):
        render_content_by_click(
            content=my_new_content,
            button_click=button_click_flags,
            environment=environment,
        )

Here is an example of rendering content based on an content key.

    if content_id:
        render_content_by_key(
            content=my_new_content, content_key=content_id, environment=environment
        )

##### Content Format
Streamweb expects all content modules to contain the following attributes and functions:

###### Attributes
    short_title: A short title for the content (usually displayed in a link or button)
    long_title: A long title for the content (usually displayed as a page title)
    content_date: A Python date used for sorting content. By default content is sorted in date descending order (most recent posts appear at the top)
    key: A unique key used in URLs

###### Functions
    render(): Function containing standard Python code and Streamlit syntax for building the display

There are several examples of [dynamic](https://github.com/tkeech1/streamweb/tree/master/dynamic) and [static](https://github.com/tkeech1/streamweb/tree/master/static) content included in this repo. 

#### TODO
* UI tests
* Logging
* Sphinx docs