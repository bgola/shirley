#!/usr/bin/python2
# coding: utf-8

import re, datetime, random, time
CHAIN_LENGTH=3
START = '\1'
END = '\0'
ansi_escape = re.compile(r'\x1b[^m]+m')


data = {}
data_b = {}
def split(msg, length):
    m = msg.split()
    m = [START] + m + [END]
    for i in range(len(m) - length):
        yield m[i:i + length + 1]

def process(m, length=CHAIN_LENGTH, d=data):
    m = m.lower()
    m.replace("(", "")
    m.replace(")", "")
    m.replace("[", "")
    m.replace("]", "")
    for y in re.split("[.!?;\n]", m):
        for x in split(y, length):
            key = tuple(z.replace(",", "") for z in x[:length])
            value = x[length]
            d[key] = d.get(key, []) + [value.replace(",", "")]
            #key2 = tuple(z.replace(",", "") for z in x[1:length+1])
            #data_b[key2] = data_b.get(key2, []) + [x[0]]

def say(m):
    r = [ w for w in m.strip().split() if len(w) > 2 ]
    if not r:
        return ""
    out = random.choice(r)
    new = random.choice(data.get((START, out), [END]))
    if new == END:
        return say(m.replace(out, ""))
    c = random.choice(data.get((START, out, new), [END]))
    out = "%s %s" % (out, new)
    while c != END:
        out = "%s %s" % (out, c)
        o = out.split()
        c = random.choice(data.get((o[-3], o[-2], o[-1]), [END]))
    return out
try:
    for line in open("input.txt"):
        process(line)
        process(line, 2, data)
except IOError:
    pass
if __name__ == "__main__":
    while True:
        print say(raw_input("> "))
