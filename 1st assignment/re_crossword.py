# Sorry for the bad structure. My first Python program!
import argparse
import csv
import re
import string

import sre_yield

parser = argparse.ArgumentParser()
parser.add_argument("crossword_file", help="name of crossword file")
parser.add_argument("regular_expressions_file",
                    help="name of regular expressions file")

args = parser.parse_args()
joints = {}
words = {}
regex = []
regex_used = {}
all_words = {}

# Reading the csv file and creating the words and joints dicts.
with open(args.crossword_file, newline='') as c:
    data = csv.reader(c)
    for row in data:
        joints[int(row[0])] = []
        words[int(row[0])] = row[1]
        for i in range(2, len(row), 2):
            joints[int(row[0])].append((int(row[i]), int(row[i+1])))

# Reading the txt file and creating the regex list.
with open(args.regular_expressions_file, newline='') as r:
    for line in r:
        regex.append(line[:-1])

# Creating a dict with all the possible values of the certain regex list.
for r in regex:
    all_words[r] = set(sre_yield.AllStrings(
        r, max_count=5, charset=string.ascii_uppercase))


# It is used for efficiently update certain words with the lettes or their neighbours
# and also to update the dict with the regex that 've been used so far.
def update(x, word):
    for v in joints[x]:
        for d in joints[v[0]]:
            if d[0] == x:
                i = d[1]
        # Here we are modifying the string using slices.
        words[v[0]] = words[v[0]][:v[1]] + word[i] + words[v[0]][(v[1]+1):]
        if '.' not in words[v[0]]:
            if regex_used[v[0]] == None:
                for k, val in all_words.items():
                    if words[v[0]] in val and (k not in regex_used.values()):
                        regex_used[v[0]] = k
        else:
            regex_used[v[0]] = None


# This is for the initial update of the grid because not all words contain the
# letters of the their neighbours and also to check if some regex have already
# been used in the crossword.
for k, v in words.items():
    for ch in v:
        if '.' != ch:
            update(k, v)
    if v in regex:
        regex_used[k] = v


# Check to see if the crossword has been completed by checking if all
# the regex have been used.
def is_finished():
    b = True
    for v in regex:
        if v not in regex_used.values():
            b = False
    return b


# It finds the next word to be solved.
def best_word():
    min = 2.0
    best = 0
    for k, word in words.items():
        count = 0
        for ch in word:
            if ch == '.':
                count += 1
        if (count != 0) and ((count / len(word)) < min):
            min = count / len(word)
            best = k
    return best


# This is the solution of the crossword. We are actually using our given words by
# converting those into regural expressions and trying to find matches in the dictionary
# with all the possible words that we created from the regex.
def solve_puzzle():
    i = best_word()
    next = words[i]
    re_next = re.compile(next)
    for k, v in all_words.items():
        if k not in regex_used.values():
            for s in v:
                y = re_next.fullmatch(s)
                if y:
                    words[i] = s
                    regex_used[i] = k
                    update(i, words[i])
                    if not is_finished():
                        solve_puzzle()
                    # Here we break because if it continues after it has solve it
                    # it ruins it again.
                    if is_finished():
                        break
        if is_finished():
            break
    # This is for bringing the grid to it's previous state due to recursion.
    if not is_finished():
        words[i] = next
        update(i, words[i])
        regex_used[i] = None


solve_puzzle()
for k, v in sorted(words.items()):
    print(k, regex_used[k], v)
