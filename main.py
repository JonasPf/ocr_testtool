import autopy
import ocr
import window
import time
import actions

time.sleep(3)


# bmp = window.capture_active_window()
# result = ocr.ocr_bitmap(bmp)
# import pprint
# pprint.pprint(result)

#window.click_text_in_active_window('Categories')
window.click_text_in_active_window('Settings')
window.click_text_in_active_window('minutes', occurence=0)
window.click_text_in_active_window('minutes', occurence=1)
window.click_text_in_active_window('minutes.')
