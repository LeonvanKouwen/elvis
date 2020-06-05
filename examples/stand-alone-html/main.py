
import panel as pn
import elvis

panel_1 = pn.pane.Markdown("1")
panel_2 = pn.pane.Markdown("2")
panel_3 = pn.pane.Markdown("3")
panel_4 = pn.pane.Markdown("4")

gpanel = elvis.GoldenPanel(theme=elvis.LayoutTheme.DARK)
gpanel.compose(
    gpanel.column(
        gpanel.header("Elvis Example // Scientific Dashboard"),
        gpanel.row(
            gpanel.view(panel_1, 'panel 1', scrollable=False),
            gpanel.view(panel_2, 'panel 2'),
        ),
        gpanel.stack(
            gpanel.view(panel_3, 'panel 3', scrollable=False),
            gpanel.view(panel_4, 'panel 4'),
        ),
    ),
)


gpanel.servable()



# from bokeh.resources import INLINE
# gpanel.app.save('x.html', resources=INLINE)
# self._set_assets("", LayoutTheme.LIGHT)
# Bokeh.set_elvis_style(theme=LayoutTheme.LIGHT)
# for name, panel in self.panels.items():
#     panel.save(name + '.html',
#gpanel.save_to_html()


# gpanel.serve(title="Science Dashboard", show=False, port=5051)

# simple = pn.Column(panel_1, panel_2, panel_3, panel_4)
#
# from bokeh.resources import INLINE
# gpanel.app.save('test2.html', resources=INLINE)

# from bokeh.embed import components, file_html
# from bokeh.io import show
#
# script, html = components(gpanel.app)

# gpanel.save_to_html()
# gpanel.serve(title="Time Series", show=False, port=5050)









