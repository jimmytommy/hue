from screenshot import Screenshot
from HelloHue import HelloHue
from datetime import datetime, timedelta
from time import sleep

class Ambilight(HelloHue):

    MAX_RUN_TIME = 100000

    def turn_on_ambilight(self, interval=0.2, light_num=None, group_num=None, tr_time=None, run_time=None, region=None):

        start_time = datetime.now()
        if not run_time:
            run_time = self.MAX_RUN_TIME
        if not tr_time:
            tr_time = 3

        while ((datetime.now() - start_time).seconds < run_time):
            h, l, s = Screenshot.get_hls_from_screen_capture(region=region)
            # don't let the saturation get too washed out
            s *= 2
            if s < 255:
                s = 255
            self.set_light_hue_sat_bri(hue=h, sat=s, bri=l, light_num=light_num, group_num=group_num, tr_time=tr_time)

            sleep(interval)


    def turn_on_ambilight_top_third(self, interval=0.2, light_num=None, group_num=None, run_time=None, tr_time=None):
        region = Screenshot.get_top_third_of_screen()
        self.turn_on_ambilight(interval=interval, light_num=light_num, group_num=group_num, run_time=run_time, region=region, tr_time=tr_time)
