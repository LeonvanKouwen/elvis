import elvis
import numpy as np
import param
import holoviews as hv
import plotly.express as px
import plotly.graph_objects as go


elvis.HoloviewsPlotly.set_theme(elvis.LayoutTheme.LIGHT)


class Plots(param.Parameterized):
    """ An utter nonsense model to test stuff """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def view_1(self):
        y, x = np.mgrid[-5:5, -5:5] * 0.1
        heights = np.sin(x ** 2 + y ** 2)
        hv.Scatter3D((x.flat, y.flat, heights.flat)).opts(
            cmap='fire', color='z', size=5)

        plot = ( hv.Scatter3D(np.random.randn(100, 4), vdims='Size')
               * hv.Scatter3D(np.random.randn(100, 4) + 2,vdims='Size'))
        plot.opts(height=100, width=200)
        return plot

    def view_2(self):
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        y = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        curve =  hv.Points((x, y)).opts(height=100, width=200)
        return curve

    def view_3(self):
        fig = px.line(x=["a", "b", "c"], y=[1, 3, 2], title="sample figure")
        return fig

    def view_4(self):
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=["Apples", "Oranges", "Watermelon", "Pears"],
            y=[3, 2, 1, 4]
        ))

        fig.update_layout(
            responsive=True,
        )

        return fig

model = Plots()

gpanel = elvis.GoldenPanel(theme=elvis.LayoutTheme.LIGHT)
gpanel.compose(
        gpanel.column(
            gpanel.view(model.view_1, 'holoviews 1', scrollable=False),
            gpanel.view(model.view_2, 'holoviews 2', scrollable=False),
            gpanel.view(model.view_3, 'px', scrollable=False),
            gpanel.view(model.view_3, 'plotly', scrollable=False)))

gpanel.serve(title="Science Dashboard", show=False, port=5051)










