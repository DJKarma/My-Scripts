#this file needs to edit embed.py in sitepackages of anaconda due to issue in python 3.7
#the file is ideally located in something like this  C:\ProgramData\Anaconda3\Lib\site-packages\ipywidgets
#replace script escape to return script_escape_re.sub(lambda match: r"\u003c" + match.group(1), s)
#thank DJ later.
#i did not have access to C so created embedd with extra d and i import that file instead of original embed.py


import pandas as pd
import numpy as np
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import gmplot
from gmplot import *
import PIL
from PIL import Image,ImageTk
import tkinter as tk
from tkinter import *
from tkinter import Button
from tkinter.filedialog import askopenfilename
from tkinter import INSERT
import os
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
import gmaps
from ipywidgets.embedd import embed_minimal_html
import os
global df
global count
df=pd.DataFrame()
import warnings
warnings.filterwarnings("ignore")
gmaps.configure(api_key='AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78')


def locationcorrection():

    geolocator = Nominatim(user_agent='d')
    df['Location']=df['Location'].astype(str)
    x=0
    ctr=0
    #REMOVES UNWANTED SPECIAL CHARACTERS

    df['Full Location']=np.nan
    df['Latitude']=np.nan
    df['Longitude']=np.nan

    text=df['Location'].values.T.tolist() #converting the same column to lists
    text= [k.lower() for k in text]
    leng = df.shape[0]
    fleng= df.shape[0]

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='black')
    bar = Progressbar(root, length=500, style='black.Horizontal.TProgressbar')

    bar.grid(column=5, row=2)

    def do_geocode(ctr,leng):
        geolocator = Nominatim(user_agent='d')

        try:
            for x in range(leng):

                dj=text[ctr]
                df['Full Location'].iloc[ctr]=geolocator.geocode(dj,timeout=2,language='en')

                if df['Full Location'].iloc[ctr] is not None:
                    df['Latitude'].iloc[ctr]=df['Full Location'].iloc[ctr].latitude
                    df['Longitude'].iloc[ctr]=df['Full Location'].iloc[ctr].longitude
                else:
                    df['Latitude'].iloc[ctr]='None'
                    df['Longitude'].iloc[ctr]='None'
                ctr=ctr+1
                txt.config(state=NORMAL)
                txt.insert(INSERT,"\nProgress -> ")
                txt.insert(INSERT,ctr)
                txt.insert(INSERT,"|")
                txt.insert(INSERT,fleng)
                bar['value'] = np.round((ctr/fleng)*(100))
                root.update()
                txt.see(tk.END)
                txt.config(state=DISABLED)


        except GeocoderTimedOut:
            leng=leng-x
            x=0
            return do_geocode(ctr,leng)

    do_geocode(ctr,leng)
    txt.config(state=NORMAL)
    txt.insert(INSERT,"\n Done! ")
    txt.insert(INSERT,"\n File with Locations and Co-ordinates exported as filname - LocupdatedData.xlsx ")
    txt.insert(INSERT,"\n Please select the same file and then click on Scatter or Heatmap to generate one. ")
    txt.see(tk.END)
    txt.config(state=DISABLED)
    df.to_excel("LocupdatedData.xlsx", index=False)


#plotting######################################################################


def scatterplots():
    try:
        df['Full Location'].replace('', np.nan, inplace=True)
        df['Location'].replace('', np.nan, inplace=True)
        df.dropna(subset=['Location','Full Location'], inplace=True)
    except:
        print("...")
    lat = df['Latitude'].values
    lon = df['Longitude'].values
    """
    gmap=gmplot.GoogleMapPlotter(54.02,-0.94,6.5)
    gmap.apikey = "AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78"
    gmap.scatter(lat,lon,'#3B0B39', size=140, marker=False)
    gmap.draw( "scatterplotmap.html" )
    """
    gmaps.configure(api_key='AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78')

    figure_layout = { 'width': '1600px', 'height': '900px', 'border': '1px solid black', 'padding': '1px' }

    fig = gmaps.figure(layout=figure_layout,map_type='TERRAIN')
    symbol_layer = gmaps.symbol_layer(df[['Latitude', 'Longitude']], fill_color='rgba(0, 150, 0, 0.4)', stroke_color='rgba(0, 150, 0, 0.4)', scale=2)
    fig.add_layer(symbol_layer)
    embed_minimal_html('scatterplotmap.html', views=[fig])
    txt.config(state=NORMAL)
    txt.insert(INSERT,"\n Done! ")
    txt.insert(INSERT,"\n Maps exported as interactive HTML - scatterplotmap.html ")

    txt.config(state=DISABLED)
    #gmaps.figure(map_type='TERRAIN')

def heatmaps():
    try:
        df['Location'].replace('', np.nan, inplace=True)
        df.dropna(subset=['Location','Full Location'], inplace=True)
    except:
        print("...")
    lat = df['Latitude'].values
    lon = df['Longitude'].values

    """
    gmap=gmplot.GoogleMapPlotter(54.02,-0.94,6.5)
    gmap.apikey = "AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78"
    gmap.heatmap(lat,lon,threshold=30, radius=10, gradient=None, opacity=0.4, dissipating=True)


    gmap.draw( "heatmap.html" )
    """
    txt.config(state=NORMAL)
    txt.insert(INSERT,"\n Done! ")
    txt.insert(INSERT,"\n Maps exported as interactive HTML - heatmap.html ")

    txt.config(state=DISABLED)

    #GMAPS CODE TO OUTPUT
    gmaps.configure(api_key='AIzaSyAhzINZ3b25CuR5ldJOdouaQLRE8_lUD78')

    figure_layout = { 'width': '1600px', 'height': '900px', 'border': '1px solid black', 'padding': '1px' }

    fig = gmaps.figure(layout=figure_layout,map_type='TERRAIN')
    heatmap_layer = gmaps.heatmap_layer(df[['Latitude', 'Longitude']], max_intensity=8,point_radius=5.0)
    fig.add_layer(heatmap_layer)
    embed_minimal_html('heatmap.html', views=[fig])



###############################################################################


filepath=''

root=tk.Tk()
root.geometry("920x580")
root.title("Location Data Analysis and Plotting - DJ")
lbl = Label(root, text="Follow the rules(Excel files only)--\n1)Rename the column you want to correct locations for to - 'Location' to avoid errors.\n2)Select the file, click on Location Correct to correct locations and get latitude and Longitude.\n 3)Click on types of plot you want to output, dont forget to re-select the file, the file should have 'Latitude' and 'Longitude' as columns to avoid error.\n4)Done to quit")
lbl.grid(column=5, row=10)

txt = scrolledtext.ScrolledText(root,width=90,height=24)
txt.grid(column=5,row=20,padx=140,pady=90)


def filepaths():
    global filepath
    global df
    global count
    txt.config(state=DISABLED)

    txt.config(state=NORMAL)
    filepath = askopenfilename()
    df=pd.read_excel(filepath)
    #df=pd.read_excel("loc.xlsx")
    try:
        df['Location']=df['Location'].str.replace("[^., a-zA-Z0-9 \n\.]", '')
        df['Location'].replace('', np.nan, inplace=True)
    except:
        print("...")

    count=df.shape[0]
    txt.tag_config('warning', background="grey", foreground="black")
    txt.insert(INSERT,"Currently selected -> ",'warning')
    txt.insert(INSERT,filepath,'warning')
    txt.insert(INSERT,"\nLocations with specials characters and invalid removed")
    txt.insert(INSERT,"\nFile imported with locations - ")
    txt.insert(INSERT,count)
    txt.insert(INSERT,"\n")

    txt.config(state=DISABLED)

    B2.config(state = NORMAL)
    B3.config(state = NORMAL)
    B4.config(state = NORMAL)
    B5.config(state = NORMAL)


def close_window():
          MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application?',icon = 'warning')
          if MsgBox == 'yes':
              root.destroy()


B1 = Button(root, text = "File", command = filepaths)
B1.place(x = 25,y = 160)

B2 = Button(root, text = "Location Correction", command = locationcorrection)
B2.place(x = 15,y = 260)

B3 = Button(root, text = "Generate Scatter Plot", command = scatterplots)
B3.place(x = 15,y = 360)
B4 = Button(root, text = "Generate Heatmap", command = heatmaps)
B4.place(x = 15,y = 460)
B5 = Button(root, text = "DONE", command = close_window)
B5.place(x = 15,y = 530)
B2.config(state = DISABLED)
B3.config(state = DISABLED)
B4.config(state = DISABLED)


root.mainloop()