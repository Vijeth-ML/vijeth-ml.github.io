# Name : VIJETH BALASUBRAMANIAM
# Student ID : 201664207

import copy
def generatePreferences(values):
    
    agent_dict = {}
    temp_dict = {}
    for row in range(1, values.max_row + 1):
        key = row
        if key not in agent_dict.keys():
            agent_dict[key] = []
        for col in range(1, values.max_column + 1):
            agent_dict[key].append(values.cell(row, col).value)

    # the values are sorted to store the preferences of the agents
    for key, values in agent_dict.items():
        temp_dict = {index + 1 : val for index, val in enumerate(values)}
        agent_dict[key] = sorted(temp_dict, key=temp_dict.get)[::-1]
    return agent_dict

#An agent is selected, and the winner is the alternative that this agent ranks first
def dictatorship(preferenceProfile, agent):
    try:
        if agent in preferenceProfile.keys():
            winner = preferenceProfile[agent][0]
            return winner
        else:
            raise ValueError      
    except ValueError:
        print("Not an agent")

#testscoringRule function
#function contains error-handling code for the case when the length of the scoring vector is not m.
#In that case, the message "Incorrect input" will be printed and the function will return False
def scoringRule(preferences, scoreVector, tieBreak): 
    
    score_dict = {}
    winner = list()
    alternate_len = len(preferences[1])
    try:
        if len(scoreVector) != alternate_len:
            raise ValueError
        for key in preferences.keys():
            temp_dict = dict(zip(preferences[key], sorted(scoreVector, reverse=True)))
            for key, values in temp_dict.items(): 
                score_dict[key] = score_dict.get(key, 0) + values
    except ValueError:
        print("Incorrect input")

    winner = get_max_val(score_dict)
    return tie_break(preferences, tieBreak, winner)

#plurality
#winner is the alternative that appears the most times in the first position of the agents preference orderings
def plurality(preferences, tieBreak):
    
    temp_dict = {}
    votes = {}
    winner = list()
    for key, values in preferences.items():
        temp_dict[key] = values[0]
    for values in temp_dict.values():
        if values in votes.keys():
            votes[values] += 1
        else:
            votes[values] = 1

    winner = get_max_val(votes)
    return tie_break(preferences, tieBreak, winner)

#plurality
# Every agent assigns 0 points to the alternative that they rank in the last place of their preference orderings, and 1 point to every other alternative.
# The winner is the alternative with the most number of points
def veto(preferences, tieBreak):
    
    temp_dict = {}
    winner = list()
    for key, values in preferences.items():
        for element in values:
            if element not in temp_dict:
                temp_dict[key] = 0
    for values in preferences.values():
        for item in values[:-1]:
            temp_dict[item] += 1

    winner = get_max_val(temp_dict)
    return tie_break(preferences, tieBreak, winner)

#borda
# Every agent assigns a score of 0 to the their least-preferred alternative (the one at the bottom of the preference ranking), a score of 1 to the second least-preferred alternative, ... , and a score of m-1 to their favourite alternative.
# In other words, the alternative ranked at position j receives a score of m-j. The winner is the alternative with the highest score
def borda(preferences, tieBreak):
    
    temp_dict = {}
    winner = list()
    alternate_len = len(preferences[1])
    for key, values in preferences.items():
        for element in values:
            if element not in temp_dict:
                temp_dict[key] = 0
    for values in preferences.values():
        for item in values[:-1]:
            temp_dict[item] += alternate_len - (values.index(item) + 1)

    winner = get_max_val(temp_dict)
    return tie_break(preferences, tieBreak, winner)

#harmonic
#Every agent assigns a score of 1/m to the their least-preferred alternative (the one at the bottom of the preference ranking), a score of 1/(m-1) to the second least-preferred alternative, ... , and a score of 1 to their favourite alternative.
#In other words, the alternative ranked at position j receives a score of 1/j
def harmonic(preferences, tieBreak):

    temp_dict = {}
    winner = list()
    alternate_len = len(preferences[1])
    for key, values in preferences.items():
        for element in values:
            if element not in temp_dict:
                temp_dict[key] = 0
    for values in preferences.values():
        for item in values:
            temp_dict[item] += 1/(alternate_len - (alternate_len - (values.index(item) + 1)))

    winner = get_max_val(temp_dict)
    return tie_break(preferences, tieBreak, winner)

#STV
#The voting rule works in rounds. In each round, the alternatives that appear the least frequently in the first position of agents' rankings are removed, and the process is repeated.
#When the final set of alternatives is removed (one or possibly more), then this last set is the set of possible winners
def STV(preferences, tieBreak):
    
    temp_dict = copy.deepcopy(preferences)
    while True:
        frequency = dict.fromkeys(temp_dict[1], 0)
        for values in  temp_dict.values():
            frequency[values[0]] += 1

        
        least = list()
        min_value = min(frequency.values())
        for key, values in frequency.items():
            if values == min_value:
                least.append(key)
        
        if len(least) == len(temp_dict[1]):
            return tie_break(preferences, tieBreak, least)

        
        else:
            for item in least:
                frequency.pop(item, None)
            for values in temp_dict.values():
                for item in least:
                    values.remove(item)

#rangeVoting function
# input a worksheet corresponding to an xlxs file and it should return the alternative that has the maximun sum of valuations and uses tie breaking option to distinguish between possible winners
def rangeVoting(values, tieBreak):
    
    agent_dict = {}
    total = {}
    winner = list()
    for col in range(1, values.max_column + 1):
        total = 0
        key = col
        if key not in agent_dict.keys():
            agent_dict[key] = []
        for row in range(1, values.max_row + 1):
            total += values.cell(row, col).value
            agent_dict[key] = total

    winner = get_max_val(agent_dict)
    return tie_break(generatePreferences(values), tieBreak, winner)
    
#get max value function and among the possible winning alternatives, it selects the one with the highest number
def get_max_val(dictionary):
    if not dictionary:
        return []
    
    winner_list = list()
    max_val = max(dictionary.items(), key=lambda x: x[1])
    for key, values in dictionary.items():
        if values == max_val[1]:
            winner_list.append(key)
    return winner_list

#tie break function
#it  will consider the following three tie-breaking rules and assume that the alternatives are represented by integers
def tie_break(preferences, tieBreak, winner):
    if not winner:
        return None

    if tieBreak == 'max':
        return max(winner)
    elif tieBreak == 'min':
        return min(winner)
    try:
        if tieBreak in preferences.keys():
            for values in preferences[tieBreak]:
                if values in winner:
                    return values
        else:
            raise ValueError
    except ValueError:
        print("Incorrect input")

print()