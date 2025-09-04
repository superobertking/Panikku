# Panikku

(パニック, Panic!)

<img alt="Ferris Sticker" src="https://doc.rust-lang.org/stable/book/img/ferris/does_not_compile.svg" width="100">

An automated quiz tool to memorize stuff, such as learning languages.

Personal toy project. Written when I was trying to memorize Japanese kana. It can be generalized to vocabulary learning of any language.

## Features

- Romanization tests (with alias support)
- Typing tests
- Short-term memory (not LSTM) weight-based randomization
  - Weight system based on answer correctness, response time, and unvisited time.
- Speaks the word after each test (only works on macOS)
- Summary of the test
- Special command for the user to take a short break :)
- Special command to show cheat sheet (not all datasets have one).

## Datasets

Currently supported modules:

- Hiragaka and Katakana
- Hangul
- JIS keyboard symbol locations (typing test only)

## Usage

### Command line

Global usage for `main.py`:

```text
usage: panikku [-h] [--no-say] [--say-first] [--notify-wrong] [--typing]
               [--reverse] [--recitation] [-v VOICE]
               {hiragana,katakana,hangul,jis,jiskana} ...

positional arguments:
  {hiragana,katakana,hangul,jis,jiskana}

optional arguments:
  -h, --help            show this help message and exit
  --no-say              Say the word using TTS after each quiz
  --say-first           Say the word before each quiz. Otherwise, say it after
                        each quiz.
  --notify-wrong        Notify wrong answer by saying 'wrong answer'.
  --typing              Typing test instead of default romanization quiz
  --reverse             Reverse romanization and character
  --recitation          Play sound first and do not show the character
                        (implies --say and --say-first)
  -v VOICE, --voice VOICE
                        Override voice choice
```

Usage of each dataset can be get from `./main.py <dataset> -h`. The general
composition is in the form of:

```text
./main.py [--options] <dataset> <testsets...>
```

### Example

```bash
./main.py katakana   # or ./main.py katakana normal
```

Output:

```text
Using voice: Kyoko (Enhanced)
Loaded test set size: 46
Press CTRL-D (^D) to finish test and print testing weights.
Type 'wait' to take a break.
Type '?' to show cheatsheet.

'ユ' is: yo
Wrong! It should be 'yu'.
'ク' is: ku
Correct! Time elapsed 9.807545s.
'メ' is: me
Correct! Time elapsed 5.141610s.
'ク' is: ku
Correct! Time elapsed 1.350759s.
'ヘ' is: ke
Wrong! It should be 'he'.
'ロ' is: wait
Type 'c' to continue... c
'ン' is: nn
Correct! Time elapsed 5.277924s.
......
'ハ' is: ha
Correct! Time elapsed 0.942780s.
'ユ' is: ^D
Correct rate stats:
ナ: 10/10, 0.383541
キ: 7/7, 0.520720
......
ネ: 13/14, 6.021254
フ: 37/42, 10.321055
Unvisited vocabularies:
{'タ', 'ト', 'ル', 'キ', 'ユ', 'コ', 'ニ', 'ク', 'ノ', 'ホ', 'ミ', 'ヤ', 'ン'}
```

### APIs

Main APIs are the following classes and functions. See documentations at
definition and usages in module files, in a Hack-It-Yourself style. :)

```python
from tester import Tester, TesterOptions
from test_bank import TestBank, find_voice
```

## Future

- Custom weight algorithm
- Custom vocabulary book
