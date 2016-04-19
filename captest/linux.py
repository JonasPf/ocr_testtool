import subprocess 
import re

# This is just quickly hacked together. It could probably be done more elegant by using xlib directly.

def _find_number(text, label):
    result = re.search(label + ' *([0-9]*)', text)
    return int(result.group(1))

def get_window_rect(id):
    out = subprocess.check_output(['xwininfo', '-id', id])

    x = _find_number(out, 'Absolute upper-left X:')
    y = _find_number(out, 'Absolute upper-left Y:')
    w = _find_number(out, 'Width:')
    h = _find_number(out, 'Height:')

    return ((x, y), (w, h))

def get_window_by_name(name):
    return subprocess.check_output(['xdotool', 'search', '--name', name])

def get_active_window():
    return subprocess.check_output(['xdotool', 'getactivewindow'])
