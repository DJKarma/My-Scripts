# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:56:40 2019

@author: P10461328
"""
#!pip install tkcalendar

import tweepy
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import Button
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog

from tkcalendar import Calendar, DateEntry
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
    


#---------------------------------------------------------------------------------------------------#

root = Tk()

def new_winF(): # new window definition
    newwin = Toplevel(root)
    display = Label(newwin, text="Humm, see a new window !")
    display.pack()    

button1 =Button(root, text ="open new window", command =sentCat) #command linked
button1.pack()

root.mainloop()

#---------------------------------------------------------------------------------------------------#

filenametax=''
exportpathname="export"
userId = ''
pwd = ''
dateUntil = ''
searchStr = ''
flag = ''
fileNameSave = ''
dateFilterStart = ''
dateFilterEnd = ''

root=tk.Tk()
#root.geometry("200x200")
root.title("Twitter Download")
root.geometry("800x400")
lbl = Label(root, text="Enter the details as mentioned below")
#lbl.grid(column=5, row=10)
    
def on_change(e):
    print(e.widget.get())

def setUserId(e):
    global userId
    userId = e.widget.get()

def setPwd(e):
    global pwd
    pwd = e.widget.get()

def setDateFilStart(e):
    global dateFilterStart
    dateFilterStart = e.widget.get()
    
def setDateFilEnd(e):
    global dateFilterEnd
    dateFilterEnd = e.widget.get()

def setDateUntil(e):
    global dateUntil
    dateUntil = e.widget.get()
    
def setSearch(e):
    global searchStr
    searchStr = e.widget.get()
    
def setFileName(e):
    global fileNameSave
    fileNameSave = e.widget.get()
    
L1 = Label(root, text="User Id/Pxxxxxx")
L1.pack(side = LEFT)
L1.place(x = 5, y = 50)
u = tk.Entry(root, bd =5)
u.pack()
u.place(x = 150, y = 50)
# Calling on_change when you press the return key
u.bind("<Key>", setUserId)  
u.bind('<Enter>', setUserId)
u.bind('<Leave>', setUserId) 


L2 = Label(root, text="Password")
L2.pack(side = LEFT)
L2.place(x = 5, y = 80)
v = tk.Entry(root, bd =5,show = "*")
v.pack()
v.place(x = 150, y = 80)
# Calling on_change when you press the return key
v.bind("<Key>", setPwd)  
v.bind('<Enter>', setPwd) 
v.bind('<Leave>', setPwd) 

L3 = Label(root, text = "Date Until")
L3.pack(side = LEFT)
L3.place(x = 5, y = 110)
cal = DateEntry(root, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2019)
cal.pack(padx=10, pady=10)
cal.place(x = 150, y = 110)
#cal.bind("<Key>", setDateUntil) 
cal.bind("<Enter>", setDateUntil) 
cal.bind("<Leave>", setDateUntil) 


L4 = Label(root, text = "Date Start Filter")
L4.pack(side = LEFT)
L4.place(x = 5, y = 140)
cal2 = DateEntry(root, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2019)
cal2.pack(padx=10, pady=10)
cal2.place(x = 150, y = 140)
#cal2.bind("<Key>", setDateFil) 
cal2.bind("<Enter>", setDateFilStart) 
cal2.bind("<Leave>", setDateFilStart) 

L7 = Label(root, text = "Date End Filter")
L7.pack(side = LEFT)
L7.place(x = 300, y = 140)
cal3 = DateEntry(root, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2019)
cal3.pack(padx=10, pady=10)
cal3.place(x = 450, y = 140)
#cal2.bind("<Key>", setDateFil) 
cal3.bind("<Enter>", setDateFilEnd) 
cal3.bind("<Leave>", setDateFilEnd) 


L5 = Label(root, text = "Enter the search string")
L5.pack(side = LEFT)
L5.place(x = 5, y = 170)
w = tk.Entry(root, bd = 5)
w.pack()
w.place(x = 150, y = 170)
w.bind("<Key>", setSearch) 
w.bind("<Enter>", setSearch)
w.bind("<Leave>", setSearch) 

L6 = Label(root, text = "File name to be saved")
L6.pack(side = LEFT)
L6.place(x = 5, y = 200)
x = tk.Entry(root, bd = 5)
x.pack()
x.place(x = 150, y = 200)
x.bind("<Key>", setFileName) 
x.bind("<Enter>", setFileName)
x.bind("<Leave>", setFileName) 

def twittertokenpath():
        global filenametax
        filenametax = askopenfilename()
        labl = Label(root, text=""+filenametax)
        labl.place(x=150,y=230)

def close_window():
         #print(filenamemaindata)
         global flag
         if filenametax and userId and pwd and dateUntil and searchStr and fileNameSave and not exportpathname:
             messagebox.showinfo('Hey! ',"Export path not selected , will be defaulted to export/")
             flag = 'T'
             root.destroy()
         elif not userId:
             messagebox.showinfo('Hey! ',"Please enter User Id (Pxxxxxx)"+userId)
         elif not pwd:
             messagebox.showinfo('Hey! ',"Please enter Password"+pwd)
         elif not dateUntil:
             messagebox.showinfo('Hey! ',"Please enter dateUntil"+dateUntil)
         elif not searchStr:
             messagebox.showinfo('Hey! ',"Please enter search string"+searchStr)
         elif not fileNameSave:
             messagebox.showinfo('Hey! ',"Please enter search string"+fileNameSave)
         elif not filenametax:
             messagebox.showinfo('Hey! ',"Please select Tokens File. To Quit please close window"+filenametax)
         elif filenametax and exportpathname:
             flag = 'T'
             root.destroy()

def exportpath():
  global exportpathname
  exportpathname = filedialog.askdirectory()
  labl = Label(root, text=""+exportpathname)
  labl.place(x=150,y=260)
  if exportpathname:
      exportpathname=exportpathname
  else:
      messagebox.showinfo('Export Directory ',"No Export path selected,files will be exported to export folder")
      exportpathname='export' 


            
B1 = Button(root, text = "TwitterTokens", command = twittertokenpath)
B1.place(x = 5,y = 230)
B2 = Button(root, text = "Export", command = exportpath)
B2.place(x = 5,y = 260)
B3 = Button(root, text = "Done", command = close_window)
B3.place(x = 5,y = 290)
    
root.mainloop()


#---------------------------------------------------------------------------------------------------#

if flag == 'T': #Execute the below code only if the flag is T i.e only if all the details are entered by the user.
    #token = pd.read_excel(r"C:\Karthik\K Bckp\ADHOC\O2\token.xlsx")
    """token = pd.read_excel(filenametax)
    
    dictTk = token.set_index('key').T.to_dict('str')
    for i in dictTk.keys():
        if "access_token" == i:
            access_token = dictTk[i]["value"]
        elif 'access_token_secret' == i:
            access_token_secret = dictTk[i]["value"]
        elif 'consumer_key' == i:
            consumer_key = dictTk[i]["value"]
        elif 'consumer_secret' == i:
            consumer_secret = dictTk[i]["value"]"""
            
            
    col_names = ["UserName", "Location", "Reach", "Tweet", "TwittedAt"]
    TweetDataFrame = pd.DataFrame(columns = col_names)
    count = 1
    
    #dateFilter =   datetime.datetime(2019, 9, 12, 0, 0, 0)  #Date Filter to filter only specific days data.
    dateUnt = datetime.strptime(dateUntil, '%m/%d/%y').strftime('%Y-%m-%d')
    
    access_token = "554514706-5qkKQbieLo85azCsdwQ9j7wGAWOHf6Zq8MxIzJzB"
    access_token_secret = "i7vHclaCqIiK5JM7VPvLH2h5J0cs2zOyqsvJtXUzgZ2ZJ"
    consumer_key = "DPTeL16d7nT3OdShwlP5f9yQc"
    consumer_secret = "4dMn5z0HA4WYPJiF3uODfLu6si3dH6akOF1htOjwqCxu8nJOMy"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Creating the API object while passing in auth information
    proxy_url = "http://"+ userId + ":" + pwd + "@ci-proxy:80"
    api = tweepy.API(auth,timeout=300,proxy = proxy_url,wait_on_rate_limit=True)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    #result = api.geo_search(query="United Kingdom", granularity="country") #Added by Karthik to get only the values for UK
    #place_id = result[0].id #Added by Karthik to get only the values for UK
    
    #newTweets  = api.search(q='@O2 iPhone & place:%s' % place_id,count=50,lang = "en",tweet_mode='extended',wait_on_rate_limit=True,until = '2019-09-12')
    search = searchStr 
    newTweets  = api.search(q= search,count=120,lang = "en",tweet_mode='extended',wait_on_rate_limit=True,until = dateUnt)
    
    alltweets.extend(newTweets)
    oldest = alltweets[-1].id - 1
    
    
    while len(newTweets) > 0:
        # print("getting tweets before %s" % (oldest))
        newTweets = api.search(q=search ,count=20,lang = "en",tweet_mode='extended',wait_on_rate_limit=True,until = dateUnt,max_id=oldest)
        #newTweets  = api.search(q='#iPhone 11 & @O2 & place:%s' % place_id,count=10,lang = "en",tweet_mode='extended',max_id=oldest,wait_on_rate_limit=True)
        alltweets.extend(newTweets)
        oldest = alltweets[-1].id - 1
        
    dateFiltStart = datetime.strptime(dateFilterStart, '%m/%d/%y')
    dateFiltEnd = datetime.strptime(dateFilterEnd, '%m/%d/%y')
    # foreach through all tweets pulled
    for tweet in alltweets:
       # printing the text stored inside the tweet object
       # print(tweet.user.screen_name,"Tweeted:",tweet.text)
        #print("The user Name:", tweet.user.name, "and Location is:",tweet.user.location, "Reach of:", tweet.user.followers_count,"Tweeted:",tweet.full_text,"Twitted At:", tweet.created_at)
        if (tweet.created_at).date() >= dateFiltStart.date() and (tweet.created_at).date() <= dateFiltEnd.date():
            TweetDataFrame.at[count,"UserName"] = tweet.user.name
            TweetDataFrame.at[count,"Location"] = tweet.user.location
            TweetDataFrame.at[count,"Reach"] = tweet.user.followers_count
            TweetDataFrame.at[count,"Tweet"] = tweet.full_text
            TweetDataFrame.at[count,"TwittedAt"] = tweet.created_at
            count = count+1;
        
    #print(TweetDataFrame)
    TweetDataFrame.to_excel(exportpathname+"\\"+fileNameSave+".xlsx")

