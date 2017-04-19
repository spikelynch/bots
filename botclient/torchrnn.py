#!/usr/bin/env python

import subprocess, os

TORCHRNN = os.environ['TORCH_RNN']

TRCMD = [ os.environ['TORCH_TH'], TORCHRNN + '/sample.lua' ]
TRARGS = { '-gpu': '-1' }

SAMPLE_SIZE = 5
DEFAULT_LINE = 140


def run_sample(model, temperature, start, nchars):
    cmd = TRCMD
    args = TRARGS
    args['-checkpoint'] = model
    args['-temperature'] = str(temperature)
    args['-length'] = str(nchars)
    args['-start_text'] = start
    for k, v in args.items():
        cmd.append(k)
        cmd.append(v)
    return subprocess.check_output(cmd, cwd=TORCHRNN)

def generate_lines(model, temperature=1.0, n=1, min_length=1, max_length=DEFAULT_LINE):
    lines = []
    while len(lines) < n:
        text = run_sample(model, temperature, '', max_length * SAMPLE_SIZE).decode('utf-8')
        ls = text.split('\n')[1:]
        for l in ls:
            if not l or len(l) > max_length or len(l) < min_length:
                continue
            lines.append(l)
    return lines[:n]

