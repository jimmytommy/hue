from httplib2 import Http
import json

class HelloHue(object):
    """ 
    Hello World class for the Phillips Hue API
    Only works when connected to the local network
    """

    HUE_BRIDGE_URL = "http://www.meethue.com/api/nupnp"
    MY_BRIDGE_ID = "001788fffe0a792e"
    BRIDGE_ID = "id"
    BRIDGE_IP = "internalipaddress"

    #IP_ADDRESS = "192.168.0.12"
    IP_ADDRESS = None
    USERNAME = "newdeveloper"
    URL_ADDRESS = None

    GROUP_LIST = {}
    LIGHT_LIST = []

    A_LIGHTS = "lights"
    A_GROUPS = "groups"
    A_CONFIG = "config"
    A_SCHEDULES = "schedules"

    LIGHTS_STATE = "state"
    LIGHTS_ON = "on"
    LIGHTS_BRI = "bri"
    LIGHTS_HUE = "hue"
    LIGHTS_SAT = "sat"
    LIGHTS_XY = "xy"
    LIGHTS_CT = "ct"
    LIGHTS_ALERT = "alert"
    LIGHTS_EFFECT = "effect"
    LIGHTS_NAME = "name"
    LIGHTS_TRANSITION_TIME = "transitiontime"

    GROUPS_ACTION = "action"
    GROUPS_NAME = "name"

    EFFECT_COLORLOOP = "colorloop"
    EFFECT_NONE = "none"
    ALERT_SELECT = "select"

    CT_READING = 245

    HUE_RED = 65280
    HUE_PURPLE = 56100
    HUE_BLUE = 46920
    HUE_GREEN = 25500
    HUE_YELLOW = 12750

    def __init__(self):
        self.IP_ADDRESS = self._get_bridge_ip_address()
        self.URL_ADDRESS = "http://{0}/api/{1}".format(self.IP_ADDRESS, self.USERNAME)

        self.LIGHT_LIST = [int(k) for k in self.get_all_lights().keys()]
        for group in self.get_all_groups().keys():
            self.GROUP_LIST[int(group)] = self.get_lights_in_group(group)

    def get_all_lights(self):
        return self.get_request(self.A_LIGHTS)

    @classmethod
    def _get_bridge_ip_address(klass):
        h = Http()
        resp = h.request(klass.HUE_BRIDGE_URL, "GET")

        if not resp or resp[0].status != 200:
            return None
        resp_json= json.loads(resp[1])
        for bridge in resp_json:
            if bridge[klass.BRIDGE_ID] == klass.MY_BRIDGE_ID:
                return bridge[klass.BRIDGE_IP]

    def get_all_groups(self):
        return self.get_request(self.A_GROUPS)

    def get_group_attributes(self, group_num):
        return self.get_request("{0}/{1}".format(self.A_GROUPS, group_num))

    def get_lights_in_group(self, group_num):
        group_attr = self.get_group_attributes(group_num)
        return [int(light_num) for light_num in group_attr[self.A_LIGHTS]]

    def get_request(self, req_url):
        h = Http()
        req_url = "{base_url}/{req_url}".format(base_url=self.URL_ADDRESS,
                                                req_url=req_url)
        resp = h.request(req_url, "GET")
        if resp and resp[0].status == 200:
            return json.loads(resp[1])
        else:
            return None

    def send_command_to_light(self, light_num, params):
        h = Http()
        json_params = json.dumps(params)
        command_url = "{base_url}/{lights}/{num}/{state}".format(base_url=self.URL_ADDRESS,
                                                                 lights=self.A_LIGHTS,
                                                                 num=light_num,
                                                                 state=self.LIGHTS_STATE)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    def send_command_to_group(self, group_num, params):
        for light in self.GROUP_LIST[group_num]:
            self.send_command_to_light(light, params)

    def send_command_to_all_lights(self, params):
        for light in self.LIGHT_LIST:
            self.send_command_to_light(light, params)

    def send_command(self, params, light_num=None, group_num=None, tr_time=None):
        if tr_time:
            params[self.LIGHTS_TRANSITION_TIME] = tr_time

        if light_num:
            return self.send_command_to_light(light_num, params)
        elif group_num:
            return self.send_command_to_group(group_num, params)
        else:
            return self.send_command_to_all_lights(params)

    def turn_on_lights(self, light_num=None, group_num=None, tr_time=None):
        params = {self.LIGHTS_ON : True}
        return self.send_command(params, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def turn_off_lights(self, light_num=None, group_num=None, tr_time=None):
        params = {self.LIGHTS_ON : False}
        return self.send_command(params, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_xy_color(self, x, y, bri=None, light_num=None, group_num=None, tr_time=None):
        params = {self.LIGHTS_XY : [x, y]}
        if bri:
            params[self.LIGHTS_BRI] = bri
        return self.send_command(params, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_color_temp(self, ct, bri=None, light_num=None, group_num=None, tr_time=None):
        params = {self.LIGHTS_CT : ct}
        if bri:
            params[self.LIGHTS_BRI] = bri
        return self.send_command(params, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_hue_sat_bri(self, hue=None, sat=None, bri=None, light_num=None, group_num=None, tr_time=None):
        params = {}
        if hue:
            params[self.LIGHTS_HUE] = hue
        if bri:
            params[self.LIGHTS_BRI] = bri
        if sat:
            params[self.LIGHTS_SAT] = sat
        return self.send_command(params, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_brightness(self, bri, light_num=None, group_num=None, tr_time=None):
        return self.set_light_hue_sat_bri(bri=bri, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_hue(self, hue, light_num=None, group_num=None, tr_time=None):
        return self.set_light_hue_sat_bri(hue=hue, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_sat(self, sat, light_num=None, group_num=None, tr_time=None):
        return self.set_light_hue_sat_bri(sat=sat, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def start_light_colorloop(self, light_num=None, group_num=None):
        params = {self.LIGHTS_EFFECT : self.EFFECT_COLORLOOP}
        return self.send_command(params, light_num=light_num, group_num=group_num)

    def stop_light_colorloop(self, light_num=None, group_num=None):
        params = {self.LIGHTS_EFFECT : self.EFFECT_NONE}
        return self.send_command(params, light_num=light_num, group_num=group_num)

    def send_light_alert(self, light_num=None, group_num=None):
        params = {self.LIGHTS_ALERT : self.ALERT_SELECT}
        return self.send_command(params, light_num=light_num, group_num=group_num)

    def set_light_color(self, color, bri=None, sat=None, light_num=None, group_num=None, tr_time=None):
        hue = None
        if color == "red":
            hue = self.HUE_RED
        elif color == "purple":
            hue = self.HUE_PURPLE
        elif color == "blue":
            hue = self.HUE_BLUE
        elif color == "green":
            hue = self.HUE_GREEN
        elif color == "yellow":
            hue = self.HUE_YELLOW
        return self.set_light_hue_sat_bri(hue=hue, bri=bri, sat=sat, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def set_light_reading(self, bri=None, light_num=None, group_num=None, tr_time=None):
        return self.set_light_color_temp(self.CT_READING, bri=bri, light_num=light_num, group_num=group_num, tr_time=tr_time)

    def get_light_attributes(self, light_num):
        return self.get_request("{0}/{1}".format(self.A_LIGHTS, light_num))

    def rename_light(self, light_num, light_name):
        h = Http()
        params = {self.LIGHTS_NAME : light_name}
        json_params = json.dumps(params)
        command_url = "{base_url}/{lights}/{num}".format(base_url=self.URL_ADDRESS,
                                                         lights=self.A_LIGHTS,
                                                         num=light_num)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    def set_group_attributes(self, group_num, group_name, group_members):
        # the current API release doesn't support group creation...
        # TODO - update internal group representation
        h = Http()
        group_str = [str(i) for i in group_members]
        params = {self.GROUPS_NAME : group_name,
                  self.A_LIGHTS : group_str}
        json_params = json.dumps(params)
        command_url = "{base_url}/{groups}/{group_num}".format(base_url=self.URL_ADDRESS,
                                                               groups=self.A_GROUPS,
                                                               group_num=group_num)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    def flip_light_switch(self, light_num=None, group_num=None, tr_time=None):
        if light_num:
            lights = [light_num]
        elif group_num:
            lights = self.GROUP_LIST[group_num]
        else:
            lights = self.LIGHT_LIST

        for light in lights:
            status = self.get_light_attributes(light)
            is_light_on = status["state"]["on"]

            if is_light_on:
                self.turn_off_lights(light, tr_time=tr_time)
            else:
                self.turn_on_lights(light, tr_time=tr_time)
