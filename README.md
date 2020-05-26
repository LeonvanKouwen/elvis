* Tag-line: Combining holoviz panel with the golden-panel layout.
* Author: Leon van Kouwen, lvankouwen@gmail.com
* Last updated: 21-5-2020
* Version 0.1.0

## About elvis

Elvis is primarily intended to enable using all the features of [panel](https://panel.holoviz.org/)
in combination with the [golden-layout](http://golden-layout.com/), in a way that
it can be setup entirely from simple python commands. This enables a nice looking and flexible dashboard
being setup very quickly, while having all the otions of python at ones disposal. 

In addition, this package is a collection of somewhat arbitrary
additions to panel. Current functionality includes
* Golden layout combined with panel from pure python
* Altered styling of golden-layout (dark and light theme)
* A KPI widget matching the theme.
* Re-styling of bokeh graphs.
* A-synchronous live calculation and live plotting.

NOTE: this package under developement and experimental. Some of the solutions
are probably not very scalable/maintainable.
In particular the a-synchronous live calculation and live plotting isn't what
it could be. I encourage contributions, suggestions, advice, refactor efforts, ... :).

Feel free to use this for any purpose, within the limits of the licenses of panel and golden-layout.
If you make improvements or additions I kindly ask you to share them. This can be done by adding
them to this repository, or other channels like a blog. Feel free to contact me.

### Impression

![Dark-Theme Demo](demos/demo-dark-param.gif)
![Light-Theme Demo](demos/demo-light-live.gif)

## How do I get set up?

### Installation
From the directory in which the package folder is located use the following command to install:

    pip install elvis

It is now possible to remove the elvis folder. To install in developers mode (changes to local
elvis files are active)

    pip install -e elvis

At present it is required do use a developers install of panel. Follow the instructions
[here](https://panel.holoviz.org/developer_guide/index.html) and checkout in the branch
static_serve. Use the panel_dev conda environment. Note that this is only required temporarily,

as serving static assets will be included in the standard panel distribution at some point.

* panel 0.10.0a2.post9+g643033f dev_0

It is possible as a work-around to test this package without the developers install.
Don't pip install elvis but simply create a main.py (or move one of the examples) in the root
folder of the repository. Replace the default way of serving from the code

    gpanel.serve()

With

   gpanel.app.servable()

Now from the command line one directory level higher run:

   panel serve elvis

### Examples
To get started with some examples look at the examples folder.
- live_time_series shows the asynchronous live plotting functionality in the light theme
- science-dashboard shows the dark theme and some standard panel/param functionality.

### Future work

#### ToDo
- Fix reset button for streaming plots (resetting a holoviews object)
- Reset the server from a button in the browser
- Change size of the streaming plot (doesn't work)
- Refactor the streaming module
- Add docstrings
- The css is a mess; needs to be cleaned up

#### Wishlist
- Remove the 5px left-margin when generating widgets with param.
- A widget that shows stdout
- A global message widget
- Prevent overlapping hover pop-ups in Bokeh plots
