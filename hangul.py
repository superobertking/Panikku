from test_bank import TestBank, find_voice


# Glossary
# Hangul: 谚文 (한글)


# This module contains two systems of consonant, vowel, and patchims---an older
# combinational character standard and Unicode standard.
# Since IME (at least the macOS one) uses the former one when typing only
# the jamos, and converts to Unicode when converted to hangul, we will as well
# use older standard code page for jamos and Unicode for hangul.

# Below are manually written maps from the Hangul Compatibility Jamo code page
#
# https://www.reddit.com/r/Korean/comments/11fr8b8/is_there_a_full_listchart_of_hangul_and_batchim/
# Initial: ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ
# Vowel:   ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ
# Final:   ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ (null)
#
# Full character table: https://en.wikipedia.org/wiki/Hangul_Syllables
# https://en.wikipedia.org/wiki/Hangul#Consonants
# https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean#Conversion_process

cheatsheet_vowel_base = """\
ㅏ a
ㅓeo: 熬 (接近拼音ao,收口腔,发音位置更靠前,或国际音标ə(or的o))
ㅗ o: 哦 (接近拼音 o,收口腔,位置更靠后)
ㅜ u: 卷嘴う
ㅡeu: 呃 (拉长嘴)
ㅣ i
"""

cheatsheet_vowel_double = """\
e:
  ㅐㅔ:e    (ae,e)
  ㅒㅖ:ye   (yae,ye)
w:
  阳性元音与阴性元音不会组成复合元音
  阳: ㅗㅏ
  阴: ㅜㅓ
  中: ㅣ
  ㅗ+ㅏㅣ = ㅘㅚㅙ
  ㅜ+ㅓㅣ = ㅝㅟㅞ
     ao i e
    | ㅘ     wa
  ㅗ|   ㅚ  |   (oe)
  __|     ㅙ|we (wae)
    |     ㅞ|
  ㅜ| ㅝ     wo (weo)
    |   ㅟ   wi
ui:
  ㅢ:ui (yi for Unicode name)
"""


# The romanization mixes the Unicode representation/standard romanization/sound

vowel = {
    "base":     ("a  eo  o  u   eu i",
                 "ㅏ ㅓ  ㅗ ㅜ  ㅡ ㅣ"),
    "ybase":    ("ya yeo yo yu",
                 "ㅑ ㅕ  ㅛ ㅠ"),
    "double":   ("ae/e e  yae/ye ye wa oe/we wae/we weo/wo wi we ui/yi",
                 "ㅐ   ㅔ ㅒ     ㅖ ㅘ ㅚ    ㅙ     ㅝ     ㅟ ㅞ ㅢ"),
    # yi is only used by Unicode
}

vowel_groups = {
    'single': ['base', 'ybase'],
    'all': ['base', 'ybase', 'double'],
}

consonant = {
    "plain": ("g  n  d  r/l m  b  s  x  j  h",
              "ㄱ ㄴ ㄷ ㄹ  ㅁ ㅂ ㅅ ㅇ ㅈ ㅎ"),
    "tense": ("c/ch k  t  p",
              "ㅊ   ㅋ ㅌ ㅍ"),
    "asp":   ("gg/kk dd/tt bb/pp ss jj",
              "ㄲ    ㄸ    ㅃ    ㅆ ㅉ"),
}

consonant_groups = {
    'base': ['plain'],
    'double': ['tense'],
    'aspirated': ['asp'],
    'all': ['plain', 'tense', 'asp'],
}

patchim = {
    "empty":    ("x", "x"),
    "single":   ("g/k gg/k n  d/t l  m  b/p s/t ss/t ng j/t c/t k  t  p  h/t",
                 "ㄱ  ㄲ   ㄴ ㄷ  ㄹ ㅁ ㅂ  ㅅ  ㅆ   ㅇ ㅈ  ㅊ  ㅋ ㅌ ㅍ ㅎ"),
    "double":   ("gs/g/k nj/n nh/n lg/g/k lm/m lb/l ls/l lt/l lp/p lh/l bs/b/p",
                 "ㄳ     ㄵ   ㄶ   ㄺ     ㄻ   ㄼ   ㄽ   ㄾ   ㄿ   ㅀ   ㅄ"),
}

patchim_groups = {
    'nonempty': ['single', 'double'],
    'all': ['empty', 'single', 'double'],
}


def collect_sets(sets, valid, groups):
    newsets = set()
    for s in sets:
        if s in groups:
            newsets.update(groups[s])
        elif s in valid:
            newsets.add(s)
        else:
            raise ValueError(f'Invalid set name {s}')
    return newsets


def gen_letter_table(sets, jamos, jamos_groups):
    sets = collect_sets(sets, jamos, jamos_groups)

    table = {
        hangul.replace('x', ''): [x.replace('x', '') for x in romaja.split('/')]
        for name in sets
        for romaja, hangul in zip(jamos[name][0].split(),
                                  jamos[name][1].split())
    }

    return table


def gen_consonant_table(sets):
    table = gen_letter_table(sets, consonant, consonant_groups)
    return table, None


def gen_patchim_table(sets):
    table = gen_letter_table(sets, patchim, patchim_groups)
    return table, None


def gen_vowel_table(sets):
    sets = collect_sets(sets, vowel, vowel_groups)

    table = gen_letter_table(sets, vowel, vowel_groups)

    cheatsheet = ""
    if "base" in sets or "ybase" in sets:
        cheatsheet = cheatsheet_vowel_base
    if "double" in sets:
        cheatsheet += cheatsheet_vowel_double
    if cheatsheet == "":
        cheatsheet = None

    return table, cheatsheet


# Digging into the macOS Character Viewer:
# plistutil -p /System/Library/Input\ Methods/CharacterPalette.app/Contents/Resources/Category-HalfwidthHangul.plist
# sqlite3 /System/Library/Input\ Methods/CharacterPalette.app/Contents/Resources/CharacterDB.sqlite3 \
#        "select * from unihan_dict where info like 'HANGUL%';"
# sqlite3 /System/Library/Input\ Methods/CharacterPalette.app/Contents/Resources/RelatedCharDB.sqlite3 \
#        "select * from related_dict where relatedChars like '%ㅏ%';"
# The Unicode official name is actually dynamically generated..
# /System/Library/Perl/5.34/unicore/Name.pm


# Below are Unicode handling code only for hanguls.
# Below are converted from unicore/Name.pm

# Leading consonant (can be null)
Jamo_L = {
    'plain': {
        'G': (0,   'k'),
        'N': (2,   None),
        'D': (3,   't'),
        'R': (5,   'l'),
        'M': (6,   None),
        'B': (7,   'p'),
        'S': (9,   None),
        '':  (11,  None),
        'J': (12,  None),
        'H': (18,  None),
    },
    'tense': {
        'C': (14,  'ch'),
        'K': (15,  None),
        'T': (16,  None),
        'P': (17,  None),
    },
    'asp': {
        'GG': (1,  'kk'),
        'DD': (4,  'tt'),
        'BB': (8,  'pp'),
        'SS': (10, None),
        'JJ': (13, None),
    },
}

# Vowel
Jamo_V = {
    'base': {
        'A':   (0,  None),
        'EO':  (4,  None),
        'O':   (8,  None),
        'I':   (20, None),
        'EU':  (18, None),
        'U':   (13, None),
    },
    'ybase': {
        'YA':  (2,  None),
        'YEO': (6,  None),
        'YO':  (12, None),
        'YU':  (17, None),
    },
    'double': {
        'AE':  (1,  'e'),
        'YAE': (3,  'ye'),
        'E':   (5,  None),
        'YE':  (7,  None),

        'WA':  (9,  None),
        'OE':  (11, 'we'),
        'WAE': (10, 'we'),
        'WEO': (14, 'wo'),
        'WE':  (15, None),
        'WI':  (16, None),

        'YI':  (19, 'ui'),
    },
}

# Optional trailing consonant
Jamo_T = {
    'empty': {
        '': (0, None)
    },
    'single': {
        'G':  (1,  'k'),
        'GG': (2,  'k'),
        'N':  (4,  None),
        'D':  (7,  't'),
        'L':  (8,  None),
        'M':  (16, None),
        'B':  (17, 'p'),
        'S':  (19, 't'),
        'SS': (20, 't'),
        'NG': (21, None),
        'J':  (22, 't'),
        'C':  (23, 't'),
        'K':  (24, None),
        'T':  (25, None),
        'P':  (26, None),
        'H':  (27, 't'),
    },
    'double': {
        'GS': (3,  ['g', 'k']),
        'NJ': (5,  'n'),
        'NH': (6,  'n'),
        'LG': (9,  ['g', 'k']),
        'LB': (11, 'l'),
        'LM': (10, 'm'),
        'LS': (12, 'l'),
        'LT': (13, 'l'),
        'LP': (14, 'p'),
        'LH': (15, 'l'),
        'BS': (18, ['b', 'p']),
    }
}


# constants
SBase = 0xAC00
# LBase = 0x1100
# VBase = 0x1161
# TBase = 0x11A7
LCount = 19
VCount = 21
TCount = 28
NCount = VCount * TCount


def gen_set(jamo, jamo_groups, names):
    names = collect_sets(names, jamo, jamo_groups)
    table = {}
    for name in names:
        table |= jamo[name]
    return table


def get_alias(orig, alias):
    if alias is None:
        return (orig,)
    elif isinstance(alias, str):
        return (orig, alias)
    elif isinstance(alias, (list, tuple)):
        return (orig, *alias)
    else:
        raise ValueError(f"Bug: Invalid alias value type {type(alias)}")


# Deprecated Unicode letter table generation
#
# def gen_letter_table(jamo, codebase, jamo_groups):
#
#     def gen_table(setnames):
#
#         set = gen_set(jamo, jamo_groups, setnames)
#
#         table = {}
#
#         for name, (code, name_alias) in set.items():
#             codepoint = codebase + code;
#             name_full = get_alias(name, name_alias)
#             romajas = [name.lower() for name in name_full]
#             table[chr(codepoint)] = romajas
#
#         return table, None
#
#     return gen_table
#
#
# gen_consonant_table = gen_letter_table(Jamo_L, LBase, consonant_groups)
# gen_patchim_table = gen_letter_table(Jamo_T, TBase, patchim_groups)


def gen_syllable_table(lsetnames, vsetnames, tsetnames):

    lset = gen_set(Jamo_L, consonant_groups, lsetnames)
    vset = gen_set(Jamo_V, vowel_groups, vsetnames)
    tset = gen_set(Jamo_T, patchim_groups, tsetnames)

    table = {}

    for l, (L, l_alias) in lset.items():
        for v, (V, v_alias) in vset.items():
            for t, (T, t_alias) in tset.items():

                codepoint = (L * VCount + V) * TCount + T + SBase

                # Cannot use l_alias = get_alias(l, l_alias).. it will grow
                # in the next iteration.. I don't know why..
                l_full = get_alias(l, l_alias)
                v_full = get_alias(v, v_alias)
                t_full = get_alias(t, t_alias)

                romajas = [(l+v+t).lower() for l in l_full for v in v_full
                                           for t in t_full]

                table[chr(codepoint)] = romajas

    return table, None


def gen_hangul_table(sets):
    """\
sets:
    consonant:plain(base),tense(double),asp[irated],all
                    Custom consonant set
    vowel:base,ybase,double,single,all
                    Custom vowel set
    patchim:single,double,nonempty,all
                    Basically only used for learning patchim romanize rule

    [syllable:]<consonant..>*<vowel..>[*<patchim..>]
                    LVT components separated by * or +.  Each component is a
                    comma (,) separated list.  Mesh generates all combinations.
                    Examples:  base,double,asp+ybase,double  all*all*single

    consonant       All consonants
    vowel           All vowels
    patchim         Non-empty patchims
    lv              All LV  (leading+vowel)
    lvt             All LVT (leading+vowel+patchim)
    syllable|all    All LV+LVT

Future: support parsing combination name like 'ga'
Future: change argument parsing to custom parser
"""

    table = {}
    cheatsheet = ""

    for s in sets:
        parts = s.split(':')

        if len(parts) == 0 or len(parts) > 2:
            raise ValueError(f'Invalid set {s!r}')

        t, c = None, None

        if len(parts) == 1:
            settype = parts[0]
            if settype == 'all' or settype == 'syllable':
                t, c = gen_syllable_table(['all'], ['all'], ['all'])
            elif settype == 'lvt':
                t, c = gen_syllable_table(['all'], ['all'], ['nonempty'])
            elif settype == 'lv':
                t, c = gen_syllable_table(['all'], ['all'], ['empty'])
            elif settype == 'vowel':
                t, c = gen_vowel_table(['all'])
            elif settype == 'consonant':
                t, c = gen_consonant_table(['all'])
            elif settype == 'patchim':
                t, c = gen_patchim_table(['nonempty'])
            else:
                parts = ['syllable', parts[0]]

        # optional 'syllable' will fall through to here
        if len(parts) == 2:
            settype = parts[0]
            if settype == 'vowel':
                t, c = gen_vowel_table(parts[1].split(','))
            elif settype == 'consonant':
                t, c = gen_consonant_table(parts[1].split(','))
            elif settype == 'patchim':
                t, c = gen_patchim_table(parts[1].split(','))
            elif settype == 'syllable':
                subparts = [y for x in parts[1].split('*') for y in x.split('+')]
                if len(subparts) == 2:
                    t, c = gen_syllable_table(subparts[0].split(','),
                                              subparts[1].split(','), ['empty'])
                elif len(subparts) == 3:
                    t, c = gen_syllable_table(subparts[0].split(','),
                                              subparts[1].split(','),
                                              subparts[2].split(','))
                else:
                    raise ValueError(f'Invalid syllable component {s!r}!')
            else:
                raise ValueError(f'Invalid set type {settype!r}!')

        assert(t is not None)

        table.update(t)
        if c is not None:
            cheatsheet += c

    if cheatsheet.strip() == "":
        cheatsheet = None

    return TestBank(voice=find_voice('ko_KR'), table=table, cheatsheet=cheatsheet)
