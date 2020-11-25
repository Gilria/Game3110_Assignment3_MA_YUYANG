import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import urllib
import urllib.parse
import urllib.request
import random

playerInQueue=[]


def connectionLoop(sock):
   while True:
      data, addr = sock.recvfrom(1024)
      res=json.loads(data.decode())
      res['WaitTime']="0"
      res['Addr']=addr
      print("Get: "+str(res)+" From: "+str(addr))
      playerInQueue.append(res)
      
def getGameEvent():
   res = urllib.request.urlopen("https://hu4mc3l519.execute-api.us-east-2.amazonaws.com/default/GameEvent").read().decode("utf-8")
   res=json.loads(res)
   if res:
      maxGameId=int(res[0]['GameID'])
      for item in res:
         if int(item['GameID'])>maxGameId:
            maxGameId=int(item['GameID'])
      return maxGameId
      
def updateGameEvent(GameEvent):
   GameID=GameEvent['GameID']
   AverageUserScore=GameEvent['AverageUserScore']
   P1=GameEvent['P1']
   P2=GameEvent['P2']
   P3=GameEvent['P3']
   TimeStamp=GameEvent['TimeStamp']
   Winner=GameEvent['Winner']
   item={
      "GameID":GameID,
      "AverageUserScore":AverageUserScore,
      "P1":P1,
      "P2":P2,
      "P3":P3,
      "TimeStamp":TimeStamp,
      "Winner":Winner
   }
   data = bytes(json.dumps(item),'utf8')
   headers = {"Content-Type": "application/json"}
   req = urllib.request.Request("https://hu4mc3l519.execute-api.us-east-2.amazonaws.com/default/GameEvent", data=data, headers=headers)
   res = urllib.request.urlopen(req)
   print(res.read().decode("utf-8")) 
         
def matchMakingServer(sock):
   playerInGame=[]
   while True:
      for player in playerInQueue:
         player['WaitTime']=int(player['WaitTime'])+1

      if len(playerInQueue)>=3 or playerInGame:
         
         
         if not playerInGame:
            playerInGame.append(playerInQueue[0])
            p1Max=int(playerInGame[0]['UserScore'])+int(playerInGame[0]['WaitTime'])*10
            p1Min=int(playerInGame[0]['UserScore'])-int(playerInGame[0]['WaitTime'])*10
            del playerInQueue[0]

         else:
            for player in playerInQueue:
               p2Max=int(playerInGame[0]['UserScore'])+int(playerInGame[0]['WaitTime'])*10
               p2Min=int(playerInGame[0]['UserScore'])-int(playerInGame[0]['WaitTime'])*10
               if p1Max>=p2Min or p1Min<=p2Max:
                  playerInGame.append(player)
                  playerInQueue.remove(player)
                  if len(playerInGame)==3:
                     simulateMatch(playerInGame[0],playerInGame[1],playerInGame[2],sock)
                     playerInGame=[]
                     break
               
            
      time.sleep(1)

      
def simulateMatch(player1,player2,player3,sock):
   print("GameStart\n"+str(player1)+str(player2)+str(player3))
   temp=random.randint(1,3)
   if temp==1:
      player1['UserWinTurn']=str(int(player1['UserWinTurn'])+1)
      player2['UserLoseTurn']=str(int(player2['UserLoseTurn'])+1)
      player3['UserLoseTurn']=str(int(player3['UserLoseTurn'])+1)
      Winner=player1['UserID']
      player1['UserScore']=str(int(player1['UserScore'])+10)
      player2['UserScore']=str(int(player2['UserScore'])-5)
      player3['UserScore']=str(int(player3['UserScore'])-5)
   elif temp==2:
      player2['UserWinTurn']=str(int(player2['UserWinTurn'])+1)
      player1['UserLoseTurn']=str(int(player1['UserLoseTurn'])+1)
      player3['UserLoseTurn']=str(int(player3['UserLoseTurn'])+1)
      Winner=player2['UserID']
      player1['UserScore']=str(int(player1['UserScore'])-5)
      player2['UserScore']=str(int(player2['UserScore'])+10)
      player3['UserScore']=str(int(player3['UserScore'])-5)
   elif temp==3:
      player3['UserWinTurn']=str(int(player3['UserWinTurn'])+1)
      player2['UserLoseTurn']=str(int(player2['UserLoseTurn'])+1)
      player1['UserLoseTurn']=str(int(player1['UserLoseTurn'])+1)
      Winner=player3['UserID']
      player1['UserScore']=str(int(player1['UserScore'])-5)
      player2['UserScore']=str(int(player2['UserScore'])-5)
      player3['UserScore']=str(int(player3['UserScore'])+10)
   
     
   if int(player1['UserScore'])<0:
      player1['UserScore']='0'
      
   if int(player2['UserScore'])<0:
      player2['UserScore']='0'
      
   if int(player3['UserScore'])<0:
      player3['UserScore']='0'
      
      
      
   player1['Kill']=str(int(player1['Kill'])+random.randint(0,5))
   player1['Death']=str(int(player1['Death'])+random.randint(0,5))
   player1['UserLevel']=str(int(player1['UserLevel'])+1)
   player2['Kill']=str(int(player2['Kill'])+random.randint(0,5))
   player2['Death']=str(int(player2['Death'])+random.randint(0,5))
   player2['UserLevel']=str(int(player2['UserLevel'])+1)
   player3['Kill']=str(int(player3['Kill'])+random.randint(0,5))
   player3['Death']=str(int(player3['Death'])+random.randint(0,5))
   player3['UserLevel']=str(int(player3['UserLevel'])+1)
   
   temp_total=int(player1['UserScore'])+int(player2['UserScore'])+int(player3['UserScore'])
   gameId=getGameEvent()+1
   GameEvent={"GameID":str(gameId),"AverageUserScore":str(temp_total/3),"P1":player1['UserID'],"P2":player2['UserID'],"P3":player3['UserID'],"TimeStamp":str(time.time()),"Winner":Winner}
   updateGameEvent(GameEvent)
    
      
   sock.sendto(json.dumps(player1).encode(), player1['Addr'])
   sock.sendto(json.dumps(player2).encode(), player2['Addr'])
   sock.sendto(json.dumps(player3).encode(), player3['Addr'])

def UpdatePlayer(player):
   UserID=player['UserID']
   UserWinTurn=player['UserWinTurn']
   UserLoseTurn=player['UserLoseTurn']
   UserScore=player['UserScore']
   Kill=player['Kill']
   Death=player['Death']
   UserLevel=player['UserLevel']
   item={
      "UserID":UserID,
      "UserWinTurn":UserWinTurn,
      "UserLoseTurn":UserLoseTurn,
      "UserScore":UserScore,
      "Kill":Kill,
      "Death":Death,
      "UserLevel":UserLevel
   }
   data = bytes(json.dumps(item),'utf8')
   headers = {"Content-Type": "application/json"}
   req = urllib.request.Request("https://hu4mc3l519.execute-api.us-east-2.amazonaws.com/default/GameEvent", data=data, headers=headers)
   res = urllib.request.urlopen(req)
   print(res.read().decode("utf-8")) 
   
   
def main():
   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))
   start_new_thread(connectionLoop, (s,))
   start_new_thread(matchMakingServer, (s,))
   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()