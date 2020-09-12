# Elvis

* Combining holoviz panel with the golden-panel layout.
* Author: Leon van Kouwen, lvankouwen@gmail.com
* Last updated: 12-09-2020
* Version 0.1.1

## About elvis

Elvis is primarily intended to enable using all the features of [panel](https://panel.holoviz.org/)
in combination with the [golden-layout](http://golden-layout.com/), in a way that
it can be setup entirely from simple python commands. This enables a nice looking and flexible dashboard
being setup very quickly, while having all the options of python at ones disposal. 

In addition, this package is a collection of somewhat arbitrary
additions to panel. Current functionality includes
* Golden layout combined with panel from pure python
* Altered styling of golden-layout (dark and light theme)
* A KPI widget matching the theme.
* Re-styling of bokeh graphs.
* A-synchronous live calculation and live plotting.

The .js code for golden-layout is included in this package such that the packge
can be used offline as well and to avoid problems when the online golden-layout resources
move or are no longer available. This means that the golden-layout code does not automatically follow
updates of golden-layout. 

NOTE: this package under development and experimental. Some of the solutions
are probably not very scalable/maintainable. In particular the a-synchronous 
live calculation and live plotting isn't what it could be. I am no longer 
using this functionality, but it is left here as code snippet inspiration. 
I appreciate suggestions, advice, contributions... :).

Feel free to use this for any purpose, within the limits of the licenses of panel and golden-layout.
If you make improvements or additions I kindly ask you to share them. This can be done by adding
them to this repository, or other channels like a blog. Feel free to contact me.

Some documentation is generated using pdoc3 and can be found in 'docs'.

### Impression

![Dark-Theme Demo](demos/demo-dark-param.gif)
![Light-Theme Demo](demos/demo-light-live.gif)

## How do I get set up?

### Installation
From the directory in which the package folder is located use the following command to install:

    pip install elvis

It is now possible to remove the elvis folder. To install in developers mode (changes to local
elvis files are active) use:

    pip install -e elvis

At present it is required do use a developers install of panel. Follow the instructions
[here](https://panel.holoviz.org/developer_guide/index.html). Note that this is only required
temporarily, as serving static assets will be included in the standard panel distribution at some point.
The panel version in which elvis is tested is:

* panel 0.10.0a2.post9+g643033f dev_0

### Examples
To get started with some examples look at the examples folder.
- live_time_series shows the asynchronous live plotting functionality in the light theme
- science-dashboard shows the dark theme and some standard panel/param functionality.

### Resources

This package is just a very thin layer around the holoviz framework and the golden layout GUI package. 
* [Holoviz](https://holoviz.org/)
* [Holoviz panel](https://panel.holoviz.org/)
* [Holoviz param](https://awesome-panel.org/)
* [Holoviz holoviews](https://holoviews.org/)
* [Golden-layout](https://golden-layout.com/)

A good comparison with other frameworks can be found [here](https://panel.holoviz.org/Comparisons.html).

As a plotting backend both Bokeh and plotly can be used, although currently there is a problem with vertical
responsiveness of plotly. Matloblib is not implemented due to the lack of interactive possibilities. 
* [Bokeh](https://bokeh.org/)
* [Plotly](https://plotly.com/)

For demonstrations and more additions to panel, visit
* [Awesome panel](https://awesome-panel.org/)

Combining panel with the golden-layout was inspired by the 
[VTKSlicer](https://panel.holoviz.org/gallery/demos/VTKSlicer.html#demos-gallery-vtkslicer) dashboard.

For bugs and problems with the code in this package, please raise a github issue. For more general questions, the
[holoviz discourse](https://discourse.holoviz.org/) can be used. 
