#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tester import Tester
from kana import gen_kana_table


def gen_testset():
    kana_table = gen_kana_table(type='kata')
    return kana_table


if __name__ == '__main__':
    test_bank = gen_testset()
    tester = Tester(test_bank)
    tester()
