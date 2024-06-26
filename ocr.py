import PIL.ImageGrab as ImageGrab
import pytesseract


def resize_by_ratio(im, r):
    width, height = im.size
    return im.resize((width * r, height * r))


# @manual_check_decorator
def get_arty_angle():
    im = resize_by_ratio(ImageGrab.grab(bbox=(951, 1033, 969, 1045)), 5)
    result = pytesseract.image_to_string(im,
                                         config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')

    if result != '' and 0 <= int(result) <= 360:
        return int(result)
    else:
        return 0


# @manual_check_decorator
def get_arty_mil():
    im = resize_by_ratio(ImageGrab.grab(bbox=(1798, 937, 1866, 963)), 5)
    result = pytesseract.image_to_string(im,
                                         config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789MIL')
    result = result.split('M')[0]

    if result.isdigit():
        return int(result)
    else:
        return 0
