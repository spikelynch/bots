#!/usr/bin/env python3

import re
import subprocess
import yaml

PAGE_RE = "^(.*?)\("
BRACKET_RE = "^\S*?\s\[(.*?)\]"
EXCLUDE_RE = "https?://"

def smart_fix(line):
    l = line.strip()
    if l[-1] == '-':
        return l[:-1]
    return l + ' '

def smart_join(lines):
    joined = ''.join([ smart_fix(l) for l in lines ])
    joined = joined.strip()
    w_re = re.compile('\s+')
    joined = w_re.sub(' ', joined)
    return joined

def read_man(page):
    try:
        manbytes = subprocess.check_output(["man", page])
    except subprocess.CalledProcessError as e:
        print("Error calling man: %s" % e)
        return []
    manstr = manbytes.decode()
    bugs = []
    bflag = False
    clean_re = re.compile('(.)[_\x08](.)')
    section_re = re.compile('^([A-Z][A-Z ]+)')
    for line in manstr.split('\n'):
        clean = clean_re.sub(r'\1', line)
        m = section_re.search(clean)
        if m:
            section = m.group(0)
            if section == 'BUGS':
                bflag = True
            elif bflag:
                bflag = False
        elif bflag and clean:
            bugs.append(clean)
    text = smart_join(bugs)
    return text

def list_man_pages():
    manlistbytes = subprocess.check_output(["apropos", ","])
    manlist = manlistbytes.decode()
    page_re = re.compile(PAGE_RE)
    bracket_re = re.compile(BRACKET_RE)
    pages = {}
    for item in manlist.split("\n"):
        m = page_re.search(item)
        if m:
            p = m.group(1)
            m2 = bracket_re.search(p)
            if m2:
                page = m2.group(1)
            else:
                page = m.group(1).strip()
            pages[page] = 1
    return list(pages.keys())

def full_stop(s):
    if not s[-1] == '.':
        return s + '.'
    else:
        return s

def split_sentences(text):
    sep_re = re.compile('\.\s+')
    return [ full_stop(s) for s in sep_re.split(text) ]

unique_bugs = {}

pages = list_man_pages()

for p in pages:
    bugs = read_man(p)
    mask_re = re.compile(EXCLUDE_RE)
    if bugs:
        for sent in split_sentences(bugs):
            if len(sent) < 141 and not mask_re.search(sent):
                if sent in unique_bugs:
                    unique_bugs[sent] += 1
                else:
                    unique_bugs[sent] = 1

for sent in unique_bugs.keys():
    print(sent)
