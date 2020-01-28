import math 
import json
import requests
#import pdb; pdb.set_trace()
headers = {
    'Authorization': 'Bearer -',
    'Content-Type': 'application/json',
}

#pip install airtable-python-wrapper

# Function to calculate the Probability 
def Probability(rating1, rating2): 
  
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 
  
  
# Function to calculate Elo rating 
# Ra is Team a rating
# Rb is Team b rating
# aWin determines whether Team A wins or Team B (aWin == 1 is a win for team a)  
# margin is the actual point margin
def EloRating(Ra, Rb, aWin, margin): 
   
    StartingRa = Ra
    # To calculate the Winning 
    # Probability of Team B 
    Pb = Probability(Ra, Rb) 
  
    # To calculate the Winning 
    # Probability of Team A 
    Pa = Probability(Rb, Ra) 
  
    #spread finder
    spread = SpreadFinder(Pa, Pb)

    # Case -1 When Team A wins 
    # Updating the Elo Ratings 
    if (aWin == 1): 
      if (Pa > Pb):
        K = 20 + (margin - spread)
      else:
        K = 20 + ((margin + spread) / 2)
      
      Ra = Ra + K * (1 - Pa) 
      Rb = Rb + K * (0 - Pb)
      
  
    # Case -2 When Team B wins 
    # Updating the Elo Ratings 
    else:
      if (Pb > Pa):
        K = 20 + (margin - spread)
      else:
        K = 20 + ((margin + spread) / 2)
      
      Ra = Ra + K * (0 - Pa) 
      Rb = Rb + K * (1 - Pb) 
      
  
    #print("Updated Ratings:-") 
    #print("Ra =", round(Ra, 6)," Rb =", round(Rb, 6)) 
    return (Ra - StartingRa)

# Our code
# Function to calculate average rating
def Average(r1, r2, r3, r4, r5):
  return ((r1 + r2 + r3 + r4 + r5) / 5)
  
# Spread determination
def SpreadFinder(Pa, Pb):
  spread = 0
  if (Pa > Pb):
    P = Pa
  else:
    P = Pb

  if (P  < 54):
    spread = 1
  elif (P < 58):
    spread = 2
  elif (P < 62):
    spread = 3
  elif (P < 66):
    spread = 4
  elif (P < 70):
    spread = 5
  elif (P < 74):
    spread = 6
  elif (P < 78):
    spread = 7
  elif (P < 82):
    spread = 8
  elif (P < 86):
    spread = 9
  elif (P < 90):
    spread = 10
  elif (P < 92):
    spread = 11
  elif (P < 94):
    spread = 12
  elif (P < 96):
    spread = 13
  elif (P < 98):
    spread = 14
  else:
    spread = 15
  return spread

# Ra and Rb are current ELO ratings 

#pull request for r1 - r10 as well as final score margin (difference in final scores)
items = json.loads(requests.get('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks?maxRecords=10&view=Grid%20view', headers=headers).text)

lst = []
  

for item in items['records']:
  lst.append({'rank': item['fields']['Rank'], 'name': item['fields']['Name']})


#print("Enter the ratings of each of the players. Team A: ")
i = 0
r = []
for i in range(len(lst)):
#
  r.append(int(lst[i]['rank']))



winner = input("Who won? Team a or b? ")
if (winner == "a"):
    aWin = 1
else:
    aWin = 0
margin = int(input("What was the margin of Victory? "))

Ra = Average(r[0], r[1], r[2], r[3], r[4])
Rb = Average(r[5], r[6], r[7], r[8], r[9])
diff = round(EloRating(Ra, Rb, aWin, margin))
#print(diff)
#print(Ra)
#print(Rb)

r[0] += diff
r[1] += diff
r[2] += diff
r[3] += diff
r[4] += diff
r[5] -= diff
r[6] -= diff
r[7] -= diff
r[8] -= diff
r[9] -= diff

print("Updated Ratings:")
print("Team A below:     Team B below: ")   
print("P1 =", str(r[0]), " P6 =", str(r[5]))
print("P2 =", str(r[1])," P7 =", str(r[6]))
print("P3 =", str(r[2])," P8 =", str(r[7]))
print("P4 =", str(r[3])," P9 =", str(r[8]))
print("P5 =", str(r[4])," P10 =", str(r[9])) 

data = '{  "fields": {    "Name": "p1",    "Rank": "'+str(int(r[0]))+'",     "League": "Gold"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recP0Ug7CltqlaONR', headers=headers, data=data)

data = '{  "fields": {    "Name": "p2",    "Rank": "'+str(int(r[1]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recZ6QZ7Mp3AjYU83', headers=headers, data=data)

data = '{  "fields": {    "Name": "p3",    "Rank": "'+str(int(r[2]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recWdoxMgJOpL3vXq', headers=headers, data=data)

data = '{  "fields": {    "Name": "p4",    "Rank": "'+str(int(r[3]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recjFJxsdctwgxwir', headers=headers, data=data)

data = '{  "fields": {    "Name": "p5",    "Rank": "'+str(int(r[4]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/rec2e413CzY4xw3vw', headers=headers, data=data)

data = '{  "fields": {    "Name": "p6",    "Rank": "'+str(int(r[5]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/rec7IhazJHbxGpYJl', headers=headers, data=data)

data = '{  "fields": {    "Name": "p7",    "Rank": "'+str(int(r[6]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recbrE7TS6zczLO20', headers=headers, data=data)

data = '{  "fields": {    "Name": "p8",    "Rank": "'+str(int(r[7]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/rec0XUKNGhIJeragY', headers=headers, data=data)

data = '{  "fields": {    "Name": "p9",    "Rank": "'+str(int(r[8]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recdNvUQWkLmgP5Nm', headers=headers, data=data)

data = '{  "fields": {    "Name": "p10",    "Rank": "'+str(int(r[9]))+'",     "League": "Silver"  }}' # how to use a variable instead of a number in this?

response = requests.patch('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks/recaY6psMCOtDincQ', headers=headers, data=data)