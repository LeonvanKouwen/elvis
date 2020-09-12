"""
Combining holoviz panel with the golden-panel layout.
See README.md for set-up instructions.
"""

from .goldenpanel import GoldenPanel
from .bokeh import HoloviewsBokeh
from .plotly import HoloviewsPlotly
from .streaming import LiveComputation, LivePlot
import elvis.widgets
from .themes import LayoutTheme
