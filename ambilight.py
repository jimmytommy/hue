from screenshot import MacScreenshot, WinScreenshot
from HelloHue import HelloHue
from datetime import datetime, timedelta
from time import sleep
import sys


class Ambilight(HelloHue):

    MAX_RUN_TIME = 100000

    def __init__(self):
        super(Ambilight, self).__init__()
        self.os = sys.platform

    def turn_on_ambilight(self, interval=0.2, light_num=None, group_num=None, tr_time=None, run_time=None, region=None):

        start_time = datetime.now()
        if not run_time:
            run_time = self.MAX_RUN_TIME
        if not tr_time:
            tr_time = 3

        while ((datetime.now() - start_time).seconds < run_time):
            if self.os == "win32":
                ss = WinScreenshot()
            else:
                ss = MacScreenshot(region=region)
            h, l, s = ss.get_hls()
            # don't let the saturation get too washed out
            s *= 2
            if s < 255:
                s = 255
            self.set_light_hue_sat_bri(hue=h, sat=s, bri=l, light_num=light_num, group_num=group_num, tr_time=tr_time)

            sleep(interval)
