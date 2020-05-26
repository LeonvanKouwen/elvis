"""
Elvis main module: the golden-layout panel creator.
"""

import panel as pn
import os


class GoldenPanel:
    """
    Generates a jinja2 template, specifically tailored for the (slightly modified)
    golden-layout that can be served using panel.

    Only create golden panels in one go; use one compose method and nest the stack, row,
    colum, and panel methods. Do not create panels without adding them to
    the composition string.
    """
    CSS_BASE = ['assets\goldenlayout-base.css',
                'assets\panel-customizations.css']

    CSS_THEME = {'light': ['assets\goldenlayout-elvis-light.css',
                           'assets\panel-customizations-light.css'],
                  'dark': ['assets\goldenlayout-elvis-dark.css',
                           'assets\panel-customizations-dark.css']}


    JS_FILES = {'jquery': 'assets\js\jquery-1.11.1.min.js',
                'goldenlayout': 'assets\js\goldenlayout.min.js'}

    def __init__(self, title="Elvis", theme='light'):
        """
        :param theme: Choose between 'light' and 'dark'.
        :param title: Title for the browser tab.
        """
        self.title = title
        self.panels = {}
        self.counter = 0
        self.app = None
        css_files = self.CSS_BASE + self.CSS_THEME[theme]
        pn.extension(css_files=css_files, js_files=self.JS_FILES)

    def serve(self, static_dirs=None, **kwargs):
        """ Wrapper for pn.serve, with the inclusion of the required static assets. """
        static_dirs = {} if static_dirs is None else static_dirs
        assets_elvis = {'assets': os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'assets'))}
        kwargs.setdefault('title', self.title)
        return pn.serve(self.app, static_dirs={**assets_elvis, **static_dirs}, **kwargs)

    def compose(self, golden_layout_string):
        """
        Creates a servable template from a golden layout js code string.
        :param golden_layout_string: Result of nesting stacks, columns, rows, and panels
                                     using the methods in this class.
        """
        template = ClientSideCodeStrings.JINJA2_BASE % golden_layout_string
        self.app = pn.Template(template=template)
        for panel_ID, panel in self.panels.items():
            self.app.add_panel(panel_ID, panel)

    def view(self, view, title=None, width=None, height=None, scrollable=True):
        """
        Adds a viewable panel.
        :param view: The panel to show in this golden layout sub section.
        :param title: The text to show at the top of the panel.
        :param width: Initial width.
        :param height: Initial height.
        """

        # We need to register every panel with a unique name such that after
        # composing the jinja2 template, we can add them (see compose function).
        self.counter = self.counter + 1
        panel_ID = "panel_" + str(self.counter)
        self.panels[panel_ID] = pn.panel(view, sizing_mode='stretch_both')
        title_str = "title: '%s'," % str(title) if title is not None else "title: '',"
        width_str = "width: %s," % str(width) if width is not None else ""
        height_str = "height: %s," % str(height) if height is not None else ""
        scroll_str = "css_classes: ['not_scrollable']" if not scrollable else ""
        settings = title_str + height_str + width_str + scroll_str
        return ClientSideCodeStrings.VIEW % (panel_ID, settings)

    def header(self, header, height=90):
        """ Convenience function to make a title style view."""
        return self.view(pn.pane.HTML(f"<div class='title'>{header}</div>",
                                      sizing_mode='stretch_width'), height=height)

    def _block(self, *args, type='stack'):
        """
        Creates nestable js code strings. Note that 'stack', 'colum' and 'row' are the
        strings dictated by the golden layout js code.
        """
        content = ''.join(arg for arg in args)
        return ClientSideCodeStrings.NESTABLE % (type, content)

    def stack(self, *args):
        """ Adds a 'tab' element."""
        return self._block(*args, type='stack')

    def column(self, *args):
        """ Vertically aligned panels"""
        return self._block(*args, type='column')

    def row(self, *args):
        """ Horizontally aligned panels"""
        return self._block(*args, type='row')


class ClientSideCodeStrings:
    """ Namespace class to hold client size code (html, javascript and jinja2) """

    JINJA2_BASE = \
        """

        {%% extends base %%}

        {%% block postamble %%}
       
        <head> <link rel="icon"  href="/assets/favicon.ico"  type="image/x-icon"/>
        
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