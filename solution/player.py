__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")


class Player(object):

    def __init__(self, name, type):
        """
        Constructor for player
        :param str name: player's name
        :param str type: player's type
        """
        self.name = name
        self.type = type
        self.ranking_total = 0
        self.ranking = []
        self.highest_round = []
        self.prize_money = []
        self.prize_money_total = 0
        self.number_tournaments = 0

    def get_name(self):
        """
        Getter for name
        :return str name: player name
        """
        return self.name

    def get_type(self):
        """
        Getter for type
        :return str type: player type
        """
        return self.type

    def set_number_tournaments(self,num):
        """
        Setter for number of tournaments
        :param int num:
        :return: void
        """
        self.number_tournaments = num
        for i in range(0,num):
            self.highest_round.append(1)
            self.ranking.append(0)
            self.prize_money.append(0)


    def get_highest_round(self,tourn):
        """
        Getter for highest round
        :param int tourn: tournament num
        :return int high_round: highest round in tournament
        """
        return self.highest_round[tourn]

    def add_highest_round(self,tourn):
        """
        Increments the highest round for a tournament
        :param int tourn: tournament num
        :return: void
        """
        self.highest_round[tourn] += 1

    def reset(self):
        """
        Resets the player's stats
        :return: void
        """
        for i in range(0,self.number_tournaments):
            self.highest_round[i] = 1
            self.ranking[i] = 0
            self.prize_money[i] = 0

    def get_rank(self):
        """
        Gets total number of ranking points across tournaments
        :return float total: The total number of ranking points
        """
        total = 0
        for i in range(0,len(self.ranking)):
            total += self.ranking[i]
        self.ranking_total = total
        return total

    def set_rank(self,rank,tourn):
        """
        Sets the rank for a player in a tournament
        :param float rank: the ranking points for the tournament
        :param int tourn: number of the tournament
        :return: void
        """
        self.ranking[tourn] = round(rank,2)

    def set_prize_money(self,prize,tourn):
        """
        Sets the prize money for a tournament
        :param float prize: the amount of money
        :param int tourn: the tournament number
        :return: void
        """
        self.prize_money[tourn] = prize

    def get_prize_money(self):
        """
        Gets total prize money across tournaments
        :return float total: the total prize money
        """
        total = 0
        for i in range(0, len(self.prize_money)):
            total += self.prize_money[i]
        self.prize_money_total = total
        return total

    def __str__(self):
        """String representation"""
        return str(self.name)
