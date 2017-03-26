from PyNode import *
from ActionNode import *

import datetime


class DateNode(PyNode):
    def __init__(self):
        super().__init__()

    @action
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

