__author__ = "JGC"  #Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")


class Tournament(object):

    def __init__(self, name,diff,money_list):
        """
        Constructor for tournament
        :param str name: name of tournament
        :param float diff: difficulty of tournament
        :param List<float> money_list: list of prize money for the tournament
        """
        self.name = name
        self.difficulty = diff
        self.divisions = []
        self.prize_money = []
        self.set_prize_money(money_list)

    def add_division(self,div):
        """
        Adds new division to the tournament
        :param Division div: the division you want to add
        :return: void
        """
        self.divisions.append(div)

    def set_prize_money(self,list):
        """
        Setter for prize money
        :param List<float> list:
        :return: void
        """
        for i in list:
            self.prize_money.append(i)

    def get_prize_money(self, i):
        """
        Gets prize money from list
        :param int i: the index in the list of prize money
        :return:
        """
        return self.prize_money[i]

    def add_prize_money(self,i):
        """
        Adds prize money to list of prize money
        :param float i: the new amount of prize money to add to list
        :return: void
        """
        self.prize_money.append(i)

    def get_prize_money_all(self):
        """
        Gets the list of prize money
        :return: List<float>
        """
        return self.prize_money

    def sort_prize_money(self):
        """
        Sorts the list of prize money
        :return: void
        """
        self.prize_money.sort()

    def get_name(self):
        """
        Getter for name of tournament
        :return str name: name of tournament
        """
        return self.name

    def get_divisions(self):
        """
        Gets all divisions for a tournament
        :return List<Division>: whole list of divisions
        """
        return self.divisions

    def get_division(self,id):
        """
        Gets one division from list
        :param int id: the index of the division
        :return Division: one division from the list
        """
        return self.divisions[id]

    def number_divisions(self):
        """
        Number of divisions
        :return int: number of divs
        """
        return len(self.divisions)

    def get_difficulty(self):
        """
        Gets difficulty of tournament
        :return float: the diff of tournament
        """
        return float(self.difficulty)

    def __str__(self):
        """String representation of tournament"""
        st = self.name +" "+ str(self.difficulty)+"\n      "
        for i in range(len(self.divisions)):
            st += "- "+str(self.divisions[i]) + "\n      "
        return st
