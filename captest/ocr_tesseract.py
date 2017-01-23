import subprocess
import tempfile
import os.path
import uuid
import re
import collections
import logging

from PIL import Image
from PIL import ImageOps
import bs4
import autopy

# We just assume that the current dpi is 72. Might not work well on retina displays, etc.
SOURCE_DPI=72
TARGET_DPI=300

def get_temp_filename(type='png'):
    return os.path.join(tempfile.gettempdir(), uuid.uuid4().hex + "." + type)

def prepare_bitmap(bitmap):
    orig_file = get_temp_filename()
    # For some reason (maybe to do with the dpi metadata information) jpeg works better with tesseract than png
    new_file = get_temp_filename(type='jpeg')

    bitmap.save(orig_file)

    try:
        # Add dpi to the original file so that we can convert it after that
        hocr = subprocess.check_output(['gm', 'convert', '-density', str(SOURCE_DPI), orig_file, orig_file])
        # Rescale to 300 dpi, change to grayscale and negate if neccessary
        hocr = subprocess.check_output(['gm', 'convert', '-resample', str(TARGET_DPI), '-type', 'grayscale', '-quality', '100', orig_file, new_file])
    except OSError:
        raise Exception('Could not find graphicsmagick (gm) binary')

    os.remove(orig_file)

    return new_file

def parse_hocr(hocr):
    # The hOCR Embedded OCR Workflow and Output Format
    # https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview?pref=2&pli=1#heading=h.77bd784474e5

    soup = bs4.BeautifulSoup(hocr, 'html.parser')
    result = collections.defaultdict(list) 

    def parse_bbox(bbox):
        scale = float(SOURCE_DPI) / float(TARGET_DPI)

        m = re.match('bbox ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*)', bbox)
        start_x = int(m.group(1))
        start_y = int(m.group(2))
        end_x = int(m.group(3))
        end_y = int(m.group(4))

        x = int(start_x * scale)
        y = int(start_y * scale)
        w = int(end_x * scale - x)
        h = int(end_y * scale - y)
        
        return ((x,y), (w,h))

    for span in soup.find_all('span'):
        html_class = span.attrs['class'][0] 
        if html_class in [u'ocrx_word', u'ocr_line']:
            text = span.text.strip()
            rect = parse_bbox(span.attrs['title'])
            result[text].append(rect)

    return dict(result)

def ocr_bitmap(bitmap):
    filename = prepare_bitmap(bitmap)

    try:
        hocr = subprocess.check_output(['tesseract', '-l', 'eng', filename, 'stdout', '-c', 'tessedit_create_hocr=1'])
    except OSError:
        raise Exception('Could not find tesseract binary')

    OCR_ENGINE_DEBUG = os.environ.get('OCR_ENGINE_DEBUG', None)

    if OCR_ENGINE_DEBUG:
        logging.warn("OCR file %s. The file will not be deleted because of environment variable OCR_ENGINE_DEBUG", filename)
    else:
        os.remove(filename)

    result = parse_hocr(hocr)
    return result


