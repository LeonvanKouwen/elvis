
import panel as pn
import elvis
import numpy as np
import queue
from tornado.ioloop import PeriodicCallback
import param
from tornado import gen


THEME = 'light'
elvis.Bokeh.set_elvis_style(theme=THEME)


class Live():

    def __init__(self):
        self.plot = elvis.streaming.LivePlot(num_curves=len(self.data_generator(.0)))
        self.computation = elvis.streaming.LiveComputation(self.data_generator)
        self.computation.register_queue(self.plot.data_queue)
        self.kpi_queue = queue.Queue(maxsize=50)
        self.computation.register_queue(self.kpi_queue)
        self.kpi_max = elvis.widgets.KPI(title="max", value=0.0, units="Volt")
        self.kpi_rms = elvis.widgets.KPI(title="RMS", value=0.0, units="Volt")
        PeriodicCallback(self.update_kpis, 200).start()

    @staticmethod
    def data_generator(t):
        return np.sin(10 * t) + np.random.randn(1) * 0.1, \
               np.cos(t * (2 + np.sin(0.3 * t))) + np.random.randn(1) * 0.05 + 2.0

    @gen.coroutine
    def update_kpis(self):
        data = list(self.kpi_queue.queue)
        y_combined = np.squeeze(np.array([d[1] for d in data]))
        #print(y_combined)
        try:
            self.kpi_max.value = np.max(y_combined)
            self.kpi_rms.value = np.sqrt(np.mean(y_combined ** 2) / len(y_combined))
        except ValueError:
            pass

    def view(self):
        return pn.Row(self.plot.view(),
                      pn.Column(self.kpi_max.view(),
                                self.kpi_rms.view()),
                      height=500)


class TimeControlPanel(param.Parameterized):

    is_running = param.Boolean(default=False, label=' Play / Pause')  # \u25b6
    sample_time = param.Number(default=.20, label="Sample Time (s)")
    slow_motion = param.Number(default=1.0, label="Slow Motion")

    def __init__(self, dataobj, plotobj, **params):
        super().__init__(**params)

        self.dataobj = dataobj
        self.plotobj = plotobj

        self.reset = pn.widgets.Button(name='reset', value=False, width=150)
        self.sim_time = elvis.widgets.KPI(title="Simulation Clock", units="s")
        self.achieved_sample_rate = elvis.widgets.KPI(title="Actual Sample rate", units="Hz")
        self.requested_sample_rate = elvis.widgets.KPI(title="Requested sample rate",
                                                       units="Hz")
        PeriodicCallback(self.update_kpis, 1000).start()
        self.update_time_settings()

    def view(self):

        widgets = {
            'is_running': pn.widgets.Checkbox,
            'sample_time': pn.widgets.LiteralInput,
            'slow_motion': pn.widgets.LiteralInput}

        return pn.panel(
            pn.Column(self.reset,
                      pn.Param(self.param, show_name=False,
                               widgets=widgets, margin=(0, 0, 0, -5)),
                      self.sim_time.view(),
                      self.requested_sample_rate.view(),
                      self.achieved_sample_rate.view(), ))

    @param.depends('sample_time', 'slow_motion', watch=True)
    def update_time_settings(self):
        self.dataobj.slow_motion = self.slow_motion
        self.dataobj.sample_time = self.sample_time
        self.dataobj.set_periodic_callback()
        self.requested_sample_rate.value = 1 / (self.slow_motion * self.sample_time)
        self.achieved_sample_rate.trip_levels = (self.requested_sample_rate.value * 0.75,
                                                 self.requested_sample_rate.value * 1.5)

    @param.depends('is_running', watch=True)
    def toggle_is_running(self):
        if self.is_running:
            self.dataobj.start()
        else:
            self.dataobj.stop()

    @gen.coroutine
    def update_kpis(self):
        self.sim_time.value = self.dataobj.t_sim
        self.achieved_sample_rate.value = self.plotobj.sample_rate

live = Live()
control_panel = TimeControlPanel(live.computation, live.plot)

gpanel = elvis.GoldenPanel(theme=THEME)
gpanel.compose(
    gpanel.row(
        gpanel.view(control_panel.view(), 'Controls', width=210, scrollable=False),
        gpanel.stack(
            gpanel.view(live.view(), 'Live', scrollable=False),
            gpanel.view(pn.pane.Markdown("..."), 'Some Tab'),
            gpanel.view(pn.pane.Markdown("..."), 'Another Tab'))))


if __name__ == "__main__":
    gpanel.serve(title="Time Series", show=False, port=5050)

    # Use the code below to run from the command line
    # gpanel.app.servable()










