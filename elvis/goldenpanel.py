"""
Elvis main module: the golden-layout panel creator.
"""

import panel as pn
import os
from .bokeh import HoloviewsBokeh
from enum import Enum
from .themes import LayoutTheme


class Block(Enum):
    stack = 'stack'
    row = 'row'
    column = 'column'


class GoldenPanel:
    """
    Generates a jinja2 template, specifically tailored for the (slightly modified)
    golden-layout that can be served using panel.

    Only create golden panels in one go; use one compose method and nest the stack, row,
    colum, and panel methods. Do not create panels without adding them to
    the composition string.
    """

    def __init__(self, theme: LayoutTheme=LayoutTheme.DARK):
        """
        :param theme: use elvis.LayoutTheme.DARK or elvis.LayoutTheme.LIGHT
        """
        self.theme = theme
        self.panels = {}
        self.counter = 0
        self.app = None

    def serve(self, static_dirs=None, **kwargs):
        """ Wrapper for pn.serve(), with the inclusion of the required static assets.
        :static_dirs: Specify directories with static assets in addition to the standard elvis assets.
        :kwargs: key word arguments that are passed on to pn.serve
        """
        static_dirs = {} if static_dirs is None else static_dirs
        assets_elvis = {'assets': os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'assets'))}
        self._set_assets("assets\\", self.theme)
        return pn.serve(self.app, static_dirs={**assets_elvis, **static_dirs}, **kwargs)

    def servable(self, **kwargs) -> None:
        """
        !!! NOT WORKING !!!

        Wrapper for pn.app.servable(), with the inclusion of the required static assets.

        """
        #raise NotImplementedError
        # self._set_assets("assets\\", self.theme)
        # static_dirs = {} if static_dirs is None else static_dirs
        # assets_elvis = {'assets': os.path.abspath(
        #     os.path.join(os.path.dirname(__file__), os.pardir, 'assets'))}
        self._set_assets(os.path.join(os.path.dirname(__file__), os.pardir, 'assets\\'), self.theme)
        self.app.servable(**kwargs)

    def _set_assets(self, root: str, theme: LayoutTheme):
        """ Add the static files (.css and .js) to the panel config. """
        css_base = [root + 'goldenlayout-base.css',
                    root + 'goldenlayout-elvis.css',
                    root + 'panel-customizations.css']
        css_theme = {LayoutTheme.LIGHT: [root + 'goldenlayout-elvis-light.css',
                                         root + 'panel-customizations-light.css'],
                     LayoutTheme.DARK: [root + 'goldenlayout-elvis-dark.css',
                                        root + 'panel-customizations-dark.css']}
        js_files = {'jquery': root + 'js\jquery-1.11.1.min.js',
                    'goldenlayout': root + 'js\goldenlayout.min.js'}
        css_files = css_base + css_theme[theme]
        pn.config.js_files = js_files
        pn.config.css_files = css_files

    def compose(self, golden_layout: str) -> None:
        """
        Creates a servable template from a golden layout js code string.
        Any GoldenPanel object needs to call compose exactly once to function as expected.
        :param golden_layout: Result of nesting stacks, columns, rows, and panels
                              using the methods in this class.
        """
        template = ClientSideCodeStrings.JINJA2_BASE % golden_layout
        self.app = pn.Template(template=template)
        for panel_ID, panel in self.panels.items():
            self.app.add_panel(panel_ID, panel)

    def stack(self, *args: str) -> str:
        """ Adds a 'tab' element. Every argument should be a view or another nestable (stack, column, row)."""
        return self._block(*args, type=Block.stack)

    def column(self, *args: str) -> str:
        """ Vertically aligned panels. Every argument should be a view or another nestable (stack, column, row)."""
        return self._block(*args, type=Block.column)

    def row(self, *args: str) -> str:
        """ Horizontally aligned panels. Every argument should be a view or another nestable (stack, column, row)."""
        return self._block(*args, type=Block.row)

    def _block(self, *args: str, type: Block=Block.stack) -> str:
        """
        Creates nestable js code strings. Note that 'stack', 'colum' and 'row' are the
        strings dictated by the golden layout js code.
        """
        content = ''.join(arg for arg in args)
        return ClientSideCodeStrings.NESTABLE % (type.name, content)

    def view(self, view,
             title: str=None,
             width: int=None,
             height: int=None,
             scrollable=True) -> str:
        """
        Adds a viewable panel.
        :param view: The panel to show in this golden layout sub section.
        :param title: The text to show at the top of the panel.
        :param width: Initial width.
        :param height: Initial height.
        :param scrollable: if True, the the view will get scroll bars, if the content is larger
                           than the panel size.
        """

        # We need to register every panel with a unique name such that after
        # composing the jinja2 template, we can perform add_panel (see compose function).
        self.counter = self.counter + 1
        panel_ID = "panel_" + str(self.counter)
        self.panels[panel_ID] = pn.panel(view, sizing_mode='stretch_both')
        title_str = "title: '%s'," % str(title) if title is not None else "title: '',"
        width_str = "width: %s," % str(width) if width is not None else ""
        height_str = "height: %s," % str(height) if height is not None else ""
        scroll_str = "css_classes: ['not_scrollable']" if not scrollable else ""
        settings = title_str + height_str + width_str + scroll_str
        return ClientSideCodeStrings.VIEW % (panel_ID, settings)

    def header(self, header: str, height: int=90) -> str:
        """ Convenience function to make a title style view."""
        return self.view(pn.pane.HTML(f"<div class='title'>{header}</div>",
                                      sizing_mode='stretch_width'), height=height)







class ClientSideCodeStrings:
    """ Namespace class to hold client size code (html, javascript and jinja2) """

    JINJA2_BASE = \
        """
        {%% extends base %%}
        {%% block postamble %%}
            <head> <link rel="icon"  href="/assets/favicon.ico"  type="image/x-icon"/> </head>
        {%% endblock %%}
        
        <!-- goes in body -->
        {%% block contents %%}
                   
        <script type="text/javascript">
        
        
        var config = 
        {
            settings: 
            {
                hasHeaders: true,
                constrainDragToContainer: true,
                reorderEnabled: true,
                selectionEnabled: true,
                popoutWholeStack: false,
                blockedPopoutsThrowError: true,
                closePopoutsOnUnload: true,
                showPopoutIcon: false,
                showMaximiseIcon: true,
                showCloseIcon: false
            },
            dimensions: {
                borderWidth: 5,
                minItemHeight: 10,
                minItemWidth: 10,
                headerHeight: 30,
                dragProxyWidth: 300,
                dragProxyHeight: 200
            },
            
            content: [ %s ]   
        };

        var myLayout = new GoldenLayout(config);
        myLayout.registerComponent('view', function(container, componentState)
        {
            const {height, width, css_classes} = componentState;
            if(height)
              container.on('open', () => container.setSize(container.width, height));
            if(width)
              container.on('open', () => container.setSize(width, container.height));
            if (css_classes)
              css_classes.map((item) => container.getElement().addClass(item));
            container.setTitle(componentState.title);
            container.getElement().html(componentState.model);
            container.on('resize', () => window.dispatchEvent(new Event('resize')));
        });
        
        myLayout.init();
        
        </script>

        {%% endblock %%}
        """

    NESTABLE = \
        """
        {
            type: '%s',
            content: [ %s ]
        },
        """

    VIEW = \
        """
        {   
            type: 'component',
            componentName: 'view',
            componentState: 
            { 
                model: '{{ embed(roots.%s) }}',
                %s
            },
            isClosable: false,
        },
        """