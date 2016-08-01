from PyNode import *
from VirtualNode import *
from ActionNode import *

import datetime

class DateNode(PyNode):
    def __init__(self):
        super().__init__()
        self.append_node('year', VirtualNode(self.year))
        self.append_node('month', VirtualNode(self.month))
        self.append_node('day', VirtualNode(self.day))

    @Action
    def get(self, target_node):
        now = datetime.date.today()
        return "{}-{}-{}".format(now.year, now.month, now.day)

    def year(self):
        now = datetime.date.today()
        return now.year

    def month(self):
        now = datetime.date.today()
        return now.month

    def day(self):
        now = datetime.date.today()
        return now.day

