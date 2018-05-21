__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")

class Match(object):

    def __init__(self,p_a,s_a,p_b,s_b):
        """
        Constructor for match
        :param str p_a: player A name
        :param int s_a: player A score
        :param str p_b: player B name
        :param int s_b: player B score
        """
        self.score = []
        self.participants = []
        self.participants.append(p_a)
        self.score.append(s_a)
        self.participants.append(p_b)
        self.score.append(s_b)

    def get_score(self,id):
        """
        Gets the score of one of players
        :param int id: the index of the player
        :return int: score of the player
        """
        return self.score[id]

    def get_participant(self,id):
        """
        Gets the name of the player
        :param int id: the index of the player
        :return:
        """
        return self.participants[id]

    def __str__(self):
        """String representation of the player"""
        st = ""
        for i in self.score:
            st = st.join(str(self.score[i])).join(" ")
            st = st.join(str(self.participants[i])).join(" ")
