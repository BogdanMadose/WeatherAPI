import time

def convert_epoch_to(epoch, fmt):
    return time.strftime(fmt, time.localtime(epoch))

def is_around_midday(epoch):
    return 11 <= int(convert_epoch_to(epoch, "%H")) <= 13

def to_fahrenheit(temp):
    return ((temp * 1.8) + 32)