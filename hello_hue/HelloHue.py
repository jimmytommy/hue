from httplib2 import Http
import json

class HelloHue(object):
    """ 
    Hello World class for the Phillips Hue API
    Only works when connected to the local network
    """

    def _get_bridge_ip_address():
        URL = "http://www.meethue.com/api/nupnp"
        MY_BRIDGE_ID = "001788fffe0a792e"
        BRIDGE_ID = "id"
        BRIDGE_IP = "internalipaddress"

        h = Http()
        resp = h.request(URL, "GET")

        if not resp or resp[0].status != 200:
            return None
        resp_json= json.loads(resp[1])
        for bridge in resp_json:
            if bridge[BRIDGE_ID] == MY_BRIDGE_ID:
                return bridge[BRIDGE_IP]

    #IP_ADDRESS = "192.168.0.12"
    IP_ADDRESS = _get_bridge_ip_address()
    USERNAME = "newdeveloper"
    URL_ADDRESS = "http://{0}/api/{1}".format(IP_ADDRESS, USERNAME)

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

    @classmethod
    def send_command_to_group(klass, group_num, params):
        h = Http()
        json_params = json.dumps(params)
        command_url = "{base_url}/{groups}/{num}/{action}".format(base_url=klass.URL_ADDRESS,
                                                                  groups=klass.A_GROUPS,
                                                                  num=group_num,
                                                                  action=klass.GROUPS_ACTION)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    @classmethod
    def send_command_to_light(klass, light_num, params):
        h = Http()
        json_params = json.dumps(params)
        command_url = "{base_url}/{lights}/{num}/{state}".format(base_url=klass.URL_ADDRESS,
                                                                 lights=klass.A_LIGHTS,
                                                                 num=light_num,
                                                                 state=klass.LIGHTS_STATE)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    @classmethod
    def send_command_to_all_lights(klass, params):
        return klass.send_command_to_group(0, params)

    @classmethod
    def get_request(klass, req_url):
        h = Http()
        req_url = "{base_url}/{req_url}".format(base_url=klass.URL_ADDRESS,
                                                req_url=req_url)
        resp = h.request(req_url, "GET")

        if resp and resp[0].status == 200:
            return json.loads(resp[1])
        else:
            return None

    @classmethod
    def send_command(klass, params, light_num=None, group_num=None, tr_time=None):
        if tr_time:
            params[klass.LIGHTS_TRANSITION_TIME] = tr_time

        if light_num:
            return klass.send_command_to_light(light_num, params)
        elif group_num:
            return klass.send_command_to_group(group_num, params)
        else:
            return klass.send_command_to_all_lights(params)

    @classmethod
    def turn_on_lights(klass, light_num=None, group_num=None, tr_time=None):
        params = {klass.LIGHTS_ON : True}
        return klass.send_command(params, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def turn_off_lights(klass, light_num=None, group_num=None, tr_time=None):
        params = {klass.LIGHTS_ON : False}
        return klass.send_command(params, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_xy_color(klass, x, y, bri=None, light_num=None, group_num=None, tr_time=None):
        params = {klass.LIGHTS_XY : [x, y]}
        if bri:
            params[klass.LIGHTS_BRI] = bri
        return klass.send_command(params, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_color_temp(klass, ct, bri=None, light_num=None, group_num=None, tr_time=None):
        params = {klass.LIGHTS_CT : ct}
        if bri:
            params[klass.LIGHTS_BRI] = bri
        return klass.send_command(params, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_hue_sat_bri(klass, hue=None, sat=None, bri=None, light_num=None, group_num=None, tr_time=None):
        params = {}
        if hue:
            params[klass.LIGHTS_HUE] = hue
        if bri:
            params[klass.LIGHTS_BRI] = bri
        if sat:
            params[klass.LIGHTS_SAT] = sat
        return klass.send_command(params, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_brightness(klass, bri, light_num=None, group_num=None, tr_time=None):
        return klass.set_light_hue_sat_bri(bri=bri, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_hue(klass, hue, light_num=None, group_num=None, tr_time=None):
        return klass.set_light_hue_sat_bri(hue=hue, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_sat(klass, sat, light_num=None, group_num=None, tr_time=None):
        return klass.set_light_hue_sat_bri(sat=sat, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def start_light_colorloop(klass, light_num=None, group_num=None):
        params = {klass.LIGHTS_EFFECT : klass.EFFECT_COLORLOOP}
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def stop_light_colorloop(klass, light_num=None, group_num=None):
        params = {klass.LIGHTS_EFFECT : klass.EFFECT_NONE}
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def send_light_alert(klass, light_num=None, group_num=None):
        params = {klass.LIGHTS_ALERT : klass.ALERT_SELECT}
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_color(klass, color, bri=None, sat=None, light_num=None, group_num=None, tr_time=None):
        hue = None
        if color == "red":
            hue = klass.HUE_RED
        elif color == "purple":
            hue = klass.HUE_PURPLE
        elif color == "blue":
            hue = klass.HUE_BLUE
        elif color == "green":
            hue = klass.HUE_GREEN
        elif color == "yellow":
            hue = klass.HUE_YELLOW
        return klass.set_light_hue_sat_bri(hue=hue, bri=bri, sat=sat, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def set_light_reading(klass, bri=None, light_num=None, group_num=None, tr_time=None):
        return klass.set_light_color_temp(klass.CT_READING, bri=bri, light_num=light_num, group_num=group_num, tr_time=None)

    @classmethod
    def get_all_lights(klass):
        return klass.get_request(klass.A_LIGHTS)

    @classmethod
    def get_light_attributes(klass, light_num):
        return klass.get_request("{0}/{1}".format(klass.A_LIGHTS, light_num))

    @classmethod
    def get_all_groups(klass):
        return klass.get_request(klass.A_GROUPS)

    @classmethod
    def get_group_attributes(klass, group_num):
        return klass.get_request("{0}/{1}".format(klass.A_GROUPS, group_num))

    @classmethod
    def get_lights_in_group(klass, group_num):
        group_attr = klass.get_group_attributes(group_num)
        return [int(light_num) for light_num in group_attr[klass.A_LIGHTS]]

    @classmethod
    def rename_light(klass, light_num, light_name):
        h = Http()
        params = {klass.LIGHTS_NAME : light_name}
        json_params = json.dumps(params)
        command_url = "{base_url}/{lights}/{num}".format(base_url=klass.URL_ADDRESS,
                                                         lights=klass.A_LIGHTS,
                                                         num=light_num)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    @classmethod
    def set_group_attributes(klass, group_num, group_name, group_members):
        # the current API release doesn't support group creation...
        h = Http()
        group_str = [str(i) for i in group_members]
        params = {klass.GROUPS_NAME : group_name,
                  klass.A_LIGHTS : group_str}
        json_params = json.dumps(params)
        command_url = "{base_url}/{groups}/{group_num}".format(base_url=klass.URL_ADDRESS,
                                                               groups=klass.A_GROUPS,
                                                               group_num=group_num)
        resp = h.request(command_url, "PUT", json_params)
        return resp

    @classmethod
    def flip_light_switch(klass, light_num=None, group_num=None, tr_time=None):
        if light_num:
            lights = [light_num]
        elif group_num:
            lights = klass.get_lights_in_group(group_num)
        else:
            lights = [int(k) for k in klass.get_all_lights().keys()]

        for light in lights:
            status = klass.get_light_attributes(light)
            is_light_on = status["state"]["on"]

            if is_light_on:
                klass.turn_off_lights(light, tr_time=tr_time)
            else:
                klass.turn_on_lights(light, tr_time=tr_time)
