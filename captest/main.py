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

w = window.Window.from_active_window()
w.click_bitmap('test.png')
w.click_text('Todo/Projects')
w.click_position(100,100)
