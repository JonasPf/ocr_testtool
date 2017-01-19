import os

OCR_ENGINE = os.environ.get('OCR_ENGINE', 'tesseract')

if OCR_ENGINE == 'tesseract':
    import ocr_tesseract as ocr
elif OCR_ENGINE == 'havenondemand':
    import ocr_havenondemand as ocr
else:
    raise Exception('Unkown value in environment variable OCR_ENGINE: {}'.format(OCR_ENGINE))

import autopy
import sys

if sys.platform == 'linux2':
    from linux import get_window_by_name, get_active_window, get_window_rect
else:
    raise Exception('Sorry, platform {} is not supported (yet)'.format(sys.platform))

class NotFoundException(Exception):
    pass

def _capture_screen(rect):
    bitmap = autopy.bitmap.capture_screen(rect)
    if os.environ.get('OCR_SAVE_BEFORE', None):
        bitmap.save('ocr.png')

    return bitmap

def find_text_in_rect(text, rect, occurence=0, negate=False):
    bitmap = _capture_screen(rect)
    text_positions = ocr.ocr_bitmap(bitmap, negate)

    try:
        positions = text_positions[text]
    except KeyError:
        msg = u"Couldn't find string '{}'\n".format(text)
        msg += u"Strings found:\n"
        for text in text_positions:
            msg += u"    '{}'\n".format(text)
        raise NotFoundException(msg.encode('utf-8'))

    try:
        return positions[occurence]
    except IndexError:
        msg = u"Couldn't find '{}' occurences of string '{}'".format(occurence + 1, text)
        msg += u"Only '{}' occurences could be found".format(len(positions))
        raise NotFoundException(msg)

def find_bitmap_in_rect(needle, rect, occurence=0):
    bitmap = _capture_screen(rect)
    results = bitmap.find_every_bitmap(needle, 0.0, None)

    try:
        return ((results[occurence][0], results[occurence][1]), (needle.width, needle.height))
    except IndexError:
        msg = u"Coulnd't find '{}' occurences of '{}'".format(occurence + 1, needle)
        msg += u"Only '{}' occurences could be found".format(len(positions))
        raise NotFoundException(msg)
    
def open_bitmap(filename):
    return autopy.bitmap.Bitmap.open(filename)

def calc_center(rect):
    return (rect[0][0] + int(rect[1][0] / 2), rect[0][1] + int(rect[1][1] / 2))

class Window(object):
    def __init__(self, wid):
        self.wid = wid
        
    @property
    def rect(self):
        return get_window_rect(self.wid)

    def _to_screen_rect(self, rect):
        return ((rect[0][0] + self.rect[0][0], rect[0][1] + self.rect[0][1]), (rect[1][0], rect[1][1]))

    def find_text(self, text, occurence=0, negate=False):
        rect = find_text_in_rect(text, self.rect, occurence, negate)
        return self._to_screen_rect(rect)

    def find_bitmap(self, needle, occurence=0):
        rect = find_bitmap_in_rect(needle, self.rect, occurence)
        return self._to_screen_rect(rect)

    def click_text(self, text, occurence=0, negate=False):
        rect = self.find_text(text, occurence, negate)
        pos = calc_center(rect)
        autopy.mouse.smooth_move(*pos)
        autopy.mouse.click()

    def click_bitmap(self, path, occurence=0):
        needle = open_bitmap(path)
        rect = self.find_bitmap(needle, occurence)
        pos = calc_center(rect)
        autopy.mouse.smooth_move(*pos)
        autopy.mouse.click()

    def click_position(self, x, y):
        autopy.mouse.smooth_move(x + self.rect[0][0], y + self.rect[0][1])
        autopy.mouse.click()

    @classmethod
    def from_name(klass, name):
        return klass(get_window_by_name(name))

    @classmethod
    def from_active_window(klass):
        return klass(get_active_window())


