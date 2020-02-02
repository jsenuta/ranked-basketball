from flask import Flask, request, jsonify, render_template 
import requests
import json
import ranking
import math
#import pdb; pdb.set_trace() -  for debugging purposes, uncomment and setup the pdb trace
headers = {
    'Authorization': 'Bearer -',
    'Content-Type': 'application/json'
}

app = Flask(__name__)

@app.route('/')
def hello():
  items = json.loads(requests.get('https://api.airtable.com/v0/appsdIexEprfXeowP/Ranks?maxRecords=10&view=Grid%20view', headers=headers).text)

  lst = []
  

  for item in items['records']:
    lst.append({'rank': item['fields']['Rank'], 'name': item['fields']['Name']})
    # , 'league': item['fields']['League']
    #print(item['fields']['Rank'])
    #print(item['fields']['Name'])

  for x in range(10):
      lst[x]['rank'] = int(lst[x]['rank'])

  i = 0
  for i in range(10):
        place = lst[i]['rank']
        person = lst[i]['name']
        pos = i
        
        while pos > 0 and lst[pos - 1]['rank'] < place:
            # Swap the number down the list
            lst[pos]['rank'] = lst[pos - 1]['rank']
            lst[pos]['name'] = lst[pos - 1]['name']
            pos = pos - 1
        # Break and do the final swap
        lst[pos]['rank'] = place
        lst[pos]['name'] = person


  return render_template('index.html', rankings = lst)

# Adding a method for collecting user input from a button and running ranking.py with the winning team and the margin of victory
@app.route('/', methods=["POST"])
def collect_input():
    # Which team won? a or b
    team = str(request.form.get('winTeam'))
    # What was the margin of victory? (points)
    margin = request.form.get('ptMargin')

    data = '{  "fields": {    "Line": "game",    "Winner": "'+str(team)+'",    "Margin": "'+margin+'"  }}'

    response = requests.patch('https://api.airtable.com/v0/appsNudrABvFaxxaK/Table%201/recDEK6yhvYIDHAqk', headers=headers, data=data)

    if response.status_code == 200: # 200 is success code    
      ranking.main()

    return hello()

if __name__ == '__main__':
  app.run(debug=True, port=5000)