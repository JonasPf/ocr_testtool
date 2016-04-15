import autopy.bitmap
import sys

if sys.platform == 'linux2':
    from linux import get_window_rect, get_active_window_rect
else:
    raise Exception('Sorry, platform {} is not supported (yet)'.format(sys.platform))

def capture_window(name):
    return autopy.bitmap.capture_screen(get_window_rect(name=name))

def capture_active_window():
    return autopy.bitmap.capture_screen(get_active_window_rect())
