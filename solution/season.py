__author__ = "JGC"  #Author: JGC

if __name__ == "__main__": #File is opened directly
    print("This file has been called incorrectly")


class Season(object):
    """This is the class for season"""

    def __init__(self, date, ranking_list):
        """
        Constructor for season
        :param str date: The name of the season
        :param List<int> ranking_list: list of ranking points
        """
        self.year = date
        self.tournaments = []
        self.participants = []
        self.ranking_points = []
        self.ranking_points = ranking_list

    def add_tournament(self, tourn):
        """
        Add individual tournament
        :param Tournament tourn: the tournament you want to add
        :return: void
        """
        self.tournaments.append(tourn)

    def get_tournaments(self):
        """
        Get all tournaments
        :return List<Tournament>: all tournaments
        """
        return self.tournaments

    def get_tournament(self,i):
        """
        Get one tournament
        :param int i: the index of the tournament required
        :return Tournament: one tournament
        """
        return self.tournaments[i]

    def number_tournaments(self):
        """
        Number of tournaments in the season
        :return int: number of tournaments
        """
        return len(self.get_tournaments())

    def get_name(self):
        """
        Gets the name of the season
        :return str: name of the season (year)
        """
        return str(self.year)

    def add_participants(self, parts):
        """
        Add players to the season
        :param List<Player> parts: list of players (whole division)
        :return: void
        """
        self.participants.append(parts)

    def get_all_participants(self):
        """
        Gets all of the players
        :return List<List<Player>>: a list containing lists of players per division
        """
        return self.participants

    def get_participants(self, id):
        """
        Gets a division of players
        :param int id: the index of the division
        :return List<Player>: list of players in a division
        """
        return self.participants[id]

    def get_participant(self, id, id2):
        """
        Gets one player
        :param int id: the index of the division
        :param int id2: index of player
        :return Player: Individual player
        """
        return self.participants[id][id2]

    def get_ranking_points(self):
        """
        Gets ranking points
        :return List<int>: list of ranking points
        """
        return self.ranking_points

    def get_ranking_point(self, i):
        """
        Gets ranking points at a specific index
        :param int i: the index of the ranking points
        :return int: the ranking points at the index
        """
        return self.ranking_points[i]

    def add_ranking_points(self, i):
        """
        Adds ranking points to the list of ranking points
        :param int i: the ranking points to add to the list
        :return: void
        """
        self.ranking_points.append(i)

    def sort_ranking_points(self):
        """
        Sorts the ranking points list
        :return: void
        """
        self.ranking_points.sort()

    def __str__(self):
        """String representation of season"""
        st = "Season: "+str(self.year)+ " " + "\n"
        for i in range(len(self.tournaments)):
            st += "   • "+str(self.tournaments[i])+"\n"
        return st
