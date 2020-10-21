import plotly.graph_objects as go
import plotly.io as pio
from . import themes
import holoviews as hv


class HoloviewsPlotly(themes.HoloviewsCommon):
    """ Restyling functionality for the plotly backend. """

    @classmethod
    def set_theme(cls, theme: themes.LayoutTheme=themes.LayoutTheme.DARK):
        """
        Activate restyling of Plotly plots.
        """
        hv.extension('plotly')
        pio.templates["elvis"] = go.layout.Template(layout=cls.build_layout(theme))
        pio.templates.default = "elvis"
        cls.set_defaults()
        cls.scatter3d_defaults()


    @classmethod
    def build_layout(cls, theme):
        t =  themes.THEME_MAP[theme]

        return  {
            'height': 800,
            'autosize': True,
            'margin': {'l': 5, 'r': 5,'b': 5, 't': 5, 'pad': 0},
            'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1},
            'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
            'colorscale': {'diverging': [[0, '#8e0152'], [0.1, '#c51b7d'], [0.2,
                                         '#de77ae'], [0.3, '#f1b6da'], [0.4, '#fde0ef'],
                                         [0.5, '#f7f7f7'], [0.6, '#e6f5d0'], [0.7,
                                         '#b8e186'], [0.8, '#7fbc41'], [0.9, '#4d9221'],
                                         [1, '#276419']],
                           'sequential': [[0.0, '#0d0887'], [0.1111111111111111,
                                          '#46039f'], [0.2222222222222222, '#7201a8'],
                                          [0.3333333333333333, '#9c179e'],
                                          [0.4444444444444444, '#bd3786'],
                                          [0.5555555555555556, '#d8576b'],
                                          [0.6666666666666666, '#ed7953'],
                                          [0.7777777777777778, '#fb9f3a'],
                                          [0.8888888888888888, '#fdca26'], [1.0,
                                          '#f0f921']],
                           'sequentialminus': [[0.0, '#0d0887'], [0.1111111111111111,
                                               '#46039f'], [0.2222222222222222, '#7201a8'],
                                               [0.3333333333333333, '#9c179e'],
                                               [0.4444444444444444, '#bd3786'],
                                               [0.5555555555555556, '#d8576b'],
                                               [0.6666666666666666, '#ed7953'],
                                               [0.7777777777777778, '#fb9f3a'],
                                               [0.8888888888888888, '#fdca26'], [1.0,
                                               '#f0f921']]},
            'colorway': ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692',
                         '#B6E880', '#FF97FF', '#FECB52'],
            'font': {'color': t.COLOR_TEXT, 'size': t.FONT_SIZE},
            'geo': {'bgcolor': t.COLOR_BACKGROUND,
                    'lakecolor': 'white',
                    'landcolor': '#E5ECF6',
                    'showlakes': True,
                    'showland': True,
                    'subunitcolor': 'white'},
            'hoverlabel': {'align': 'left'},
            'hovermode': 'closest',
            'mapbox': {'style': 'light'},
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': t.COLOR_BACKGROUND,
            'polar': {'angularaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
                      'bgcolor': '#E5ECF6',
                      'radialaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}},
            'scene': {'xaxis': {'backgroundcolor': t.COLOR_BACKGROUND,
                                'gridcolor': t.COLOR_LINES,
                                'gridwidth': 2,
                                'linecolor': t.COLOR_LINES,
                                'showbackground': True,
                                'ticks': '',
                                'zerolinecolor': t.COLOR_LINES},
                      'yaxis': {'backgroundcolor': t.COLOR_BACKGROUND,
                                'gridcolor': t.COLOR_LINES,
                                'gridwidth': 2,
                                'linecolor': t.COLOR_LINES,
                                'showbackground': True,
                                'ticks': '',
                                'zerolinecolor': t.COLOR_LINES},
                      'zaxis': {'backgroundcolor': t.COLOR_BACKGROUND,
                                'gridcolor': t.COLOR_LINES,
                                'gridwidth': 2,
                                'linecolor': t.COLOR_LINES,
                                'showbackground': True,
                                'ticks': '',
                                'zerolinecolor': t.COLOR_LINES}},
            'shapedefaults': {'line': {'color': '#2a3f5f'}},
            'ternary': {'aaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
                        'baxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
                        'bgcolor': '#E5ECF6',
                        'caxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}},
            'title': {'x': 0.05},
            'xaxis': {'automargin': True,
                      'gridcolor': t.COLOR_LINES,
                      'linecolor': t.COLOR_LINES,
                      'ticks': '',
                      'title': {'standoff': 15},
                      'zerolinecolor': t.COLOR_LINES,
                      'zerolinewidth': 2},
            'yaxis': {'automargin': True,
                      'gridcolor': t.COLOR_LINES,
                      'linecolor': t.COLOR_LINES,
                      'ticks': '',
                      'title': {'standoff': 15},
                      'zerolinecolor': t.COLOR_LINES,
                      'zerolinewidth': 2,
                      # 'scaleanchor':"x",
                      # 'scaleratio':1
                      }

        }



