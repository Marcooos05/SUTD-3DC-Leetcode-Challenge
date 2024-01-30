from datetime import datetime
import time

import requests
from bs4 import BeautifulSoup

file_name = 'filterednames.txt' # file name to contain the filtered list 
baseurl = "https://leetcode.com/" # website data that the code will scrape from

# Function will filter the names of all participants based on a file
def filterall(fileofnames):
    output = []
    namelist = []
    #Accessing database of names that are participating in the challenge
    names = open(fileofnames, "r")

    #Writing a new file that is names after the date and contain the participant details of that day
    file = open(file_name, 'w')

    for username in names:
        if username not in namelist:
            namelist.append(username)
            username = username.strip()
            url = baseurl + username + '/'
            #print(url)

            req = requests.get(url)
            soup = BeautifulSoup(req.content, "html.parser")
            res = soup.get_text()

            if 'Page Not Found' in res:
                # invalid leetcode username
                output.append(username + " invalid leetcode username")
            else:
                # valid leetcode username

                # Only register valid leetcode usernames with 'SUTD' in their education
                if 'SUTD' in res:
                    file.write(username + '\n')
                    output.append(username + " successfully added")
                else:
                    output.append(username + " 'SUTD' in education not found")
        else: 
            output.append(username + " already participating")

        time.sleep(2)
    #print('Done')
    names.close()
    file.close()
    return output

# Function will include all valid usernames into the list of participants
# Multiple names can be added, names to be separated by only white spaces
def filter(names):
    output = []
    # opening the filteredname file
    namefile = open(file_name, 'r+')

    # opening the data of participants file
    month = datetime.now().strftime("%m-%y")
    datefile = '01-' + month + '.txt'
    userdetails = open(datefile, "a")

    # creating a list of already recorded names
    namelist = []
    for name in namefile:
        namelist.append(name.strip()) # remove \n at the back of each username
    
    # cleaning the list of names to be added
    addnames = set(names)
    if '' in addnames:
        addnames.remove('')
    #print(namelist)

    # for every additional only add unique names that are valid
    for newname in list(addnames):
        if newname not in namelist:
            url = baseurl + newname + '/'
            req = requests.get(url)
            soup = BeautifulSoup(req.content, "html.parser")
            res = soup.get_text()
            if 'Page Not Found' in res:
                # invalid leetcode username
                output.append(newname + " invalid leetcode username")
            else:
                # valid leetcode username

                # Only register valid leetcode usernames with 'SUTD' in their education
                if 'SUTD' in res:
                    namefile.write(newname + '\n')
                    output.append(newname + " successfully added🏅🏅")

                    # Add their scores into the reference database based on the date they joined
                    Easyscore, _, Mediumscore, _, Hardscore, _ = retrieve_leetscore(res)
                    line = newname + ' | ' + Easyscore + ' | ' + Mediumscore + ' | ' + Hardscore + '\n'
                    userdetails.write(line)

                else:
                    output.append(newname + " 'SUTD' in education not found")
        else:
            output.append(newname + " already participating")

        time.sleep(2)
    namefile.close()
    userdetails.close()

    return output

# Function uses webscrapping to obtain the number of solutions for input user
def retrieve_leetscore(res):

    indexEasy = res.index("Easy")
    indexMedium = res.index("Medium")
    indexHard = res.index("Hard")
    indexBadge = res.index("Badge")

    Easy = res[indexEasy:indexMedium]
    Medium = res[indexMedium:indexHard]
    Hard = res[indexHard:indexBadge]

    indexEasySlash = Easy.index("/")
    indexMediumSlash = Medium.index("/")
    indexHardSlash = Hard.index("/")

    Easyscore = Easy[4:indexEasySlash]
    Easytext = f'Easy Solved: {Easyscore}'
    Mediumscore = Medium[6:indexMediumSlash]
    Mediumtext = f'Medium Solved: {Mediumscore}'
    Hardscore = Hard[4:indexHardSlash]
    Hardtext = f'Hard Solved: {Hardscore}'
    
    return Easyscore, Easytext, Mediumscore, Mediumtext, Hardscore, Hardtext

# Function to store the solutions of all users before the challenge month
def referencescore():
    # Getting the date to be used as the file name for future reference
    date = datetime.now().strftime("%d-%m-%y")
    #print(date)

    if date[:2] != '01':
        return 'Update Failed\nIt is not the first day of the month'

    file_name = date + '.txt'
    #print(file_name)

    #Accessing database of names that are participating in the challenge
    names = open("filterednames.txt", "r")

    #Writing a new file that is names after the date and contain the participant details of that day
    file = open(file_name, 'w')

    for username in names:
        username = username.strip()
        url = baseurl + username + '/'
        #print(url)

        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        res = soup.get_text()
        Easyscore, _, Mediumscore, _, Hardscore, _ = retrieve_leetscore(res)
        line = username + ' | ' + Easyscore + ' | ' + Mediumscore + ' | ' + Hardscore + '\n'
    
        file.write(line)
        time.sleep(3)
    #print('Done')
    file.close()
    return "Update Successful\nNew file for the month has been created"

# Function will tally the score for all participants of the challenge
def todaytally(referencefile):
    output = {}
    #Accessing database of user details
    userdetails = open(referencefile, "r")

    baseurl = "https://leetcode.com/"

    for line in userdetails:
        line = line.strip()
        lst = line.split(' | ')

        username = lst[0]
        Easy = lst[1]
        Medium = lst[2]
        Hard = lst[3]

        username = username.strip()
        url = baseurl + username + '/'
        #print(url)

        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        res = soup.get_text()
        Easyscore, _, Mediumscore, _, Hardscore, _ = retrieve_leetscore(res)
        score = 1*(int(Easyscore) - int(Easy)) + 3*(int(Mediumscore) - int(Medium)) + 6*(int(Hardscore) - int(Hard))
        output[username] = score
    
        time.sleep(3)
    userdetails.close()
    return output

# Function returns the leaderboard for the challenge
def scoreboard(referencefile):
    output = "🔥🔥Today's Leetcode Leaderboard!!🔥🔥\n"
    score_dict = {} # store names of participants as values to their score for sorting

    name_dict = todaytally(referencefile)
    print('Tally done')

    for name in name_dict:
        score = name_dict[name]
        if score not in score_dict:
            score_dict[score] = [name]
        else:
            score_dict[score].append(name)

    sorted_dict = sorted(score_dict, reverse = True)

    for score in sorted_dict:
        for name in score_dict[score]:
            line = name + " | Score: " + str(score) + '\n'
            output = output + line
    return output


# Function return stats for one individual user for the month
def mytally(name, referencefile):
    output = "Username is not registered for SUTD Leetcode Challenge"
    #Accessing database of user details
    userdetails = open(referencefile, "r")

    baseurl = "https://leetcode.com/"

    for line in userdetails:
        line = line.strip()
        lst = line.split(' | ')

        username = lst[0]
        if username != name:
            continue

        Easy = lst[1]
        Medium = lst[2]
        Hard = lst[3]

        username = username.strip()
        url = baseurl + username + '/'
        #print(url)

        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        res = soup.get_text()
        Easyscore, _, Mediumscore, _, Hardscore, _ = retrieve_leetscore(res)
        Easy_solved = int(Easyscore) - int(Easy)
        Med_solved = int(Mediumscore) - int(Medium)
        Hard_solved = int(Hardscore) - int(Hard)
        score = 1*(Easy_solved) + 3*(Med_solved) + 6*(Hard_solved)
        output = f"{username} stats for this month🚀🚀\nEasy Solved : {Easy_solved}\nMedium Solved: {Med_solved}\nHard Solved: {Hard_solved}\nScore: {score}"
    
    userdetails.close()
    return output

def finalscore():
    # Getting the month and year to reference to the text file with data
    month = datetime.now().strftime("%m")
    newyear = datetime.now().strftime("%y")
    if month == '01':
        previousmonth = '12'
        year = str(int(newyear) - 1)
    else:
        previousmonth = f"{int(month) - 1:02}"
        year = newyear
    
    #opening both files for comparison
    newmonthfile = open(f"01-{month}-{newyear}.txt", "r")
    previousmonthfile = open(f"01-{previousmonth}-{year}.txt", "r")

    user_dict = {}
    user_score = {}

    for line in previousmonthfile:
        line = line.strip()
        lst = line.split(' | ')

        username = lst[0]
        Easy = lst[1]
        Medium = lst[2]
        Hard = lst[3]
        user_dict[username] = [Easy, Medium, Hard]

    for line in newmonthfile:
        line = line.strip()
        lst = line.split(' | ')

        username = lst[0]
        if username not in user_dict:
            continue
        Easy = lst[1]
        Medium = lst[2]
        Hard = lst[3]
        list = user_dict[username]
        user_score[username] = int(Easy) - int(list[0]) + 3*(int(Medium) - int(list[1])) + 6*(int(Hard) - int(list[2]))

    score_dict = {}
    for name in user_score:
        score = user_score[name]
        if score not in score_dict:
            score_dict[score] = [name]
        else:
            score_dict[score].append(name)

    sorted_dict = sorted(score_dict, reverse = True)

    output = "🔥🔥FINAL Leetcode Leaderboard!!🔥🔥\n"
    for score in sorted_dict:
        for name in score_dict[score]:
            line = name + " | Score: " + str(score) + '\n'
            output = output + line
    return output