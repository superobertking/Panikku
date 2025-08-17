import random
import os
import time
from dataclasses import dataclass

from test_bank import TestBank


class HistItem:
    def __init__(self, idx):
        self.score = 0
        self.total = 0
        self.idx = idx

    def __iadd__(self, rhs):
        self.score += rhs[0]
        self.total += rhs[1]
        return self

    def __str__(self):
        return f'{self.score}/{self.total}'

    def __repr__(self):
        return f'<HistItem {self.score}/{self.total}>'

    def __lt__(self, rhs):
        # TODO: allow compare with self.total == 0
        return (self.score / self.total, self.total) \
            < (rhs.score / rhs.total, rhs.total)


class Sampler:
    def __init__(self, iterable, weights):
        self._choices = list(enumerate(sorted(iterable)))
        self._weights = weights
        self._last = None
        self._check_dimensions()

    def _check_dimensions(self):
        if len(self._weights) != len(self._choices):
            raise ValueError('Wrong dimensions')

    def __call__(self):
        """\
        Sample once and get a different one from the last one.
        Input must guarantee at least 2 available results each time.
        """
        while True:
            idx, key = random.choices(self._choices, self._weights)[0]
            if key != self._last:
                self._last = key
                return idx, key

    def update_weights(self, func):
        self._weights = func(self._weights)
        self._check_dimensions()

    def get_weights(self):
        # How to ensure weights r/o
        return self._weights


@dataclass
class TesterOptions:
    say: bool = False


class Tester:
    """\
    Tester class.
    """

    def __init__(self, test_bank: TestBank, options: TesterOptions = None):
        # shorthand of table
        self._table = test_bank.table
        # store the original bank that contains other settings
        self._bank = test_bank
        self._options = TesterOptions() if options is None else options

    @staticmethod
    def _time_user_input():
        try:
            t0 = time.time()
            user_input = input()
            t1 = time.time()
            duration = t1 - t0
            # Be more accurate, postpone strip
            user_input = user_input.strip()
            return user_input, duration
        except (EOFError, KeyboardInterrupt):
            return None, None  # return empty

    @staticmethod
    def _update_weights(weights, idx, duration, test_key, correct):
        # TODO: cleanup all the magic numbers (parameters)
        # Update weights based on short-term memory? (maybe)
        # backup weights[idx]
        new_weight = weights[idx]
        for i, w in enumerate(weights):
            if w < 1.0:
                weights[i] = min(1.0, w + 0.01)

        # Update weight based on correctness
        if correct:
            if new_weight > 1.0:
                new_weight = 0.9 * new_weight + 0.1
            else:
                new_weight *= 0.66
        else:
            new_weight += 10.0

        # Update weights based on type time
        # add 0.2 weight of (duration - 1.5s per kana)
        # len(test_key) mush be at least 1
        new_weight = new_weight + 0.2 * (duration - 1.5 * len(test_key))
        # Commit new weight
        weights[idx] = max(new_weight, 0.01)
        return weights

    def __call__(self):
        histogram = {}
        sampler = Sampler(self._table.keys(), [1.0] * len(self._table))

        print("Press CTRL-D (^D) to finish test and print testing weights.\n"
              "Type 'wait' to take a break.\n"
              "Type '?' to show cheatsheet.\n")

        redo_test = False

        # Infinite loop
        while True:
            if redo_test:
                redo_test = False
            else:
                idx, test_key = sampler()
            test_value = self._table[test_key]

            # Start once test
            print(f"'{test_key}' is: ", end='')
            user_input, duration = self._time_user_input()
            # Test once finished

            if user_input is None:
                break  # END of test

            # workflow commands
            if user_input == 'wait':
                while True:
                    print("Type 'c' to continue... ", end='')
                    if input().strip() == 'c':
                        break
                redo_test = True
                continue  # Go into the next loop (word)
            elif user_input == '?':
                if self._bank.cheatsheet is not None:
                    print("Cheatsheet:")
                    print(self._bank.cheatsheet)
                else:
                    print("No cheatsheet found!")
                redo_test = True
                continue

            correct = test_value == user_input

            # Display result
            if correct:
                print(f"Correct! Time elapsed {duration:6f}s.")
            else:
                print(f"Wrong! It should be '{test_value}'.")
            # Say the word
            if self._options.say and self._bank.voice is not None:
                os.system(f"say -v '{self._bank.voice}' {test_key} &")

            # Update weights
            sampler.update_weights(lambda ws: self._update_weights(
                ws, idx, duration, test_key, correct))

            # Update stats
            histogram.setdefault(test_key, HistItem(idx))
            histogram[test_key] += (int(correct), 1)

        print()

        if histogram:
            weights = sampler.get_weights()
            stat = [(weights[s.idx], s, c) for c, s in histogram.items()]
            stat.sort()
            print('Correct rate stats:')
            for w, s, c in stat:
                print(f'{c}: {s}, {w:6f}')

            unvisited = set(histogram.keys()) ^ set(self._table.keys())
            if unvisited:
                print('Unvisited vocabularies:')
                print(unvisited)
