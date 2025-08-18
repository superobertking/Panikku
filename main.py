#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tester import Tester, TesterOptions
from kana import gen_kana_table
from hangul import gen_hangul_table
from jis import gen_jis_symbol_table

import argparse


parser = argparse.ArgumentParser("Panikku")
parser.add_argument('--no-say', action='store_true', default=False,
                    help="Say the word using TTS after each quiz")


def gen_testset():
    #  table = gen_kana_table(type='kata')
    #  table = gen_hangul_table()
    table = gen_jis_symbol_table('us')
    return table


if __name__ == '__main__':
    args = parser.parse_args()

    options = TesterOptions(say=not args.no_say)

    test_bank = gen_testset()

    if options.say and test_bank.voice is not None:
        print("Using voice:", test_bank.voice)
        if not 'Premium' in test_bank.voice and not 'Enhanced' in test_bank.voice:
            print("""\
For best TTS voice clarity, please download a Premium or Enhanced voice in
System Settings -> Accessibility -> Spoken Content -> System Voice -> Manage Voices
""")

    tester = Tester(test_bank, options)
    tester()
