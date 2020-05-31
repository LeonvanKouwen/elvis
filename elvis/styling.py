"""
Restyling of plotting backends.
Currently only the Bokeh backend in combination with holoviews is used.
"""

import holoviews as hv
from bokeh.themes.theme import Theme
from holoviews import dim, opts
from .constants import LayoutTheme


class ThemeSettingsLight():
    COLOR_LINES = "#ffffff"
    COLOR_BACKGROUND = "#f3f4f2"
    COLOR_TEXT = "#6B6B6B"
    FONT = "Helvetica"
    FONT_SIZE = "1.2em"


class ThemeSettingsDark():
    COLOR_LINES = "#3c4033"
    COLOR_BACKGROUND = None
    COLOR_TEXT = "#aaaaaa"
    FONT = "Helvetica"
    FONT_SIZE = "1.2em"


THEME_MAP = {LayoutTheme.DARK: ThemeSettingsDark,
             LayoutTheme.LIGHT: ThemeSettingsLight}


class Bokeh():
    """ Restyling functionality for the Bokeh backend. """

    @classmethod
    def style(cls, theme):

        bokeh_settings = THEME_MAP[theme]

        return {
            'attrs': {
                'Figure': {
                    #'toolbar_location': None,
                    'outline_line_width': 0,
                    'outline_line_color': None,
                    'min_border_right': 10,
                    'border_fill_color': None,
                    'sizing_mode': 'stretch_width'},
                'Axis': {
                    #'major_tick_line_alpha': 0,
                    'major_tick_line_color': None,
                    'minor_tick_line_color': None,
                    #'axis_line_alpha': 0,
                    'axis_line_color': None,
                    'major_label_text_color': bokeh_settings.COLOR_TEXT,
                    'major_label_text_font': bokeh_settings.FONT,
                    'major_label_text_font_size': bokeh_settings.FONT_SIZE,
                    'axis_label_standoff': 10,
                    'axis_label_text_color': bokeh_settings.COLOR_TEXT,
                    'axis_label_text_font': bokeh_settings.FONT,
                    'axis_label_text_font_size': bokeh_settings.FONT_SIZE,
                    'axis_label_text_font_style': 'normal',
                },
                'Plot': {
                    'background_fill_color': bokeh_settings.COLOR_BACKGROUND,
                },
                'Grid': {
                    'grid_line_color': bokeh_settings.COLOR_LINES},
                'Legend': {
                    'label_text_font': bokeh_settings.FONT,
                    'label_text_font_size': bokeh_settings.FONT_SIZE,
                    'spacing': 2,
                    'label_text_color': bokeh_settings.COLOR_TEXT,
                    'border_line_color': bokeh_settings.COLOR_LINES,
                    'background_fill_color': bokeh_settings.COLOR_BACKGROUND},
                # 'ColorBar': {
                #     'title_text_color': '#5B5B5B',
                #     'title_text_font': 'Helvetica',
                #     'title_text_font_size': '1.025em',
                #     'title_text_font_style': 'normal',
                #     'major_label_text_color': '#5B5B5B',
                #     'major_label_text_font': 'Helvetica',
                #     'major_label_text_font_size': '1.025em',
                #     'major_tick_line_alpha': 0,
                #     'bar_line_alpha': 0},
                'Title': {
                    'text_color': bokeh_settings.COLOR_TEXT,
                    'text_font': bokeh_settings.FONT,
                    'text_font_size': bokeh_settings.FONT_SIZE}}}
            # This doesn't work yet, but suposedly will soon.
            #         'LineGlyph': {'line_color': '#ee33ee', 'line_width': 2},
            #         'FillGlyph': {'fill_color': 'orange'},
            #         'HatchGlyph': {'hatch_pattern': '@', 'hatch_alpha': 0.8},
            #         'TextGlyph': {
        #             'text_color': 'red',
        #             'text_font_style': 'bold',
        #             'text_font': 'Helvetica',
        #         },
        #         'Ellipse': {'fill_color': 'green', 'line_color': 'yellow', 'fill_alpha': 0.2},

    DEFAULT_POINT_OPTS = {
        'show_grid': True,
        'size': 8,
        'fill_color': '#ffffff',
        'line_width': 2,
#       'toolbar': 'above',
#       'legend_position': 'right'
    }

    DEFAULT_PLOT_OPTS = {
        'show_grid': True,
        'line_width': 2,
        'responsive': True
    }

    @classmethod
    def set_elvis_style(cls, theme: LayoutTheme=LayoutTheme.DARK):
        """
        Activate restyling of Bokeh plots. A more minimal style comparable to plotly.
        :param theme:
        """
        hv.extension('bokeh')
        hv.renderer('bokeh').theme = Theme(json=cls.style(theme))
        cls.curve_defaults()
        cls.points_defaults()

    @classmethod
    def curve_defaults(cls, **kwargs):
        """
        Set defaults for holoviews Curve class. Use kwargs to overwrite elvis defaults
        and set user-specific defaults
        """
        return opts.defaults(opts.Curve(**_dict_merge(kwargs, cls.DEFAULT_PLOT_OPTS)))

    @classmethod
    def points_defaults(cls, **kwargs):
        """
          Set defaults for holoviews Points class. Use kwargs to overwrite elvis defaults
          and set user-specific defaults
          """
        return opts.defaults(opts.Points(**_dict_merge(kwargs, cls.DEFAULT_POINT_OPTS)))


def _dict_merge(dominant, recessive):
    """
    Combines the two dicts. In case of duplicate keys,
    the values of 'dominant' are used.
    """
    for key, value in recessive.items():
        dominant[key] = dominant.setdefault(key, value)
    return dominant