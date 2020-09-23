"""
Setting up the defaults for nice Bokeh plots.

NOTE: Works, but may become deprecated due to migration to plotly.
"""

import holoviews as hv
from bokeh.themes.theme import Theme
from holoviews import opts
from . import themes


class HoloviewsBokeh(themes.HoloviewsCommon):
    """ Restyling functionality for the Bokeh backend. """

    @classmethod
    def build_theme(cls, theme):

        bokeh_settings = themes.THEME_MAP[theme]

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
                    'major_label_text_font_size': bokeh_settings.FONT_SIZE_SPEC,
                    'axis_label_standoff': 10,
                    'axis_label_text_color': bokeh_settings.COLOR_TEXT,
                    'axis_label_text_font': bokeh_settings.FONT,
                    'axis_label_text_font_size': bokeh_settings.FONT_SIZE_SPEC,
                    'axis_label_text_font_style': 'normal',
                },
                'Plot': {
                    'background_fill_color': bokeh_settings.COLOR_BACKGROUND,
                },
                'Grid': {
                    'grid_line_color': bokeh_settings.COLOR_LINES},
                'Legend': {
                    'label_text_font': bokeh_settings.FONT,
                    'label_text_font_size': bokeh_settings.FONT_SIZE_SPEC,
                    'spacing': 2,
                    'label_text_color': bokeh_settings.COLOR_TEXT,
                    'border_line_color': bokeh_settings.COLOR_LINES,
                    'background_fill_color': bokeh_settings.COLOR_BACKGROUND},
                'ColorBar': {
                    'title_text_color': bokeh_settings.COLOR_TEXT,
                    'title_text_font': bokeh_settings.FONT,
                    'title_text_font_size': bokeh_settings.FONT_SIZE_SPEC,
                    'title_text_font_style': 'normal',
                    'major_label_text_color': bokeh_settings.COLOR_TEXT,
                    'major_label_text_font': bokeh_settings.FONT,
                    'major_label_text_font_size': bokeh_settings.FONT_SIZE_SPEC,
                    'major_tick_line_alpha': 0,
                    'background_fill_alpha': 0.0,
                    #'background_fill_color': "#00ff00",
                    'bar_line_alpha': 1.0},
                'Title': {
                    'text_color': bokeh_settings.COLOR_TEXT,
                    'text_font': bokeh_settings.FONT,
                    'text_font_size': bokeh_settings.FONT_SIZE_SPEC
                }}}
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

    @classmethod
    def set_theme(cls, theme: themes.LayoutTheme=themes.LayoutTheme.DARK):
        """
        Activate restyling of Bokeh plots. A more minimal style comparable to plotly.
        :param theme:
        """
        hv.extension('bokeh')
        hv.renderer('bokeh').theme = Theme(json=cls.build_theme(theme))
        cls.set_defaults()

