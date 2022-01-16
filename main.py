import os
import json
import requests
import schedule, random
from forever import keep_alive
from urllib.request import urlopen
import time
token = os.environ['token']
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
def claimReward(token: str):
  print('Shop updated, starting random countdown to make it look legit')
  time.sleep(random.randint(0,3600))
  gtResult = getToken(token)
  if not gtResult:
      exit()
  else:
      h = {
              "Authorization": f"bearer {gtResult[0]}",
              "Content-Type": "application/json"
      }
      r = requests.post(endpoints.reward.format(gtResult[1]), headers=h, data="{}")
      print(r.text)
      print("Should be claimed. idk if you already claimed it")
keep_alive()
schedule.every().day.at("00:00:00").do(claimReward,token)
while True:
  schedule.run_pending()

  

