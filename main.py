import ocr
import window
import time

time.sleep(3)


bmp = window.capture_active_window()
result = ocr.ocr_bitmap(bmp)
import pprint
pprint.pprint(result)
