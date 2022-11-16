#!/usr/bin/env python

from typing import Tuple, List
import numpy as np
import logging as lg
from numpy import ndarray


def _convert(raw):
    """
    Takes in text file and converts to nested list
    :param raw: name of text file of votes (each vote on new line) see example_votes.txt
    :return: nested list format of votes and list of all candidates
    """
    with open(raw, 'r') as file:
        text = file.read()
        list_of_votes = text.split("\n")
    votes = []
    candidates = set()
    for vote in list_of_votes:
        temp = vote.split(" ")
        struct_vote = []
        for choice in temp:
            names = choice.split(",")
            for name in names:
                candidates.add(name)
            struct_vote.append(names)
        votes.append(struct_vote)
    return votes, list(candidates)

class Schulze:
    def __init__(self, votes):
        """
        Creates Schulze object
        :param votes: text file of votes (each vote on new line) see example_votes.txt
        :param nominees: List of names, for example_votes.txt: ["alpha","bravo","charlie"]
        """
        self.votes, nominees = _convert(votes)
        self.nominees = sorted(nominees)
        self.names_to_index = {}
        self.index_to_names = {}
        for i, nominee in enumerate(self.nominees):
            self.names_to_index[nominee] = i
            self.index_to_names[i] = nominee
        self._vote_matrix = np.zeros((len(nominees), len(nominees)))

    def _count(self):
        """Populates private matrix with vote reports comparing individual candidates.
        The value in row i column j represents number of votes where candidate i was
        preferred over j.
        Roughly linear dependent on number of votes if number of candidates are considerably fewer."""
        # reset _vote_matrix
        self._vote_matrix = np.zeros((len(self.nominees), len(self.nominees)))

        # Iterate over each vote
        # For each vote iterate over each candidate to count wins
        for vote in self.votes:
            for nominee in self.nominees:
                winner_index = self.names_to_index[nominee]
                found = False  # Checks if nominee has been found in vote
                not_losers = []  # The candidates not to be counted as losers against nominee
                for priority_step in vote:
                    if (nominee in priority_step) and not found:
                        found = True
                    not_losers.extend(priority_step)
                    if found:
                        break
                if found:
                    for candidate in self.nominees:
                        if candidate in not_losers:
                            continue
                        loser_index = self.names_to_index[candidate]
                        self._vote_matrix[winner_index, loser_index] += 1

    def _get_strength(self):
        """Calculates the strength matrix needed for the Schulze method
        Algorithm used can be found on wikipedia page:
        https://en.wikipedia.org/wiki/Schulze_method"""
        c = len(self.nominees)
        d = self._vote_matrix
        p = np.zeros((c,c))

        for i in range(c):
            for j in range(c):
                if i == j:
                    continue
                if d[i, j] > d[j, i]:
                    p[i, j] = d[i, j]
                else:
                    p[i, j] = 0

        for i in range(c):
            for j in range(c):
                if i == j:
                    continue
                for k in range(c):
                    if i != k and j != k:
                        p[j, k] = max(p[j, k], min(p[j, i], p[i, k]))
        return p

    def get_results(self, vacancies: int = 1) -> Tuple[List[str], List[str], ndarray, ndarray]:
        """
        Counts votes and returns winners. Want more info? Use brain.
        :param vacancies: Number of vacant seats for the post
        :return: Winners in order of priority, full reports as well as pairwise and strength matrices
        """
        self._count()
        p = self._get_strength()  # Strength matrix
        results, ties = self.sort_results(p)
        full_results = [self.index_to_names[i] for i in results]
        winners = full_results[:vacancies]
        return winners, full_results, self._vote_matrix, p, ties

    def sort_results(self, p: np.array) -> list:
        """
        Calculates preferred order of nominees
        :param p: Strength matrix
        :return: Sorted order of preference as well as eventual ties
        """
        n = p.shape[0]
        win_count = [0 for i in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if p[i, j] > p[j, i]:
                    win_count[i] += 1
                elif p[i, j] < p[j, i]:
                    win_count[j] += 1
                else:
                    # No action is performed here, unknown if this is has an effect in the long run
                    # Other than ties, which is checked in the next step
                    pass

        # Check ties:
        ties = self._check_ties(win_count)
        if ties:
            lg.warning(f' The following ties were found: {ties}.')

        results = [i for i in range(n)]
        results.sort(key=lambda x: win_count[x], reverse=True)
        return results, ties

    def _check_ties(self, win_count: list):
        """
        Checks whether any ties are present and reports them
        :param win_count: Number of 'wins' for each index
        :return:
        """
        visited = {}  # Key: result, Value: index
        ties = []

        for i, val in enumerate(win_count):
            if val in visited:
                cand1 = self.index_to_names[visited[val]]
                cand2 = self.index_to_names[i]
                ties.append((cand1, cand2))
            else:
                visited[val] = i
        return ties

def test():
    a = Schulze('wiki_test.txt')
    res, tot, d, p = a.get_results(3)
    print(res)
    print(tot)
    print(d)
    print(p)