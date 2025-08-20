from dataclasses import dataclass, field
from typing import Dict
from types import FunctionType
import subprocess


@dataclass
class TestBank:
    table: Dict[str, str]
    voice: str = None
    cheatsheet: str = None
    same_sound: set = field(default_factory=set)


def find_voice(lang: str, filter=None, search: str = None):
    """\
    Finds a proper voice for some language from `say -v?`, preferring Premium
    and Enhanced voices. For example, language string could be 'ko_KR'. The
    language string is not strictly formatted, but it is used as split string
    to extract the name from first column, so be careful when using it.

    Example 'say -v?' output could be (filtered only by 'ko_KR'):
    Jian (Premium)      ko_KR    # 안녕하세요. 제 이름은 지안입니다.
    Minsu (Enhanced)    ko_KR    # 안녕하세요. 제 이름은 민수입니다.
    Yuna                ko_KR    # 안녕하세요. 제 이름은 유나입니다.

    `filter` can be either str or a function. A functions should return True
    if the passed name string is acceptable.

    `search` searches a preferred name, e.g. 'Jian', but will fall back to
    other options if the search string does not exist. Search has higher
    priority than Premium/Enhanced.
    """

    output = subprocess.check_output(['say', '-v?'], text=True)

    best = None

    for line in output.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue

        if lang not in line:
            continue

        name = line[:line.find(lang)].strip()

        if filter is None:
            pass
        elif isinstance(filter, str):
            if filter not in name:
                continue
        elif isinstance(filter, FunctionType):
            if not filter(name):
                continue
        else:
            raise ValueError(f"Invalid filter type: {type(filter)}")

        if best is None:
            best = name
            continue

        if search is not None:
            if search in best and search not in name:
                continue
            if search in name and search not in best:
                best = name
                continue
            # otherwise, use regular premium/enhanced checks

        if '(Premium)' in name:
            best = name
        elif '(Enhanced)' in name:
            if '(Premium)' not in best:
                best = name
        else:
            if '(Enhanced)' not in best and '(Premium)' not in best:
                best = name

    return best
