from datetime import datetime
import math
import sqlite3
import pandas as pd
import os
from tkinter import Tk,filedialog
from shutil import copy
import pathlib
#import admin1
#if not admin1.isUserAdmin():
#	admin1.runAsAdmin()

print('________________________________________________')
print('|                                              |')
print('| Aplikasi Convert Data (*.Nex) ke DB3 dan CSV |')
print('|       Developed by: Bayu Merdeka TFN         |')
print('|      contact : merdekabayu06@gmail.com       |')
print('|                                              |')
print('|______________________________________________|')
print('\n')
print('Pilih File Nex...')
print('\n')
root = Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(filetypes = (("Nex files","*.nex"),("all files","*.*")))
print('Input File Nex :')
for file_path in file_paths:
	print(file_path)
print('\n')
print('Pilih Folder Output...')
out_directory = filedialog.askdirectory()
print("Folder Output : ",out_directory)
print('\n')
print('Masukkan Koordinat Stasiun Anda:')
xsta = input("Longitude: ")
ysta = input("Latitude: ")

print('\n')
print('---------------------- Meproses Data ----------------------')

for file_path in file_paths:
	fname=os.path.basename(file_path)
	fname=fname[0:8]
	tgl = datetime.strptime(fname[0:8],'%Y%m%d')
	tgl = str(tgl.strftime('%Y-%m-%d'))
	nex_destfolder= pathlib.Path().absolute()
	dest=str(nex_destfolder)+'\\'+fname+'.nex'
	# copy(file_path, dest)


	os.system("C:\Windows\System32\cmd.exe /c nxutil -extract -i" + " " + fname + " -o " + fname + "temp.csv -f ALL -validate -d")
	#os.remove(fname+'.nex')
	df = pd.read_csv(fname+'temp.csv',header=None)
	index = df.index
	num=list(range(1, len(index)+1))
	df.insert(10, column = 10, value = num)
	df.to_csv(fname+'temp.csv',header=False,index=False)

	file = open(fname+'temp.csv','r')
	baris = file.readlines()
	for i in range(len(baris)):
		baris[i]=baris[i].rstrip("\n").split(",")
	file.close()
	# os.remove(fname+'temp.csv')

	file = open(out_directory+'/'+fname+'.csv','w')
	file.write('id'+','+'epoch_ms'+','+'datetime_utc'+','+'latitude'+','+'longitude'+','+'type'+'\n')
	xsta = float(xsta)
	ysta = float(ysta)
	#xsta = 127.366667
	#ysta = 0.772


	def local_to_utc(tgl,seconds):
		wkt = datetime.utcfromtimestamp(seconds).strftime("%H:%M:%S")
		date_time = tgl + ' ' + wkt
		local = datetime.strptime(date_time[0:19], '%Y-%m-%d %H:%M:%S')
		ts_local = local.timestamp()
		utc = datetime.utcfromtimestamp(ts_local)
		tgl_utc = str(utc.strftime('%Y-%m-%d'))
		wkt_utc = str(utc.strftime('%H:%M:%S'))
		yyyy = tgl[0:4]
		mm = tgl[5:7]
		dd = tgl[8:10]
		hh = datetime.utcfromtimestamp(seconds).strftime("%H")
		MM = datetime.utcfromtimestamp(seconds).strftime("%M")
		ss = datetime.utcfromtimestamp(seconds).strftime("%S")
		epoch = datetime(int(yyyy), int(mm), int(dd), int(hh), int(MM), int(ss)).timestamp()
		epochms = epoch * 1000
		return tgl_utc,wkt_utc,tgl,wkt,epochms,utc

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


	i = 0

	while i < len(baris):
		seconds = float(baris[i][0])
		waktu = local_to_utc(tgl,seconds)
		utctime = waktu[5]
		tglwkt_utc = utctime.strftime('%Y-%m-%d %H.%M.%S')
		dateutc = waktu[0]
		timeutc = waktu[1]
		dateloc = waktu[2]
		timeloc = waktu[3]
		epoch = waktu[4]
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

	conn = sqlite3.connect(out_directory+'/'+fname+'.db3')
	c = conn.cursor()
	c.execute(""" CREATE TABLE IF NOT EXISTS NGXLIGHTNING (id INTEGER PRIMARY KEY, epoch_ms INT(8), datetime_utc TEXT, latitude REAL, longitude REAL, type INT); """)
	read_data = pd.read_csv(out_directory+'/'+fname+'.csv')
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
	print(file_path,"Data Extraction Completed!!")
print("------------------------- SELESAI -------------------------")
print("\n")
print("Cek Data Output (DB3 dan CSV) di : ",out_directory)
print("\n")

os.system("pause")