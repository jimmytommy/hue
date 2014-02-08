from httplib2 import Http
import json

class HelloHue(object):
    """ 
    Hello World class for the Phillips Hue API
    Only works when connected to the local network
    """

    IP_ADDRESS = "192.168.0.12"
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

    GROUPS_ACTION = "action"

    EFFECT_COLORLOOP = "colorloop"
    EFFECT_NONE = "none"
    ALERT_SELECT = "select"

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
    def send_command(klass, params, light_num=None, group_num=None):
        if light_num:
            return klass.send_command_to_light(light_num, params)
        elif group_num:
            return klass.send_command_to_group(group_num, params)
        else:
            return klass.send_command_to_all_lights(params)

    @classmethod
    def turn_on_lights(klass, light_num=None, group_num=None):
        params = {klass.LIGHTS_ON : True}
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def turn_off_lights(klass, light_num=None, group_num=None):
        params = {klass.LIGHTS_ON : False}
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_xy_color(klass, x, y, bri=None, light_num=None, group_num=None):
        params = {klass.LIGHTS_XY : [x, y]}
        if bri:
            params[klass.LIGHTS_BRI] = bri
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_color_temp(klass, ct, bri=None, light_num=None, group_num=None):
        params = {klass.LIGHTS_CT : ct}
        if bri:
            params[klass.LIGHTS_BRI] = bri
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_hue_sat_bri(klass, hue=None, sat=None, bri=None, light_num=None, group_num=None):
        params = {}
        if hue:
            params[klass.LIGHTS_HUE] = hue
        if bri:
            params[klass.LIGHTS_BRI] = bri
        if sat:
            params[klass.LIGHTS_SAT] = sat
        return klass.send_command(params, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_brightness(klass, bri, light_num=None, group_num=None):
        return klass.set_light_hue_sat_bri(bri=bri, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_hue(klass, hue, light_num=None, group_num=None):
        return klass.set_light_hue_sat_bri(hue=hue, light_num=light_num, group_num=group_num)

    @classmethod
    def set_light_sat(klass, sat, light_num=None, group_num=None):
        return klass.set_light_hue_sat_bri(sat=sat, light_num=light_num, group_num=group_num)

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
