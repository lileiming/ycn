#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random


count = 0
while(count <40):
    A = random.randint(0, 20)
    B = random.randint(0, 20)
    symbol = random.choice('+-')
    result = ''

    if symbol == '+':
        if (A + B <20):
            result = str(A) + str(symbol) + str(B) + "="
            pass
            count = count + 1

    if symbol == '-':
        if (A - B > 0):
            result = str(A) + str(symbol) + str(B) + "="
            pass
            count = count + 1
    if result:
        print(result,count)



