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

def NewConnection(playerList):
   s0=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s0.sendto(json.dumps(playerList[0]).encode(),("13.58.202.31",12345))
   
   s1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s1.sendto(json.dumps(playerList[1]).encode(),("13.58.202.31",12345))
   
   s2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s2.sendto(json.dumps(playerList[2]).encode(),("13.58.202.31",12345))
   
   s3=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s3.sendto(json.dumps(playerList[3]).encode(),("13.58.202.31",12345))
   
   s4=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s4.sendto(json.dumps(playerList[4]).encode(),("13.58.202.31",12345))
   
   s5=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s5.sendto(json.dumps(playerList[5]).encode(),("13.58.202.31",12345))
   
   s6=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s6.sendto(json.dumps(playerList[6]).encode(),("13.58.202.31",12345))
   
   s7=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s7.sendto(json.dumps(playerList[7]).encode(),("13.58.202.31",12345))
   
   s8=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s8.sendto(json.dumps(playerList[8]).encode(),("13.58.202.31",12345))
   
   s9=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s9.sendto(json.dumps(playerList[9]).encode(),("13.58.202.31",12345))
   
   s10=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s10.sendto(json.dumps(playerList[10]).encode(),("13.58.202.31",12345))
   
   s11=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   s11.sendto(json.dumps(playerList[11]).encode(),("13.58.202.31",12345))
   
   
   # data9 = s9.recv(1024)
   start_new_thread(GetReturnData, (s0,))
   start_new_thread(GetReturnData, (s1,))
   start_new_thread(GetReturnData, (s2,))
   start_new_thread(GetReturnData, (s3,))
   start_new_thread(GetReturnData, (s4,))
   start_new_thread(GetReturnData, (s5,))
   start_new_thread(GetReturnData, (s6,))
   start_new_thread(GetReturnData, (s7,))
   start_new_thread(GetReturnData, (s8,))
   start_new_thread(GetReturnData, (s9,))
   start_new_thread(GetReturnData, (s10,))
   start_new_thread(GetReturnData, (s11,))
   
def GetReturnData(sock):
      data=sock.recv(1024)
      res=json.loads(data.decode())
      print(res)
      UpdatePlayer(res)

def GetPlayerList():
   res = urllib.request.urlopen("https://k4p6ff53ik.execute-api.us-east-2.amazonaws.com/default/Userprofile").read()
   playerList=json.loads(res)
   NewConnection(playerList)
   # print(playerList)
   
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
   req = urllib.request.Request("https://k4p6ff53ik.execute-api.us-east-2.amazonaws.com/default/Userprofile", data=data, headers=headers)
   res = urllib.request.urlopen(req)
   print(res.read().decode("utf-8")) 
   
def main():
   GetPlayerList()
   while True:
      time.sleep(1)
if __name__ == '__main__':
   main()