"""

Work in progress. Probably more complicated than needed.
Documentation will be added after the code is less volatile.
LiveComputation and LivePlot are separated to make computation
and visualization run independently.

"""

from tornado.ioloop import PeriodicCallback
from tornado import gen
import holoviews as hv
from holoviews import dim, opts
import numpy as np
from bokeh.models import HoverTool
import time
from holoviews.streams import Buffer
import queue


class LiveComputation():

    MINIMUM_CALLBACK_TIME_MS = 5

    def __init__(self, time_callback, slow_motion=1.0, sample_time=0.1, t0=0.0):
        self.t_sim_0 = t0
        self.t_sim = t0
        self.t_run = 0.0
        self.t_run_0 = time.time()
        self.queues = []
        self.time_callback = time_callback
        self.periodic_callback = None
        self.slow_motion= slow_motion
        self.sample_time = sample_time
        self.set_periodic_callback()

    def reset(self):
        self.t_sim = self.t_sim_0
        self.t_run = 0.0
        self.t_run_0 = time.time()

    @property
    def callback_interval_ms(self):
        # TODO use param here?
        ms = self.sample_time * self.slow_motion * 1000
        if ms < self.MINIMUM_CALLBACK_TIME_MS:
            ms = self.MINIMUM_CALLBACK_TIME_MS
            print("Callback interval too low, using", ms, " (ms)")
        return ms

    def start(self):
        self.t_run = 0.0
        self.t_run_0 = time.time()
        self.periodic_callback.start()

    def stop(self):
        self.periodic_callback.stop()

    def set_periodic_callback(self):
        if self.periodic_callback is None:
            self.periodic_callback = \
                PeriodicCallback(self.fill_buffer, self.callback_interval_ms * self.slow_motion)
        else:
            if self.periodic_callback.is_running():
                self.periodic_callback.stop()
                self.periodic_callback = \
                    PeriodicCallback(self.fill_buffer, self.callback_interval_ms)
                self.periodic_callback.start()
            else:
                self.periodic_callback = \
                    PeriodicCallback(self.fill_buffer, self.callback_interval_ms)

    def register_queue(self, channel):
        self.queues.append(channel)

    @gen.coroutine
    def fill_buffer(self):
        # TODO Create batched calls to time_callback

        t_run_new = time.time() - self.t_run_0
        t_sim_new = self.t_sim + (t_run_new - self.t_run) / self.slow_motion
        self.t_run = t_run_new
        self.t_sim = t_sim_new

        data = (self.t_sim, self.time_callback(self.t_sim))
        for q in self.queues:
            if q.full():
                # Remove first item when the buffer is full.
                # Theoretically the buffer could be empty again when the
                # get command gets executed.
                try:
                    q.get(block=False)
                except:
                    pass
            q.put(data)


class LivePlot:

    def __init__(self, callback_interval_ms=100, buffer_size=300, num_curves=2):

        self.callback_interval_ms = callback_interval_ms
        self.buffer_size = buffer_size
        self.num_curves = num_curves
        self.t_range = [0.0, 0.0]
        data_empty = np.empty((0, self.num_curves + 1))
        self.plot_buffer = Buffer(data_empty, length=self.buffer_size)
        self.data_queue = queue.Queue(maxsize=self.buffer_size)
        self.periodic_callback = PeriodicCallback(self.buffer_transfer,
                                                  self.callback_interval_ms)
        self.periodic_callback.start()
        self.time_previous = time.time()
        self.sample_rate = 0.0
        self.plot = hv.DynamicMap(self.plot_update, streams=[self.plot_buffer])
        self.plot.opts(shared_axes=False, toolbar=None, show_legend=False)


    def reset_plot(self):
        # Can't get this working
        raise NotImplementedError
        # self.periodic_callback.stop()
        # #self.plot_buffer.clear() # this crashes
        # self.periodic_callback.start()

    def view(self):
        return self.plot

    @gen.coroutine
    def buffer_transfer(self):

        if self.data_queue.empty():
            return

        queue_size = self.data_queue.qsize()
        current_queue = np.zeros((queue_size, self.num_curves + 1))

        for i in range(queue_size):
            try:
                t, y = self.data_queue.get()
                current_queue[i, 0] = t
                current_queue[i, 1:] = y
            except IndexError:
                break
        self.plot_buffer.send(current_queue)
        self.sample_rate = queue_size / (time.time() - self.time_previous)
        self.time_previous = time.time()

    def plot_update(self, data):

        if len(data) == 0:
            # Initially an empty array is send once by the Buffer.
            overlay = hv.Overlay()
            for i in range(self.num_curves):
                overlay = overlay * hv.Curve((np.nan, np.nan))
            return overlay

        t = data[:, 0]
        overlay = hv.Overlay()
        time = hv.Dimension('time', label='simulation time', unit='s')
        field = hv.Dimension('field', label='electric field', unit='V/m')

        for i in range(1, data.shape[1]):
            overlay = overlay * hv.Curve((t, data[:, i]), time, field)

        self.t_range = refresh_time_range(t, self.t_range,
                                          num_data_points=self.buffer_size)
        y_range = range_margin(data[:, 1:])
        hoovertool = HoverTool(mode='vline',
            tooltips=[('Time', '@time'), ('Field', '@field')])

        return overlay.opts(
            opts.Curve(xlim=tuple(self.t_range),
                       ylim=tuple(y_range),
                       tools=[hoovertool]))


def refresh_time_range(t, range, num_data_points=300,
                       rescale_fraction=0.75, growth_factor=2.0):
    tmin = t[0]
    tmax = t[-1]
    if len(t) >= num_data_points:
        if tmax >= range[1] or tmin >= range[0]:
            range[0] = tmin + (tmax - tmin) * rescale_fraction
            range[1] = tmax + (tmax - tmin) * rescale_fraction
    elif range[1] <= tmax:
        range[0] = tmin
        range[1] = tmin + growth_factor * (tmax - tmin)
    return range


def range_margin(y, margin=0.02):
    ymin = np.min(y)
    ymax = np.max(y)
    delta_y = ymax - ymin
    return [ymin - margin * delta_y, ymax + margin * delta_y]