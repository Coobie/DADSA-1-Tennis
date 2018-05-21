__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")


class Division(object):

    def __init__(self, name, best, pl):
        """
        Constructor for division
        :param str name: name of the division
        :param int best: the number of sets to win a match
        :param str pl: player type
        """
        self.name = name
        self.matches = []
        self.best_of = best
        self.player_type = pl

    def add_match(self, mat):
        """
        Adds match to the division
        :param Match mat: the match you want to add
        :return: void
        """
        self.matches.append(mat)

    def get_name(self):
        """
        Gets the name of the division
        :return str: name of the division
        """
        return self.name

    def get_player_type(self):
        """
        Gets the player type
        :return str: the type of the players
        """
        return self.player_type

    def get_matches(self):
        """
        Gets all of the matches in the division
        :return List<Match>: whole list of matches
        """
        return self.matches

    def get_best_of(self):
        """
        Gets the the number of sets to win a match
        :return int : number of sets to win
        """
        return self.best_of

    def __str__(self):
        """String representation of division"""
        st = self.name + " which is best of "+ str(self.get_best_of())
        return st
