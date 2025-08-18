# Panikku

(パニック, Panic!)

<img alt="unsafe" src="https://doc.rust-lang.org/book/img/ferris/unsafe.svg" width="100">

Personal toy project. Written when I was trying to memorize Japanese kana. It can be generalized to vocabulary learning of any language.

## Features

 - Short-term memory (not LSTM) weight-based randomization
    - weight system based on answer correctiveness, response time and unvisited time.

- Speaks the word after each test (only works on macOS)
- Summarization of the test
- Special command for the user to take a short break :)

## Usage

### Example

```python
from tester import Tester
from kana import gen_kana_table
Tester(gen_kana_table())()
```

`kana.py` is a dataset for Japanese kana. I may further include vocabularies in my daily use.

### Output

Just examples :)

```
'ナ' is: na
Correct! Time elapsed 1.683866s.
'ユ' is: yo
Wrong! It should be 'yu'.
'ク' is: ku
Correct! Time elapsed 9.807545s.
'メ' is: me
Correct! Time elapsed 5.141610s.
'ク' is: ku
Correct! Time elapsed 1.350759s.
'メ' is: me
Correct! Time elapsed 15.718419s.
'ヘ' is: ke
Wrong! It should be 'he'.
'ル' is: ru
Correct! Time elapsed 1.783516s.
'ロ' is: wait
Type 'break' to continue...
Type 'break' to continue... break
'ン' is: nn
Correct! Time elapsed 5.277924s.
'チ' is: ti
Correct! Time elapsed 1.549908s.
......
'ハ' is: ha
Correct! Time elapsed 0.942780s.
'ウ' is: u
Correct! Time elapsed 0.965341s.
'ユ' is: ^D
Correct rate stats:
ナ: 10/10, 0.383541
キ: 7/7, 0.520720
ヤ: 9/9, 0.548169
ニ: 6/6, 0.553905
カ: 3/3, 0.577832
ン: 7/7, 0.642021
ウ: 4/4, 0.743358
サ: 7/7, 0.825617
......
ソ: 8/8, 1.734599
ラ: 13/13, 1.833236
ケ: 7/7, 1.863955
レ: 10/10, 2.071733
ヲ: 10/10, 2.414260
ホ: 16/16, 2.654242
メ: 31/32, 3.662712
ヘ: 29/31, 4.360236
ヌ: 21/22, 5.781667
ネ: 13/14, 6.021254
フ: 37/42, 10.321055
```

If there are unvisited vocabularies, it will have something like:

```
Unvisited vocabularies:
{'タ', 'ト', 'ル', 'キ', 'ユ', 'コ', 'ニ', 'ク', 'ノ', 'ホ', 'ミ', 'ヤ', 'ン'}
```

## TODO

 - Customizable weight algorithm
 - TODO: test set argument parsing
