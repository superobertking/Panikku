from test_bank import TestBank, find_voice


def gen_jis_symbol_table(base: str):
    us_base = set('"&\'()=~^@`{}[];+:*')
    jis_all = us_base | set('|\\_')

    if base == "us":
        return TestBank(table=us_base)
    # please only use this if you have JIS keyboard
    elif base == "jis":
        return TestBank(table=jis_all)
    else:
        # TODO: support ISO keyboard as base
        raise ValueError("Unsupported base keyboard type!")


# Separated from symbol table because it needs
# TODO: add katakana support
# TODO: add dakuon and yoon support
# TODO: maybe use ncurses to read keystrokes directly?
def gen_jis_kana_table(base: str):
    us_map = [
        ("1234567890)-",    "ぬふあうえおやゆよわをほ"),
        ("qwertyuiop]\\",   "たていすかんなにらせむへ"),
        ("asdfghjkl;'\"",   "ちとしはきくまのりれけろ"),
        ("zxcvbnm,./",      "つさそひこみもねるめ"),
    ]

    create_table = lambda map: {kana: key for m in map for key, kana in zip(*m)}

    if base == "us":
        return TestBank(voice=find_voice('ja_JP'), table=create_table(us_map))
    else:
        # TODO: support ISO keyboard as base
        raise ValueError("Unsupported base keyboard type!")
