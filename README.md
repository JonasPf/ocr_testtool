# Automate UI tests using OCR

*This is in early stages, don't expect it to work flawlessly!*

captest (Hey, anybody have an idea for a better name?) is a cross platform (ok, only Linux so far but should be easy to port) UI testing library based on OCR and image recognition. Basically the library takes a screen capture of the program under test, figures out where an image or a text is within that screen capture, moves the mouse to this position and triggers a click event.

Benefits over other forms of testing:

- It is truly black-box testing. The test framework doesn't need to know anything about the UI toolkit, etc.
- Does still work when using custom or non-standardized screen elements (e.g. a round button rather than the ususal square ones)
- Test cases are usually easy to understand because they do exactly what a human testr would do (e.g. Click on 'Export', Check if 'icon x' is visible, Check if test 'xxxx' is visible).

Downsides:

- It can be a bit fragile, especially when using special fonts, low-contrast, etc.
- Tests run quite slow

## Example

    from captest.window import Window
    import time
    import unittest
    
    class Test1(unittest.TestCase):
        def test1(self):
            time.sleep(3)
            window = Window.from_active_window()
            window.click_text('Export')
    
            time.sleep(1) # That's not very nice, should implement something like window.wait_for(...)
    
            dialog = Window.from_active_window()
            dialog.find_text('Save')
            dialog.click_text('Cancel')
    
            window.click_bitmap('icon.png')


## Similar projects

- http://www.sikulix.com/ (There seems to be less focus on OCR)
