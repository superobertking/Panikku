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


def gen_hangul_letter_table():
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

def gen_hangul_syllable_table():
    pass


def gen_hangul_table():
    return gen_hangul_letter_table()
