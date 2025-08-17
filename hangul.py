from test_bank import TestBank, find_voice


# Glossary
# Hangul: 谚文 (한글)

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


vowel = {
    "base":     ("a  eo  o  u   eu i",
                 "ㅏ ㅓ  ㅗ ㅜ  ㅡ ㅣ"),
    "ybase":    ("ya yeo yo yu",
                 "ㅑ ㅕ  ㅛ ㅠ"),
    "double":   ("ae/e e  yae/ye ye wa oe/we wae/we weo/wo wi we ui/yi",
                 "ㅐ   ㅔ ㅒ     ㅖ ㅘ ㅚ    ㅙ     ㅝ     ㅟ ㅞ ㅢ"),
    # yi is only used by Unicode
}


# Older manually written table function, but still keep it.
def gen_vowel_table():
    #  set = ("base", "ybase")
    set = ("double",)
    #  set = ("base", "ybase", "double")

    table = { hangul: romaja.split('/')
            for name in set
            for romaja, hangul in zip(vowel[name][0].split(),
                                      vowel[name][1].split())
            }

    cheatsheet = ""
    if "base" in set or "ybase" in set:
        cheatsheet = cheatsheet_vowel_base
    if "double" in set:
        cheatsheet += cheatsheet_vowel_double
    if cheatsheet == "":
        cheatsheet = None

    return TestBank(voice=find_voice('ko_KR'),
                    table=table,
                    cheatsheet=cheatsheet)


# https://www.reddit.com/r/Korean/comments/11fr8b8/is_there_a_full_listchart_of_hangul_and_batchim/
# Initial: ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ
# Vowel:   ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ
# Final:   ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ (null)
#
# Full character table: https://en.wikipedia.org/wiki/Hangul_Syllables
# https://en.wikipedia.org/wiki/Hangul#Consonants
# https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean#Conversion_process
#
# Digging into the macOS Character Viewer:
# plistutil -p /System/Library/Input\ Methods/CharacterPalette.app/Contents/Resources/Category-HalfwidthHangul.plist
# sqlite3 /System/Library/Input\ Methods/CharacterPalette.app/Contents/Resources/CharacterDB.sqlite3 \
#        "select * from unihan_dict where info like 'HANGUL%';"
# sqlite3 /System/Library/Input\ Methods/CharacterPalette.app/Contents/Resources/RelatedCharDB.sqlite3 \
#        "select * from related_dict where relatedChars like '%ㅏ%';"
# The Unicode official name is actually dynamically generated..
# /System/Library/Perl/5.34/unicore/Name.pm

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
        'GG': (1,  None),
        'DD': (4,  None),
        'BB': (8,  None),
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
        'L':  (8,  'l'),
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
        'GS': (3,  'S'),
        'NJ': (5,  'J'),
        'NH': (6,  'H'),
        'LG': (9,  'G'),
        'LB': (11, 'B'),
        'LH': (15, 'H'),
        'LM': (10, 'M'),
        'LP': (14, 'P'),
        'LS': (12, 'S'),
        'LT': (13, 'T'),
        'BS': (18, 'S'),
    }
}

# constants
SBase = 0xAC00
LBase = 0x1100
VBase = 0x1161
TBase = 0x11A7
SCount = 11172
LCount = 19
VCount = 21
TCount = 28
NCount = VCount * TCount


def gen_set(jamo, names):
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


def gen_letter_table(jamo, default_setnames, codebase):

    def gen_table(setnames=None):

        setnames = default_setnames if setnames is None else setnames

        set = gen_set(jamo, setnames)

        table = {}

        for name, (code, name_alias) in set.items():
            codepoint = codebase + code;
            name_full = get_alias(name, name_alias)
            romajas = [name.lower() for name in name_full]
            table[chr(codepoint)] = romajas

        return TestBank(voice=find_voice('ko_KR'),
                        table=table)

    return gen_table


gen_consonant_table = gen_letter_table(Jamo_L, ['plain'], LBase)
gen_patchim_table = gen_letter_table(Jamo_T, ['single'], TBase)


def gen_syllable_table():
    lsetnames = ['plain']
    vsetnames = ['double']
    tsetnames = ['empty']

    lset = gen_set(Jamo_L, lsetnames)
    vset = gen_set(Jamo_V, vsetnames)
    tset = gen_set(Jamo_T, tsetnames)

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

    return TestBank(voice=find_voice('ko_KR'),
                    table=table)


def gen_hangul_table():
    """\
    panikku hangul <sets..>
        consonant:plain(base),tense(double),asp[irated],all
                    Custom consonant set
        vowel:base,ybase,double,single,all
                    Custom vowel set
        consonant   All consonants
        vowel       All vowels
        patchim:single,double
                    Basically only used for learning patchim romanize rule
        [syllable:]<consonant..>+<vowel..>[+<patchim..>]
                    Comma separated list.  Mesh generate all combinations.
                    Examples:  base,double,asp+ybase,double  all+base+double
        lv          All LV  (leading+vowel)
        lvt         All LVT (leading+vowel+patchim)
        all         All LV+LVT

    Future: support parsing combination name like 'ga'
    """

    #  return gen_vowel_table()
    return gen_consonant_table()
    #  return gen_patchim_table()
    #  return gen_syllable_table()
