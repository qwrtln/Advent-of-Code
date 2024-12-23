# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     102.4 ms ±   6.3 ms    [User: 89.3 ms, System: 13.0 ms]
#   Range (min … max):    95.3 ms … 123.5 ms    30 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     133.3 ms ±  11.1 ms    [User: 109.9 ms, System: 21.9 ms]
#   Range (min … max):   124.4 ms … 166.9 ms    19 runs
#
import collections


def parse_lan(puzzle):
    lines = open(puzzle).read().strip().split("\n")
    lan = collections.defaultdict(set)
    for link in lines:
        comp1, comp2 = link.split("-")
        lan[comp1].add(comp2)
        lan[comp2].add(comp1)
    return lan


def part1(lan):
    threes = set()
    for computer, neighbours in lan.items():
        for nei in neighbours:
            potential = set([computer, nei])
            common_neis = lan[computer] & lan[nei]
            for common in common_neis:
                party = ",".join(sorted(potential | {common}))
                threes.add(party)

    result = 0
    for three in threes:
        if any([c.startswith("t") for c in three.split(",")]):
            result += 1
    return result


def all_neis_interconnected(lan, common_neis):
    for c in common_neis:
        to_check = lan[c] & common_neis
        if not to_check:
            return False
        for n in to_check:
            if n not in common_neis:
                return False
    return True


def part2(lan):
    candidate = None
    length = 0
    already_checked = set()
    for computer, neighbours in lan.items():
        for nei in neighbours:
            potential = set([computer, nei])
            common_neis = lan[computer] & lan[nei]
            prospect_net = potential | common_neis
            party = ",".join(sorted(prospect_net))
            if common_neis and party not in already_checked:
                already_checked.add(party)
                if all_neis_interconnected(lan, common_neis):
                    if len(party) > length:
                        length = len(party)
                        candidate = party
    return candidate


lan = parse_lan("inputs/23.txt")
print("1:", part1(lan))
print("2:", part2(lan))
