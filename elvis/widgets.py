"""
Custom widgets.
"""

import panel as pn
import param


class KPI(param.Parameterized):

    """
    Key Performance Indicator.
    Widget that shows important numbers (KPI's) more clearly than standard numbers.
    Specify trip levels to mark the number red when the value exceeds these levels.
    """
    value = param.Number(default=0.0)

    def __init__(self, title="kpi", value=0.0, units="", trip_levels=None, format='{value:.2}', **kwargs):
        """
        :param title: string
        :param value: float
        :param units: string
        :param trip_levels: (string, string)
        """
        super().__init__(**kwargs)
        self.title = title
        self.units = units
        self.value = value
        self.format = format
        self.trip_levels = trip_levels
        self.html_pane = pn.pane.HTML(self._html())

    def view(self):
        """Returns the output to show on the panel."""
        return self.html_pane

    @param.depends('value', watch=True)
    def _update(self):
        self.html_pane.object = self._html()

    def _html(self):
        trip_class = ""
        if self.trip_levels and not self.trip_levels[0] < self.value < self.trip_levels[1]:
            trip_class = "kpi-trip"
        value = self.format.format(value=self.value)
        html_string = f""" 
            <div class='kpi kpi-div'>
                <span class='kpi kpi-title'> {self.title} </span>
                <div>
                    <span class='kpi kpi-value {trip_class}'> {value} </span>
                    <span class='kpi kpi-units'> {self.units} </span>    
                </div>
            </div>
            """
        return html_string




