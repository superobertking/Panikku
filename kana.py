from test_bank import TestBank, find_voice


# Glossary
# Hiragana: 平仮名（ひらがな）
# Katakana: 片仮名（かたかな）
# kana:
# dakuon: 濁音（だくおん）
# yoon: 拗音（ようおん）
# gojuon: 五十音（ごじゅうおん）
# sokuon:


hira_normal = (
    ("", "あいうえお"),
    ("k", "かきくけこ"),
    ("s", "さしすせそ"),
    ("t", "たちつてと"),
    ("n", "なにぬねの"),
    ("h", "はひふへほ"),
    ("m", "まみむめも"),
    ("r", "らりるれろ"),
)
hira_normal_special = {
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "わ": "wa", "を": "wo",
    "ん": ["nn", "n"],
    # overwrite alias below
    "し": ["shi", "si"],
    "ち": ["chi", "ti"],
    "つ": ["tsu", "tu"],
    "ふ": ["fu", "hu"],
}
hira_dakuon = (
    ("g", "がぎぐげご"),
    ("z", "ざじずぜぞ"),
    ("d", "だぢづでど"),
    ("b", "ばびぶべぼ"),
    ("p", "ぱぴぷぺぽ"),
)
hira_dakuon_special = {
    "じ": "ji",
    "ぢ": ["ji", "dji"]
}
hira_yoon_normal = (
    ("ky", "き"),
    #  ("sh", "し"),
    ("sy", "し"),
    #  ("ch", "ち"),
    ("ty", "ち"),
    ("ny", "に"),
    ("hy", "ひ"),
    ("my", "み"),
    ("ry", "り"),
)
hira_yoon_dakuon = (
    ("gy", "ぎ"),
    #  ("j", "じ"),
    ("jy", "じ"),
    #  ("dj", "ぢ"),
    ("dy", "ぢ"),
    ("by", "び"),
    ("py", "ぴ"),
)

kata_normal = (
    ("", "アイウエオ"),
    ("k", "カキクケコ"),
    ("s", "サシスセソ"),
    ("t", "タチツテト"),
    ("n", "ナニヌネノ"),
    ("h", "ハヒフヘホ"),
    ("m", "マミムメモ"),
    ("r", "ラリルレロ"),
)
kata_normal_special = {
    "ヤ": "ya", "ユ": "yu", "ヨ": "yo",
    "ワ": "wa", "ヲ": "wo",
    "ン": ["nn", "n"],
    # overwrite alias below
    "シ": ["shi", "si"],
    "チ": ["chi", "ti"],
    "ツ": ["tsu", "tu"],
    "フ": ["fu", "hu"],
}
kata_dakuon = (
    ("g", "ガギグゲゴ"),
    ("z", "ザジズゼゾ"),
    ("d", "ダヂヅデド"),
    ("b", "バビブベボ"),
    ("p", "パピプペポ"),
)
kata_dakuon_special = {"ジ": "ji"}
kata_yoon_normal = (
    ("ky", "キ"),
    #  ("sh", "シ"),
    ("sy", "シ"),
    #  ("ch", "チ"),
    ("ty", "チ"),
    ("ny", "ニ"),
    ("hy", "ヒ"),
    ("my", "ミ"),
    ("ry", "リ"),
)
kata_yoon_dakuon = (
    ("gy", "ギ"),
    #  ("j", "ジ"),
    ("jy", "ジ"),
    #  ("dj", "ヂ"),
    ("dy", "ヂ"),
    ("by", "ビ"),
    ("py", "ピ"),
)


vowels = "aiueo"
hira_yoon_vowels = ("auo", "ゃゅょ")
kata_yoon_vowels = ("auo", "ャュョ")
#  kata_yoon_vowels = ("aueo", "ャュェョ")


def gen_kana_table(normal=True, dakuon=False, yoon_normal=False, yoon_dakuon=False,
                   type='hira'):

    postfixes = ['normal', 'normal_special', 'dakuon',
                 'dakuon_special', 'yoon_normal', 'yoon_dakuon']

    if type not in ['hira', 'kata']:
        raise ValueError(f'Unknown kana type: {type}')

    kana = {}
    for postfix in postfixes:
        kana[postfix] = globals()[type + '_' + postfix]
    #  v = vars()

    kana_table = {}

    if normal:
        kana_table.update({c: name+e for name, chars in kana['normal']
                           for c, e in zip(chars, vowels)})
        kana_table.update(kana['normal_special'])
    if dakuon:
        kana_table.update({c: name+e for name, chars in kana['dakuon']
                           for c, e in zip(chars, vowels)})
        kana_table.update(kana['dakuon_special'])
    if yoon_normal:
        kana_table.update({char+c: name+e for name, char in kana['yoon_normal']
                           for e, c in zip(*kana['yoon_vowels'])})
    if yoon_dakuon:
        kana_table.update({char+c: name+e for name, char in kana['yoon_dakuon']
                           for e, c in zip(*kana['yoon_vowels'])})

    #  print(kana_table)
    return TestBank(table=kana_table, voice=find_voice('ja_JP'))
