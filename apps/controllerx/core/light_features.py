SUPPORT_BRIGHTNESS = 1
SUPPORT_COLOR_TEMP = 2
SUPPORT_EFFECT = 4
SUPPORT_FLASH = 8
SUPPORT_COLOR = 16
SUPPORT_TRANSITION = 32
SUPPORT_WHITE_VALUE = 128

FEATURES = [
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP,
    SUPPORT_EFFECT,
    SUPPORT_FLASH,
    SUPPORT_COLOR,
    SUPPORT_TRANSITION,
    SUPPORT_WHITE_VALUE,
]


def decode(number):
    number = int(number)
    return [number & feature for feature in FEATURES if number & feature != 0]
