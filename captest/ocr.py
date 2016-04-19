import subprocess
import tempfile
import os.path
import uuid
import re
import collections

import Image
import bs4
import autopy

scale = 4 # Scaling with factor 2 seems to work better

def get_temp_filename():
    return os.path.join(tempfile.gettempdir(), uuid.uuid4().hex + ".png")

def prepare_bitmap(bitmap):
    # Very hacky, this could probably be done more elegantly in the autopy bitmap class
    orig_file = get_temp_filename()
    new_file = get_temp_filename()

    bitmap.save(orig_file)

    image = Image.open(orig_file)
    # According to https://github.com/tesseract-ocr/tesseract/wiki/ImproveQuality#rescaling
    # at least 300 DPI is necessary. We don't know the monitor dpi so it's not clear
    # by how much the image needs to be scaled up.
    # Playing with these numbers might improve the ocr results.
    image = image.convert('L')
    image = image.resize((image.size[0] * scale, image.size[1] * scale), Image.BICUBIC)
    image.save(new_file, "PNG")

    # TODO: Refactore to use try/finally
    os.remove(orig_file)

    return new_file

def parse_hocr(hocr):
    # The hOCR Embedded OCR Workflow and Output Format
    # https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview?pref=2&pli=1#heading=h.77bd784474e5

    print hocr
    soup = bs4.BeautifulSoup(hocr)
    result = collections.defaultdict(list) 

    def parse_bbox(bbox):
        m = re.match('bbox ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*)', bbox)
        x = int(m.group(1)) / scale
        y = int(m.group(2)) / scale
        w = int(m.group(3)) / scale - x
        h = int(m.group(4)) / scale - y
        return ((x,y), (w,h))

    for span in soup.find_all('span'):
        html_class = span.attrs['class'][0] 
        if html_class in [u'ocrx_word', u'ocr_line']:
            text = span.text.strip()
            rect = parse_bbox(span.attrs['title'])
            print text
            result[text].append(rect)

    return dict(result)

def ocr_bitmap(bitmap):
    filename = prepare_bitmap(bitmap)

    hocr = subprocess.check_output(['tesseract', '-l', 'eng', filename, 'stdout', '-c', 'tessedit_create_hocr=1'])    

    # TODO: Refactore to use try/finally
    os.remove(filename)

    result = parse_hocr(hocr)
    return result


