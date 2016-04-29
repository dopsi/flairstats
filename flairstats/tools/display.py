from math import fabs,floor,log10

def float(num, min_width):
    return ('{:.'+'{:.0f}'.format(max(fabs(floor(log10(num))), min_width))+'f}').format(num)
