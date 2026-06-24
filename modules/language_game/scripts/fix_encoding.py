# -*- coding: utf-8 -*-
"""Fix smart quotes in generate_questions.py"""
import os

path = r'd:\STUDY\modules\language_game\scripts\generate_questions.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace curly/smart quotes with straight ASCII quotes
pairs = [
    ('\u201c', '"'),  # left double quotation mark
    ('\u201d', '"'),  # right double quotation mark
    ('\u2018', "'"),  # left single quotation mark
    ('\u2019', "'"),  # right single quotation mark
    ('\u2026', '...'),  # horizontal ellipsis
    ('\u300c', '"'),  # left corner bracket
    ('\u300d', '"'),  # right corner bracket
]

for bad, good in pairs:
    content = content.replace(bad, good)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed encoding issues in generate_questions.py')
