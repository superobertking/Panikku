from test_bank import TestBank


# Glossary
# Hangul: 谚文 (한글)

cheatsheet = """\
ㅏ a
ㅓeo: 熬 (接近拼音ao,收口腔,发音位置更靠前,或国际音标ə(or的o))
ㅗ o: 哦 (接近拼音 o,收口腔,位置更靠后)
ㅜ u: 卷嘴う
ㅡeu: 呃 (拉长嘴)
ㅣ i
"""

consonent = {
    "base": ("a  eo  o  u   eu i",
             "ㅏ ㅓ  ㅗ ㅜ  ㅡ ㅣ"),
    "y":    ("ya yeo yo yu"
             "ㅑ ㅕ  ㅛ ㅠ"),
    "d":    ("ae e    oe      wi",
             "ㅐ ㅔ   ㅚ      ㅟ"),
    "yd":   ("yae ye   wa wae  wo we ui",
             "ㅒ  ㅖ   ㅘ  ㅙ  ㅝ ㅞ ㅢ"),
}

def gen_hangul_table():
    table = { hangul: romaja
            for name in ("base",)
            for romaja, hangul in zip(consonent[name][0].split(),
                                      consonent[name][1].split())
            }
    return TestBank(voice='Jian (Premium)',
                    table=table,
                    cheatsheet=cheatsheet)
