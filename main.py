
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

# gpanel.serve(title="Science Dashboard", show=False, port=5051)

# simple = pn.Column(panel_1, panel_2, panel_3, panel_4)
#
# from bokeh.resources import INLINE
# gpanel.app.save('test2.html', resources=INLINE)








