import Quartz.CoreGraphics as CG
import Image
import colorsys

class Screenshot(object):
    """ 
    Used to capture and perform some analysis on screen images. 

    Code adapted from http://stackoverflow.com/questions/12978846/python-get-screen-pixel-value-in-os-x/13024603#13024603 and https://gist.github.com/olooney/1246268
    """

    @classmethod
    def get_fullscreen_capture(klass):
        region = CG.CGRectInfinite
        return klass.get_region_capture(region)

    @classmethod
    def get_region_capture(klass, region):
        image = CG.CGWindowListCreateImage(region,
                                           CG.kCGWindowListOptionOnScreenOnly,
                                           CG.kCGNullWindowID,
                                           CG.kCGWindowImageDefault)
        prov = CG.CGImageGetDataProvider(image)
        d = CG.CGDataProviderCopyData(prov)
        w = CG.CGImageGetWidth(image)
        h = CG.CGImageGetHeight(image)

        # note -- Quartz.CoreGraphics is weird and returns BGRA
        # so this image will have blue and red values flipped
        # calculations will adjust accordingly
        return Image.frombuffer("RGBA", (w,h), d, "raw", "RGBA", 0, 1)

    @classmethod
    def get_top_third_of_screen(klass):
        whole_region = CG.CGRectInfinite
        w = CG.CGRectGetWidth(whole_region)
        h = CG.CGRectGetHeight(whole_region)
        return CG.CGRectMake(0.0, 0.0, w, float(h / 3.0))

    @classmethod
    def get_histogram_from_image(klass, image):
        hist = image.histogram()
        # flip the red and blue values (see note in get_region_capture)
        adj_hist = hist[256*2:256*3] + hist[256:256*2] + hist[0:256]
        return adj_hist

    @classmethod
    def get_rgb_from_histogram(klass, hist):
        # split into red, green, blue
        r = hist[0:256]
        g = hist[256:256*2]
        b = hist[256*2:256*3]

        r_avg = sum(i*w for i, w in enumerate(r)) / sum(r)
        g_avg = sum(i*w for i, w in enumerate(g)) / sum(g)
        b_avg = sum(i*w for i, w in enumerate(b)) / sum(b)
        
        return r_avg, g_avg, b_avg

    @classmethod
    def convert_hls_to_philips_scale(klass, h, l, s):
        HUE_MAX = 65280
        #philips uses a weird # scale for their hues
        h_scaled = int(HUE_MAX * h)
        l_scaled = int(255.0 * l)
        s_scaled = int(255.0 * s)
        if h_scaled == 0:
            h_scaled == 1

        return h_scaled, l_scaled, s_scaled

    @classmethod
    def get_hls_from_rgb(klass, r, g, b):
        r_scaled = float(r) / 255.0
        g_scaled = float(g) / 255.0
        b_scaled = float(b) / 255.0
        hue, light, sat = colorsys.rgb_to_hls(r_scaled, g_scaled, b_scaled)
        return klass.convert_hls_to_philips_scale(hue, light, sat)

    @classmethod
    def get_hls_from_screen_capture(klass, region=None):
        if region:
            im = klass.get_region_capture(region)
        else:
            im = klass.get_fullscreen_capture()

        hist = klass.get_histogram_from_image(im)
        r, g, b = klass.get_rgb_from_histogram(hist)
        return klass.get_hls_from_rgb(r,g,b)

