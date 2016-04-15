import ocr
import autopy
import sys

if sys.platform == 'linux2':
    from linux import get_window_rect, get_active_window_rect
else:
    raise Exception('Sorry, platform {} is not supported (yet)'.format(sys.platform))

def capture_window(name):
    return autopy.bitmap.capture_screen(get_window_rect(name=name))

def capture_active_window():
    return autopy.bitmap.capture_screen(get_active_window_rect())

def find_text_in_active_window(text, occurence=0):
    return find_text_in_rect(text, get_active_window_rect(), occurence)

def find_text_in_window(text, window_name, occurence=0):
    return find_text_in_rect(text, get_window_rect(window_name), occurence)

def find_text_in_rect(text, rect, occurence=0):
    bitmap = autopy.bitmap.capture_screen(rect)
    text_positions = ocr.ocr_bitmap(bitmap)

    positions = text_positions[text]

    if len(positions) == 0:
        print "Couldn't find string '{}'".format(text)
        print "Strings found:"
        for text in text_positions:
            print "    " + text
        sys.exit(1)

    try:
        print occurence
        print positions
        pos = positions[occurence]
    except IndexError:
        print "Coulnd't find '{}' occurences of string '{}'".format(occurence + 1, text)
        print "Only '{}' occurences could be found".format(len(positions))
        sys.exit(2)

    center_x = rect[0][0] + pos[0][0] + int(pos[1][0] / 2)
    center_y = rect[0][1] + pos[0][1] + int(pos[1][1] / 2)

    return (center_x, center_y)

def click_text_in_active_window(text, occurence=0):
    pos = find_text_in_active_window(text, occurence)
    autopy.mouse.smooth_move(*pos)
    autopy.mouse.click()
