#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tester import Tester, TesterOptions
from kana import gen_kana_table
from hangul import gen_hangul_table
from jis import gen_jis_symbol_table

import argparse


parser = argparse.ArgumentParser("panikku")
parser.add_argument('--no-say', action='store_true', default=False,
                    help="Say the word using TTS after each quiz")
parser.add_argument('--typing', action='store_true', default=False,
                    help="Typing test instead of default romanization quiz")

subparsers = parser.add_subparsers(dest='dataset', required=True)

hiragana_parser = subparsers.add_parser('hiragana')
katakana_parser = subparsers.add_parser('katakana')

for p in (hiragana_parser, katakana_parser):
    p.add_argument('options', nargs='*', default='normal',
        choices=('normal', 'dakuon', 'yoon_normal', 'yoon_dakuon'),
        help='List of kana variants (default: normal)')

hangul_parser = subparsers.add_parser('hangul',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=gen_hangul_table.__doc__)
hangul_parser.add_argument('sets', nargs='+',
        help='Sets of hangul letters or syllables. See sets help below.')

jis_parser = subparsers.add_parser('jis')
jis_parser.add_argument('base', nargs='?', default='jis', choices=('jis', 'us'),
                        help='The base physical keyboard to use (default: jis).')


def gen_testset(args):

    if args.dataset in ('hiragana', 'katakana'):

        options = {'normal': False, 'dakuon': False, 'yoon_normal': False, 'yoon_dakuon': False}
        if isinstance(args.options, str):
            args.options = [args.options]
        for op in args.options:
            options[op] = True

        type = args.dataset[:4]

        table = gen_kana_table(type=type, **options)

    elif args.dataset == 'hangul':

        table = gen_hangul_table(args.sets)

    elif args.dataset == 'jis':
        table = gen_jis_symbol_table(args.base)
    else:
        raise ValueError(f'Unknown dataset name {args.dataset}')

    return table


if __name__ == '__main__':
    args = parser.parse_args()

    options = TesterOptions(say=not args.no_say, typing=args.typing)

    test_bank = gen_testset(args)

    if options.say and test_bank.voice is not None:
        print("Using voice:", test_bank.voice)
        if not 'Premium' in test_bank.voice and not 'Enhanced' in test_bank.voice:
            print("""\
For best TTS voice clarity, please download a Premium or Enhanced voice in
System Settings -> Accessibility -> Spoken Content -> System Voice -> Manage Voices
""")

    tester = Tester(test_bank, options)
    tester()
