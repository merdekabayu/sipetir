from datetime import datetime,timedelta
import math
import sqlite3
import pandas as pd
import os
from shutil import copy
import pathlib
import subprocess


def local_to_utc(tgl,seconds,utc):
    wkt = datetime.utcfromtimestamp(seconds).strftime("%H:%M:%S")
    date_time = tgl + ' ' + wkt
    local = datetime.strptime(date_time[0:19], '%Y-%m-%d %H:%M:%S')
    utc = local - timedelta(hours=utc)
    
    epoch = utc.timestamp()
    epochms = epoch * 1000
    return epochms,utc

def coordinate(ysta,xsta,bearing,d):
    R = 6378.137                   #Radius of the Earth
    brng = math.radians(bearing) #convert degrees to radians
    d = d                  #convert nautical miles to km
    xsta = math.radians(xsta)
    ysta = math.radians(ysta)
    lat = math.asin( math.sin(ysta)*math.cos(d/R) + math.cos(ysta)*math.sin(d/R)*math.cos(brng))
    lon = xsta + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(ysta),math.cos(d/R)-math.sin(ysta)*math.sin(lat))
    lat = math.degrees(lat)
    lon = math.degrees(lon)
    return lat,lon



def nex2db(xsta,ysta,utc,filenex):
    nexname = filenex.split('/')[2].split('.')[0] #20230708
    filetmp = nexname+'temp.csv'
    subprocess.call('sshpass -p "Ternate97432" scp -P 2223 -r '+filenex+' personal@36.91.152.130:/D:/nxutil/',shell=True)
    os.system('sshpass -p "Ternate97432" ssh -p2223 personal@36.91.152.130 nxutil -extract -i D:/nxutil/'+nexname+' -o D:/nxutil/'+filetmp+' -f ALL -validate -d')
    subprocess.call('sshpass -p "Ternate97432" scp -P 2223 -r personal@36.91.152.130:/D:/nxutil/'+filetmp+' fungsi/nxutil/',shell=True)
    # os.system("C:\Windows\System32\cmd.exe /c nxutil -extract -i" + " " + fname + " -o " + fname + "temp.csv -f ALL -validate -d")

    fname = 'fungsi/nxutil/'+filetmp
    df = pd.read_csv(fname,header=None)
    index = df.index
    num=list(range(1, len(index)+1))
    df.insert(10, column = 10, value = num)
    df.to_csv(fname,header=False,index=False)
    
    file = open(fname,'r')
    baris = file.readlines()
    for i in range(len(baris)):
        baris[i]=baris[i].rstrip("\n").split(",")
    file.close()

    
    xsta = float(xsta)
    ysta = float(ysta)
    dt = datetime.strptime(nexname,'%Y%m%d')
    tgl = dt.strftime('%Y-%m-%d')
    utc = float(utc)

    file = open('fungsi/nxutil/'+nexname+'.csv','w')
    file.write('id'+','+'epoch_ms'+','+'datetime_utc'+','+'latitude'+','+'longitude'+','+'type'+'\n')

    i = 0
    while i < len(baris):
        seconds = float(baris[i][0])
        waktu = local_to_utc(tgl,seconds,utc)
        utctime = waktu[1]
        tglwkt_utc = utctime.strftime('%Y-%m-%d %H.%M.%S')
        epoch = waktu[0]
        brg = baris[i][1]
        dist = baris[i][3]
        tipe = baris[i][4]
        pole = baris[i][5]
        no = baris[i][10]
        id=no
        if tipe == "0" and pole == "0":
            type = 0
            type_ = "CG+"
        elif tipe == "0" and pole == "1":
            type = 1
            type_ = "CG-"
        else:
            type = 2
            type_ = "IC"

        coord=coordinate(ysta,xsta,float(brg),float(dist))
        lat = str(coord[0])
        long = str(coord[1])
        file.write(str(id)+','+str(epoch)+','+str(tglwkt_utc)+'.000'+','+lat+','+long+','+str(type)+'\n')
        i = i+1
    file.close()

    conn = sqlite3.connect('fungsi/nxutil/'+nexname+'.db3')
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS NGXLIGHTNING (id INTEGER PRIMARY KEY, epoch_ms INT(8), datetime_utc TEXT, latitude REAL, longitude REAL, type INT); """)
    read_data = pd.read_csv('fungsi/nxutil/'+nexname+'.csv')
    df = pd.DataFrame(read_data, columns=['id', 'epoch_ms', 'datetime_utc', 'latitude', 'longitude', 'type'])

    for row in df.itertuples():
        id = str(row.id)
        epoch = int(row.epoch_ms)
        datetime_utc = str(row.datetime_utc)
        latitude = float(row.latitude)
        longitude = float(row.longitude)
        type = int(row.type)
        values = (id, epoch, datetime_utc, latitude, longitude, type)

        sql = ''' INSERT OR IGNORE INTO NGXLIGHTNING(id,epoch_ms,datetime_utc,latitude,longitude,type)
                    VALUES(?,?,?,?,?,?) '''
        c.execute(sql, values)
    conn.commit()

    fout = ['fungsi/nxutil/'+nexname+'.db3','fungsi/nxutil/'+nexname+'.csv']

    return fout

