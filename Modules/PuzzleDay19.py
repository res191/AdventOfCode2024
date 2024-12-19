from functools import cache

from Modules.GenericPuzzle import Puzzle
from Modules.ReadFiles import read_file_as_list

class PuzzleDay19(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.rulebook = None

    def read_file(self):
        file_output = read_file_as_list(self.filename)
        self.rulebook = file_output[0].split(', ')
        # sort the rulebook from longest to shortest to support a greedy search
        self.rulebook.sort(key=len, reverse=True)
        self.input = file_output[2::]

    ''' a greedy (i.e. most amount of chacters in one go) depth first search'''
    def item_in_rulebook(self, item):
        # if we exactly match one of the rules return true
        for rule in self.rulebook:
            if item == rule:
                return True

        # if we have any partial matches try to see if remaining string is found in the rulebook
        for rule in self.rulebook:
            if item.startswith(rule) and self.item_in_rulebook(item.removeprefix(rule)):
                return True
        # if we have been through all the rules and there are no rules that result in a match return false
        return False

    ''' exhaustive depth search -- cache the calls for quicker performance'''
    @cache
    def item_rulebook_combos(self, item):
        # we have removed all the characters we have no more left which means this is a successful combination
        if item == '':
            return 1

        #if our item has something try all the combinations possible
        valid_rules =[rule for rule in self.rulebook if item.startswith(rule)]

        # we have no valid combinations so return 0
        if len(valid_rules) == 0:
            return 0

        return sum([self.item_rulebook_combos(item.removeprefix(rule)) for rule in valid_rules])

    def part1(self):
        return sum([self.item_in_rulebook(item) for item in self.input ])

    def part2(self):
        return sum([self.item_rulebook_combos(item) for item in self.input ])
