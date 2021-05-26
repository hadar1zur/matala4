# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:07:43 2021

@author: hadar
"""
def read_file(file:str)->list:
    city_names=dict()
    count=0
    for line in file:
        city_names[count]=line
        count=count+1
    return city_names

def Printing_destinations (place:str):
    api_key = "AIzaSyByDv_GG-aGecFS53DVLMZcI-V-gX-Dr8g"
    url1 ='https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
    location ='תל אביב'
    dictionary_dests=dict()
    Distances=list()
    list_farthest =list()
    distance_integger = re.compile(r"([^km]+)")
    for dest in place:
        try:
            response = requests.get(url1 + "origins=" + location + "&destinations=" + dest + "&key=" + api_key)
            distance = response.json()["rows"][0]["elements"][0]["distance"]["text"]
            Distances.append(distance)
            seconds = response.json()["rows"][0]["elements"][0]["duration"]["value"]
            hours= int(int(seconds)/3600)
            minutes= int((int(seconds)-(hours*3600))/60)
            time= str(hours) + ' hours ' +  str(minutes) + " minutes"
            url2 ='https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (dest, api_key)
            response = requests.get(url2)
            latitude = response.json()['results'][0]['geometry']['location']['lat']
            longitude = response.json()['results'][0]['geometry']['location']['lng']   
            dictionary_dests[dest] = {'distance': distance,'duration': time,'latitude': latitude,'longitude':longitude} 
        except:
            print('Error! No place found' , dest)
            continue
    for dest in dictionary_dests:  
        print(dest+': \n', dictionary_dests[dest], '\n******************************** \n' )
        
    for i in Distances:
        sum_km = distance_integger.search(i)
        if sum_km:
            list_farthest.append(float(i[sum_km.span()[0]:sum_km.span()[1]].replace(' ','').replace(',',''))) 
            
    return list_farthest

def Farthest_destinations (list_farthest:list):
    farthest=[0,0,0]
    city=['','','']
    for i in range(len(list_farthest)):
        if list_farthest[i]>farthest[0]:
            farthest[2]=farthest[1]
            farthest[1]=farthest[0]
            farthest[0]=list_farthest[i]
            city[2]=city[1]
            city[1]=city[0]
            city[0]=city_names[i]
        elif list_farthest[i]>farthest[1]:
            farthest[2]=farthest[1]
            farthest[1]=list_farthest[i]
            city[2]=city[1]
            city[1]=city_names[i]
        elif list_farthest[i]>farthest[2]:
            farthest[2]=list_farthest[i]
            city[2]=city_names[i]

    print('\n' ,'שלושת הערים הכי רחוקות מתל-אביב:', '\n 1.', city[0].strip() ,' - ', farthest[0], 'KM''\n 2.', city[1].strip(),' - ', farthest[1], 'KM''\n 3.', city[2].strip(),' - ', farthest[2], 'KM')
    
    
import requests
import json
import re 
place=str()
with open('dests.txt','r',encoding = 'utf8') as file:
    place = file.read().splitlines()    
file=open('dests.txt','r', encoding='utf-8') #open file
city_names=read_file(file)
Farthest_destinations(Printing_destinations(place)) 
  
