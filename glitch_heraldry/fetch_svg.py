#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests, re, os.path
from urllib.parse import urljoin, urlparse

LIST = 'https://en.wikipedia.org/wiki/List_of_coats_of_arms'
OUTFILE = 'svg.txt'
SVG = './svg/'

PATH_RE = re.compile('/wiki/File:(.*)$')

def get_svg(href):
    resp = requests.get(href)
    if resp.status_code == requests.codes.ok:
        soup = BeautifulSoup(resp.text, 'html.parser')
        for link in soup.find_all('a'):
            lhref = link.get('href')
            if lhref and lhref[-3:] == 'svg':
                return urljoin(href, lhref)
    return None


def download_svg(svg):
    resp = requests.get(svg)
    if resp.status_code == requests.codes.ok:
        o = urlparse(svg)
        p = o.path
        m = PATH_RE.search(p)
        if m:
            f = os.path.join(SVG, m.group(1))
            with open(f, 'w') as pf:
                pf.write(resp.text)
        else:
            print("Parse error: {}".format(p))


resp = requests.get(LIST)
list_soup = BeautifulSoup(resp.text, 'html.parser')


svg_links = []

for link in list_soup.find_all('a'):
    href = urljoin(LIST, link.get('href'))
    
    if href:
        svg = get_svg(href)
        if svg:
            if svg not in svg_links:
                print(svg)
                svg_links.append(svg)
                #download_svg(svg)

with open(OUTFILE, 'w') as f:
    for link in svg_links:
        f.write(link + '\n')

print('Wrote links to {}'.format(OUTFILE))
        
