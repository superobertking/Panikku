from test_bank import TestBank


def gen_jis_symbol_table(base: str):
    us_base = set('"&\'()=~^@`{}[];+:*')
    jis_all = us_base | set('|\\_')

    # please only use this if you have JIS keyboard
    if base == "us":
        return TestBank(table=us_base)
    elif base == "jis":
        return TestBank(table=jis_all)
    else:
        # TODO: support ISO keyboard as base
        raise ValueError("Unsupported base keyboard type!")
