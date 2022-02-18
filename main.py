import os
import json
import requests
from forever import keep_alive
from urllib.request import urlopen
import time
token = os.environ['token']
webhook = os.environ['webhook']
global renew
renew = ""
class endpoints:
    ac = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253Dec684b8c687f479fadea3cb2ad83f5c6%2526responseType%253Dcode"
    token = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    reward = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/ClaimLoginReward?profileId=campaign"

def getToken(authCode: str):
    h = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ="
    }
    d = {
            "grant_type": "authorization_code",
            "code": authCode
    }
    r = requests.post(endpoints.token, headers=h, data=d)
    print(r.text)
    r = json.loads(r.text)
    if "access_token" in r:
        access_token = r["access_token"]
        account_id= r["account_id"]
        print(f"access_token: {access_token}\naccount_id: {account_id}\nexpires_at: {r['expires_at']}")
        return access_token, account_id
    else:
        if "errorCode" in r:
            print(f"[ERROR] {r['errorCode']}")
        else:
            print("[ERROR] Unknown error")
        return False
def getTokenFromLink(url: str):
  # import json

  # store the URL in url as 
  # parameter for urlopen
    
  # store the response of URL
  response = urlopen(url)
    
  # storing the JSON response 
  # from url in data
  data_json = json.loads(response.read())
    
  # print the json response
  print(data_json)
def claimReward(gtResult):

  
  if not gtResult:
      exit()
  else:
      h = {
              "Authorization": f"bearer {gtResult[0]}",
              "Content-Type": "application/json"
      }
      requests.post(endpoints.reward.format(gtResult[1]), headers=h, data="{}")
      print("Should be claimed. idk if you already claimed it")
keep_alive()
claimed = False
claims = 0
claimedAt = 1642464000
reminderAt = 1642464000
gtResult = getToken(token)
while True:
  now = time.time()
  current_time = time.strftime("%H")
  if int(now) - reminderAt > 21600:
    data = {"content": '6 Hourly reminder on ' + time.strftime("%D%H%M")}
    response = requests.post(url=webhook, json=data)
    reminderAt = int(now)
    time.sleep(1000)
  if claimed:
    if int(now) - int(claimedAt) > 86400 or current_time == "00":
      claimed = False
      data = {"content": '24 hours / Shop Reset - Claiming soon \n at ' + time.strftime("%D %H:%M:%S")}
      response = requests.post(url=webhook, json=data)
      time.sleep(200)
    else:
      time.sleep(1000)
  if claimed == False:
    claimReward(gtResult)
    claimedAt = int(time.time())
    data = {"content": 'Succesfully Claimed at ' + time.strftime("%D %H:%M:%S")}
    response = requests.post(url=webhook, json=data)
    claims += 1
    claimed = True
    time.sleep(1000)
  
