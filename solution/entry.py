__author__ = "JGC"  # Author: JGC

from season import Season
from tournament import Tournament
from division import Division
from player import Player
from match import Match
import extra as ex
import os.path
import csv
import math

# All files and folders
my_path = os.path.abspath(os.path.dirname(__file__)) # Relative path of files
round_paths = ""
data_paths = ""
output_path = ""
start = True

with open("CONFIG.txt") as f:  # Read config file
    for line in f:
        if "DATA" in line:  # Get data path from config
            address_folder = line.split('"')
            data_paths = address_folder[1]
        elif "ROUND" in line:  # Get round path from config
            address_folder = line.split('"')
            round_paths = address_folder[1]
        elif "OUTPUT" in line:  # Get output path from config
            address_folder = line.split('"')
            output_path = address_folder[1]

if (round_paths == "" and data_paths == "" and output_path == ""):
    start = False


def read_info():
    """Reads in all of the files apart from matches and returns: void"""
    matchFileTour = os.path.join(my_path, ".."+data_paths+"TOURNAMENT INFO.csv")
    DivInfo = os.path.join(my_path, ".."+data_paths+"DIVISION INFO.csv")
    ranking_points = os.path.join(my_path, ".."+data_paths+"RANKING POINTS.csv")

    ranking_list = []
    with open(ranking_points, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            temp = int(row["Tournament Ranking Points"])
            if temp is not None:
                ranking_list.sort()
                if (ex.binary_search(ranking_list, temp) == None):
                    ranking_list.append(temp)
            ranking_list.sort()
    # Find out the number of columns in the tournament info csv
    number_columns = 0
    with open(matchFileTour, 'r') as f1:
        csvlines = csv.reader(f1, delimiter=',')
        for lineNum, line in enumerate(csvlines):
            if lineNum == 0:
                number_columns = (len(line))
                break
            break

    # Find all of the seasons in the file and load them into seasons
    season_list = []
    with open(matchFileTour, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            temp = row["Season"]
            if temp is not None:
                if(ex.binary_search(season_list,temp) == None):
                    season_list.append(temp)
    for i in season_list:
        seasons.append(Season(i,ranking_list))

    # Load in all tournaments to their respective seasons
    # Also finds which places get prize money
    for i in seasons:
        with open(matchFileTour, 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                if(row["Season"] == i.get_name()):
                    temp = []
                    row_name = "Place "
                    number_places = (number_columns - 3)
                    for x in range(0,number_places):
                        temp.append(float(row[row_name+str(x+1)].replace(',','')))
                    new_list = list(set(temp)) # Find unique elements in list

                    i.add_tournament(Tournament(row["Tournament"],row["Difficulty"],new_list))

    # Load in divisions for each tournament
    for x in seasons:
        for j in x.get_tournaments():
            with open(DivInfo, 'r') as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    if (row["Season"] == x.get_name()) and (row["Tournament"] == j.get_name()):
                        j.add_division(Division(row["Division"],row["Best Of"],row["Players"]))

    # Add players to seasons
    list_all_divisions = []
    for x in seasons:
        for j in x.get_tournaments():
            for k in j.get_divisions():
                if list_all_divisions is not None: # Find all of the divisions in the season
                    list_all_divisions.sort()
                    if(ex.binary_search(list_all_divisions,k.get_player_type()) == None):
                        list_all_divisions.append(str(k.get_player_type()))
        for i in list_all_divisions:
            with open(os.path.join(my_path, ".."+data_paths+"PLAYERS "+i+".csv"), 'r') as csvFile:
                reader = csv.DictReader(csvFile)
                temp = []
                for row in reader:
                    player = Player(row["Player"],i)
                    player.set_number_tournaments(x.number_tournaments())
                    temp.append(player)
            x.add_participants(temp)


def read_match(file,folder):
    """
    Reads match and loads it in and returns: void
    :param str file: Address of the file (expected "season tournament ROUND n division.csv")
    :param str folder: The folder the rounds are in
    :return: void
    """
    parts_file_path = file.split(folder).pop().split(".csv").pop(0).split(" ")
    del parts_file_path[2]
    season = ex.binary_search_class(seasons,parts_file_path[0])
    tourn = ex.binary_search_class(seasons[season].get_tournaments(),parts_file_path[1])
    div = ex.binary_search_class(seasons[season].get_tournament(tourn).get_divisions(),parts_file_path[3])
    with open(file, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        d = seasons[season].get_tournament(tourn).get_division(div)
        line_number = 0
        for row in reader:
            player_a = row["Player A"]
            a_score = row["Score Player A"]
            player_b = row["Player B"]
            b_score = row["Score Player B"]
            if a_score.isdigit() and b_score.isdigit():
                if ex.valid_match(d.get_best_of(),int(a_score),int(b_score)):  # Check match is valid
                    d.add_match(Match(player_a,a_score,player_b,b_score))
                else:
                    print("\nTHE FOLLOWING MATCH IS INVALID: \n"+player_a,a_score,player_b,b_score)
                    print("In file: "+file)
                    print("Line: "+str(line_number))
                    print("PLEASE CHANGE THIS LINE")
            else:
                print("\nTHE FOLLOWING MATCH IS INVALID: \n" + player_a, a_score, player_b, b_score)
                print("File: " + file)
                print("Line: " + str(line_number))
                print("PLEASE CHANGE THIS LINE")
            line_number +=1


def reset_players():
    """Simple function to reset all of the ranking and prize money for each player and returns: void"""
    for s in seasons:
        for p1 in s.get_all_participants():
            for p in p1:
                p.reset()


def set_highest_round_for_winners():
    """Sets the highest round for each player in tournaments and returns: void"""
    reset_players()  # Required
    for s in seasons:
        for t in range(0,s.number_tournaments()):
            for d in range(0,s.get_tournament(t).number_divisions()):
                for m in s.get_tournament(t).get_division(d).get_matches():
                    # Find players in list of players
                    p1 = ex.binary_search_class(s.get_participants(d), m.get_participant(0))
                    pp1 = s.get_participant(d, p1)
                    p2 = ex.binary_search_class(s.get_participants(d), m.get_participant(1))
                    pp2 = s.get_participant(d, p2)
                    if pp1.get_highest_round(t) == pp2.get_highest_round(t):  # Check the players have the same highest round
                        if m.get_score(0) > m.get_score(1):  # First player is the winner
                            s.get_participant(d,p1).add_highest_round(t)  # Increment the highest round for the winner
                        elif m.get_score(0) < m.get_score(1):  # Second player is the winner
                            s.get_participant(d,p2).add_highest_round(t)  # Increment the highest round for the winner
                    else:  # The highest round of the players is not the same
                        print("\nA match is not valid in season",s.get_name(),"tournament",s.get_tournament(t).get_name(),"division",s.get_tournament(t).get_division(d).get_name())
                        print("This is due to the player(s) not having progressed to the round")
                        print("This is most likely in round",str(pp1.get_highest_round(t)),"or",str(pp2.get_highest_round(t)))
                        print("Although could be in a higher round")


def calculate_ranking():
    """Calculates ranking points for players based off highest round and returns: void"""
    for s in seasons:
        winner_round = []
        for pd in range(0,len(s.get_all_participants())):  # Loops number of divisions of players
            winner_round.append(math.log2(len(s.get_participants(pd)))+1)  # Calculate the round one above the final (winner of tourn)
            while winner_round[pd] > len(s.get_ranking_points()):  # Adds zeros to the front of ranking points list
                s.add_ranking_points(0)
            s.sort_ranking_points()  # Sorts the ranking points list
            for p in range(0,len(s.get_participants(pd))):  # Loop players in div
                for t in range(0,s.number_tournaments()):  # loop tournaments
                    highest_round = s.get_participant(pd, p).get_highest_round(t)
                    base = s.get_ranking_point(highest_round - 1)  # Base number of ranking points
                    if base is not 0:  # Avoids redundant times by zero
                        rank = (s.get_tournament(t).get_difficulty() * base)
                    else:
                        rank = 0
                    s.get_participant(pd, p).set_rank(rank, t)


def calculate_prize_money():
    """Calculates prize money for players based off highest round and returns: void"""
    for s in seasons:
        winner_round = []
        for t in range(0, s.number_tournaments()):
            for pd in range(0, len(s.get_all_participants())):  # Loops number of divisions of players
                winner_round.append(math.log2(len(s.get_participants(pd))) + 1) # Calculate the round one above the final (winner of tourn)
                while winner_round[pd] > len(s.get_tournament(t).get_prize_money_all()): # Adds zeros to the front of prize money list
                    s.get_tournament(t).add_prize_money(0.0)
                s.get_tournament(t).sort_prize_money()  # Sorts the ranking points so that the zeros are at the front of the list
                for p in range(0, len(s.get_participants(pd))):  # Loop players in the division
                    highest_round = s.get_participant(pd,p).get_highest_round(t)
                    prize = float(s.get_tournament(t).get_prize_money(highest_round - 1))
                    s.get_participant(pd, p).set_prize_money(prize, t)  # Assign prize money for the tournament


def calculate():
    """Calls all the functions required to calculate everything and returns: void"""
    set_highest_round_for_winners()
    calculate_ranking()
    calculate_prize_money()


def read_files(folder):
    """
    Reads in all round files in a folder into read_match
    :param str folder: The folder the round data is in
    :return: void
    """
    files = os.listdir(os.path.join(my_path, ".."+folder))
    res = filter(lambda x: "ROUND" in x and x.endswith(".csv"), files)
    for i in res:
        read_match(os.path.join(my_path, ".."+folder+i),folder)


def output_ranking():
    """Print players in order of rank to the console and returns: void"""
    for x in seasons:
        list_all_divisions = []
        for j in x.get_tournaments():
            for k in j.get_divisions():
                if list_all_divisions is not None:  # Find all of the divisions in the season
                    list_all_divisions.sort()
                    if (ex.binary_search(list_all_divisions, k.get_player_type()) == None):
                        list_all_divisions.append(str(k.get_player_type()))
        counter = 0
        print("══" * 20)
        for d in list_all_divisions:
            temp = []
            for w in x.get_participants(counter):
                temp.append(w)
            temp.sort(key=lambda obj: obj.get_rank(), reverse=True)
            count = 1
            print("Current Ranking for "+d)
            for k in temp:
                print("%02d" % (count) + ".", k.get_name(), k.get_rank(), "£" + "{:,}".format(k.get_prize_money()))
                count += 1
            print("══" * 20)
            counter+=1


def output_prize_money():
    """Print players in order of prize money to the console and returns: void"""
    for x in seasons:
        list_all_divisions = []
        for j in x.get_tournaments():
            for k in j.get_divisions():
                if list_all_divisions is not None:  # Find all of the divisions in the season
                    list_all_divisions.sort()
                    if (ex.binary_search(list_all_divisions, k.get_player_type()) == None):
                        list_all_divisions.append(str(k.get_player_type()))
        counter = 0
        print("══" * 20)
        for d in list_all_divisions:
            temp = []
            for w in x.get_participants(counter):
                temp.append(w)
            temp.sort(key=lambda obj: obj.get_prize_money(), reverse=True)
            count = 1
            print("Current prize money for "+d)
            for k in temp:
                print("%02d" % (count) + ".", k.get_name(), "£" + "{:,}".format(k.get_prize_money()),k.get_rank())
                count += 1
            print("══" * 20)
            counter+=1


def write_ranking_to_file(folder):
    """
    Outputs files containing ranking per division
    :param str folder: The folder you want to write the ranking to
    :return: void
    """
    for x in seasons:
        list_all_divisions = []
        for j in x.get_tournaments():
            for k in j.get_divisions():
                if list_all_divisions is not None:  # Find all of the divisions in the season
                    list_all_divisions.sort()
                    if (ex.binary_search(list_all_divisions, k.get_player_type()) == None):
                        list_all_divisions.append(str(k.get_player_type()))
        counter = 0
        for d in list_all_divisions:
            file_name = x.get_name() +" CURRENT RANKING "+ d
            field_names = ["RANK","PLAYER NAME","RANKING POINTS","TOTAL PRIZE MONEY"]
            temp = []
            for w in x.get_participants(counter):
                temp.append(w)
            temp.sort(key=lambda obj: obj.get_rank(), reverse=True)
            with open(os.path.join(my_path,(".."+folder+file_name+'.csv')), 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()

                c = 1
                for t in temp:
                    writer.writerow({'RANK': c, 'PLAYER NAME': t.get_name(), 'RANKING POINTS': t.get_rank(), 'TOTAL PRIZE MONEY': "{:,}".format(t.get_prize_money())})
                    c+=1
            counter+=1


# -- START -- #
seasons = []  # Important list - Holds all classes
if start is True:
    read_info()
    options = ["QUIT","OUTPUT INFO ABOUT TENNIS","LOAD ALL MATCHES","ENTER MATCH (ALL STORED MATCHES WILL BE LOADED)","CALCUALTE RANKING","PRINT OUT CURRENT RANKING","PRINT OUT PRIZE MONEY","WRITE RANKING TO FILE"]
    # Actual user input related
    quit = False
    while quit is not True:
        print("████████████")
        print("<--| MAIN MENU |-->")
        print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print("Options:")
        i = 0
        while i < len(options):
            print(str(i)+".",options[i])
            i += 1

        user = input("Enter command: ")
        if user == "quit" or user == "q" or user == "0":
            quit = True
        elif user == "1": # output info
            print("\n----INFORMATION----")
            for i in seasons:
                print(str(i))
        elif user == "2": # load matches
            read_files(round_paths)
            print("\nLoaded Matches")
        elif user == "3": # Enter match
            match_quit = False
            while match_quit is not True:
                print("\nSelect Season:")
                print("=="*10)
                s_count = 0
                for s in seasons:
                    print (str(s_count)+".",s.get_name())
                    s_count+=1
                print(str(s_count) + ".", "RETURN TO MAIN MENU")
                print("==" * 10)
                user_season = input("Enter number for season: ")
                if user_season.isdigit() and int(user_season) < len(seasons):
                    user_season = int(user_season)
                    t_count = 0
                    for t in seasons[user_season].get_tournaments():
                        print(str(t_count)+".",t.get_name())
                        t_count+=1
                    user_tourn = input("Enter number for tournament: ")
                    if user_tourn.isdigit() and int(user_tourn) < len(seasons[user_season].get_tournaments()):
                        user_tourn = int(user_tourn)
                        d_count = 0
                        for d in seasons[user_season].get_tournament(user_tourn).get_divisions():
                            print (str(d_count)+".",d.get_name())
                            d_count+=1
                        user_div = input("Enter number for division: ")
                        if user_div.isdigit() and int(user_div) < len(seasons[user_season].get_tournament(user_tourn).get_divisions()):
                            user_div = int(user_div)
                            user_round = input("Enter the round number: ")
                            if user_round.isdigit() and int(user_round) <= math.log2(len(seasons[user_season].get_participants(user_div))) and int(user_round) >= 1:
                                user_round = int(user_round)
                                # Where the user enters details for the match
                                print("PlayerA ScoreA PlayerB ScoreB")
                                match_input = input("Enter the match: ")
                                match_input = match_input.split(" ") # Split the input into list that should be 4 length
                                if len(match_input) == 4 and match_input[1].isdigit() and match_input[3].isdigit():
                                    p_a = match_input[0]
                                    a_s = int(match_input[1])
                                    p_b = match_input[2]
                                    b_s = int(match_input[3])
                                    best = seasons[user_season].get_tournament(user_tourn).get_division(user_div).get_best_of()
                                    if ex.valid_match(best,a_s,b_s) == True:
                                        # Match Score is valid
                                        pp_a = ex.binary_search_class(s.get_participants(user_div),p_a)
                                        pp_b = ex.binary_search_class(s.get_participants(user_div),p_b)
                                        # Check players entered are valid
                                        if pp_a is not None and pp_b is not None:
                                            if seasons[user_season].get_tournament(user_tourn).get_division(user_div).get_matches() == []:
                                                read_files(round_paths)
                                            set_highest_round_for_winners()
                                            highest_a = seasons[user_season].get_participant(user_div,pp_a).get_highest_round(user_tourn)
                                            highest_b = seasons[user_season].get_participant(user_div,pp_b).get_highest_round(user_tourn)
                                            if highest_a == highest_b and highest_a == user_round:
                                                # Add match
                                                seasons[user_season].get_tournament(user_tourn).get_division(user_div).add_match(Match(p_a,a_s,p_b,b_s))
                                                # Store match - write to file
                                                file = os.path.join(my_path, ".." + round_paths + seasons[user_season].get_name() + " " + seasons[user_season].get_tournament(user_tourn).get_name() + " ROUND " + str(user_round) + " " + seasons[user_season].get_tournament(user_tourn).get_division(user_div).get_name() + ".csv")
                                                file_exists = (os.path.isfile(file))
                                                with open(file, 'a', newline='') as csvfile:
                                                    fieldnames = ['Player A','Score Player A','Player B','Score Player B']
                                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                                    if file_exists is False:
                                                        writer.writeheader()
                                                    writer.writerow({'Player A': p_a, 'Score Player A': a_s, 'Player B': p_b, 'Score Player B': b_s})

                                                print("Match has been added")

                                            else:
                                                print("Invalid Match: Players not allowed together in this round")
                                        else:
                                            print("Invalid Match: Could not find players")
                                    else:
                                        print("Invalid Match: Scores are not valid")
                                else:
                                    print("Invalid Match: Incorrect number of arguments given")
                            else:
                                print("Invalid Round")
                        else:
                            print("Invalid Division")
                    else:
                        print("Invalid Tournament")
                elif user_season.isdigit() and int(user_season) == len(seasons):
                    match_quit = True
                else:
                    print("Invalid Season")

        elif user == "4":
            calculate()
            print("\nRanking has been calculated")
        elif user == "5":
            output_ranking()
        elif user == "6":
            output_prize_money()
        elif user == "7":
            "\nFiles have been outputed"
            write_ranking_to_file(output_path)

    print("Program has closed")
else:
    print("A PROBLEM HAS OCCURRED")
    print("SOMETHING IS WRONG IN THE CONFIG FILE")
