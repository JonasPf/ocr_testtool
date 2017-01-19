import window
import time

time.sleep(3)

w = window.Window.from_active_window()
w.click_bitmap('test.png')
w.click_text('Todo/Projects')
w.click_position(100,100)
