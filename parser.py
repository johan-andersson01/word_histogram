import argparse
import re
from glob import iglob
from pathlib import Path
from collections import defaultdict


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--blacklist', type=Path)
    return parser.parse_args()


def filter_words(histogram: defaultdict):
    filtered_words = []
    for w, i in histogram.items():
        if w.endswith('\'s') and w[:-2] in histogram:
            histogram[w[:-2]] += i
            filtered_words.append(w)
        elif w.endswith('s') and w[:-1] in histogram:
            histogram[w[:-1]] += i
            filtered_words.append(w)
    return filtered_words


def parse_files(paths: list):
    for f in paths:
        words = f.read_text().lower()
        words = re.sub(r'[^\'a-zA-Z]', ' ', words)
        words = words.split()
        for w in words:
            yield w


if __name__ == "__main__":
    args = get_args()
    assert args.input.exists()
    if args.input.is_dir():
        subtitle_files = [Path(f) for f in iglob(f'{args.input}/*')]
        assert len(subtitle_files) > 0
    else:
        subtitle_files = [args.input]

    if args.blacklist:
        blacklist = defaultdict()
        assert args.blacklist.exists() and args.blacklist.is_file()
        words = args.blacklist.read_text().lower().split()
        for w in words:
            blacklist[w] = 1
        
    histogram = defaultdict(int)


    for w in parse_files(subtitle_files):
        histogram[w] += 1

    for w in filter_words(histogram):
        del histogram[w]

    for w in blacklist.keys():
        if w in histogram:
            del histogram[w]

    for w, i in sorted(histogram.items(), key=lambda iw: iw[1]):
        print(w, i)
