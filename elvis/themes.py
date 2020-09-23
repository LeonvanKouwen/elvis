from enum import Enum
import holoviews as hv
from holoviews import opts

class LayoutTheme(Enum):
    LIGHT = 'LIGHT'
    DARK = 'DARK'


class ThemeSettingsLight():
    COLOR_LINES = "#ffffff"
    COLOR_BACKGROUND = "#f3f4f2"
    COLOR_TEXT = "#6B6B6B"
    FONT = "Helvetica"
    FONT_SIZE = 18
    FONT_SIZE_SPEC = "18px"


class ThemeSettingsDark():
    COLOR_LINES = "#3c4033"
    COLOR_BACKGROUND = "rgba(0,0,0,0)"
    COLOR_TEXT = "#cccccc"
    FONT = "Helvetica"
    FONT_SIZE = 18
    FONT_SIZE_SPEC = "18px"


THEME_MAP = {LayoutTheme.DARK: ThemeSettingsDark,
             LayoutTheme.LIGHT: ThemeSettingsLight}


class HoloviewsCommon():

    DEFAULT_POINT_OPTS = {
        'show_grid': True,
        'size': 8,
        #'fill_color': '#ffffff',
        #'line_width': 2,
        #'toolbar': 'above',
        #'legend_position': 'right'
        'responsive': True,
    }

    DEFAULT_CURVE_OPTS = {
        'show_grid': True,
        'line_width': 2,
        'responsive': True
    }

    DEFAULT_BARS_OPTS = {
        'show_grid': False,
        'responsive': True,
    }

    DEFAULT_QUADMESH_OPTS = {
        'show_grid': False,
        'responsive': True
    }

    DEFAULT_SCATTER3D_OPTS = {
        'show_grid': False,
        'responsive': True,
    }

    @classmethod
    def set_defaults(cls):
        cls.curve_defaults()
        cls.points_defaults()
        cls.bars_defaults()
        cls.quadmesh_defaults()


    @classmethod
    def curve_defaults(cls, **kwargs):
        """
        Set defaults for holoviews Curve class. Use kwargs to overwrite elvis defaults
        and set user-specific defaults
        """
        return opts.defaults(opts.Curve(**_dict_merge(kwargs, cls.DEFAULT_CURVE_OPTS)))

    @classmethod
    def points_defaults(cls, **kwargs):
        """
          Set defaults for holoviews Points class. Use kwargs to overwrite elvis defaults
          and set user-specific defaults
          """
        return opts.defaults(opts.Points(**_dict_merge(kwargs, cls.DEFAULT_POINT_OPTS)))

    @classmethod
    def bars_defaults(cls, **kwargs):
        """
          Set defaults for holoviews Points class. Use kwargs to overwrite elvis defaults
          and set user-specific defaults
          """
        return opts.defaults(opts.Bars(**_dict_merge(kwargs, cls.DEFAULT_BARS_OPTS)))

    @classmethod
    def quadmesh_defaults(cls, **kwargs):
        """
          Set defaults for holoviews Points class. Use kwargs to overwrite elvis defaults
          and set user-specific defaults
          """
        return opts.defaults(opts.QuadMesh(**_dict_merge(kwargs, cls.DEFAULT_QUADMESH_OPTS)))

    @classmethod
    def scatter3d_defaults(cls, **kwargs):
        """
          Set defaults for holoviews Points class. Use kwargs to overwrite elvis defaults
          and set user-specific defaults
          """
        return opts.defaults(opts.Scatter3D(**_dict_merge(kwargs, cls.DEFAULT_SCATTER3D_OPTS)))


def _dict_merge(dominant, recessive):
    """
    Combines the two dicts. In case of duplicate keys,
    the values of 'dominant' are used.
    """
    for key, value in recessive.items():
        dominant[key] = dominant.setdefault(key, value)
    return dominant

