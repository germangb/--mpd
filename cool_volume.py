#!/usr/bin/env python

import re
import sys

bars = '▁▁▂▂▃▃▅▅██'

while True:
    line = sys.stdin.readline()
    reg = re.search('#\([0-9]{1,3}\)', line)
    if reg is not None:
        l, r = reg.span(0)
        number = int(line[l+2:r-1])
        cool_volume = bars[:int(number/10)]
        sys.stdout.write(line[:l]+cool_volume+line[r:])
    else:
        sys.stdout.write(line)
    sys.stdout.flush()

