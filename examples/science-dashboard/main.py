
import panel as pn
import elvis
import numpy as np
import param
import holoviews as hv
from bokeh.models import HoverTool

THEME = 'dark'
elvis.Bokeh.set_elvis_style(theme=THEME)

class ScienceModel(param.Parameterized):
    """ An utter nonsense model to test stuff """

    flux = param.Number(default=0.5, bounds=(0.0, 1.0))
    power = param.Number(default=0.5)
    relativity = param.Boolean(default=False)

    def __init__(self, **kwargs):
        self.kpi_rms = elvis.widgets.KPI(title='Root-Mean-Square', units='a.u.')
        self.kpi_std = elvis.widgets.KPI(title='Standard Deviation', units='m2/s')
        self.kpi_per = elvis.widgets.KPI(title='performance', units='ka')
        super().__init__(**kwargs)
        self.update_kpis()

    def computation(self):
        x = np.linspace(0, 10, 100)
        y = 1 - 0.1 * self.flux * x ** 2 \
            +  np.sqrt(self.power * x) \
            + x * self.relativity
        return x, y

    @param.depends('flux', 'power', 'relativity', watch=True)
    def view(self):
        data = self.computation()
        curve = hv.Curve((data), 'realism', 'magic')
        tooltips = [('', '@realism, @magic')]
        curve.opts(tools=[HoverTool(mode='vline', tooltips=tooltips)])
        curve.opts(color='#eeeeee')
        return curve

    @param.depends('flux', 'power', 'relativity', watch=True)
    def view_power(self):
        x, y = self.computation()
        curve =  hv.Curve((np.sin(y), np.cos(x)), 'fiction', 'illusion')
        curve.opts(color='#eeeeee')
        return curve

    @param.depends('flux', 'power', 'relativity', watch=True)
    def update_kpis(self):
        _, y = self.computation()
        self.kpi_rms.value = np.linalg.norm(y)
        self.kpi_std.value = np.std(y)
        self.kpi_per.value = np.linalg.norm(y ** 2)


model = ScienceModel()

panel_1 = model.view
panel_2 = pn.Column(pn.widgets.LiteralInput(value=123.234234, name="Unused parameter"),
                    pn.widgets.Toggle(name="Dummy 1"),
                    pn.widgets.Toggle(name="Dummy 2"),
                    pn.widgets.Toggle(name="Dummy 3"),
                    pn.panel(model.param, show_name=False))
panel_3 = pn.Column(model.kpi_rms.view,
                    model.kpi_std.view,
                    model.kpi_per.view,
                    margin=10)
panel_4a = model.view_power
panel_4b = pn.pane.Markdown(''.join(str(x) + '\n ' for x in range(1000)))
panel_4c = pn.pane.Markdown("##Empty")

gpanel = elvis.GoldenPanel(theme=THEME)
gpanel.compose(
    gpanel.column(
        gpanel.header("Elvis Example // Scientific Dashboard"),
        gpanel.row(
            gpanel.view(panel_1, 'Curve', scrollable=False),
            gpanel.view(panel_2, 'Controls'),
            gpanel.view(panel_3, 'KPI')),
        gpanel.stack(
            gpanel.view(panel_4a, 'Transformation', scrollable=False),
            gpanel.view(panel_4b, 'Long Text'),
            gpanel.view(panel_4c, 'Empty'))))


if __name__ == "__main__":
    gpanel.serve(title="Science Dashboard", show=False, port=5051)










