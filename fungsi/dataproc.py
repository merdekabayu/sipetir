from subprocess import run
from flask import Flask, render_template, request, redirect,send_file
from flask_mysqldb import MySQL
from datetime import datetime, timedelta, date
from dateutil import tz
import sqlite3, os
from .idw import saveidw
import pandas as pd
import haversine as hs
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/upload/"

f = open('fungsi/coord.cfg', 'r')
baris = f.readlines()
f.close()
coord = baris[0].split(' ')
xmin = coord[0]
xmax = coord[1]
ymin = coord[2]
ymax = coord[3]

def pelayanan_sortir(custloc,tgl1,tgl2,dtime1,dtime2,utc,batas,rad,filedb):
    
    if len(filedb[0].filename) < 1:
        if tgl1 == tgl2:
            tgl = tgl1
            dt = datetime.strptime(tgl, '%d-%m-%Y')
            f_thn = tgl[6:10]
            f_bln = str(dt.strftime("%-m"))
            filename = str(dt.strftime("%Y%m%d") + '.db3')
            dir = 'fungsi/data/DB3/' + f_thn + '/' + f_bln
            databases = [dir + '/' + filename]
        else:
            dt1 = datetime.strptime(tgl1, '%d-%m-%Y')
            dt2 = datetime.strptime(tgl2, '%d-%m-%Y')
            databases = fromdbsta(dt1,dt2)
    else:
        databases = []
        for files in filedb:
            fname = secure_filename(files.filename)
            print(files)
            files.save(app.config['UPLOAD_FOLDER'] + fname)
            databases.append(app.config['UPLOAD_FOLDER'] + fname)

            
    print(databases)
    fileout = 'fungsi/gmt/sambaran_pelayanan.dat'
    
    readdb3(databases,fileout,batas)

    df=pd.read_csv(fileout,delim_whitespace=True, header=None)

    dts = []
    poss = []
    for dfcolumn in df.itertuples():
        x = float(dfcolumn[1])
        y = float(dfcolumn[2])
        type = dfcolumn[5]
        loc = (y,x)
        jarak = hs.haversine(loc, custloc)
        dtutc = dfcolumn[3]+' '+dfcolumn[4][:2]+':'+dfcolumn[4][3:5]+':'+dfcolumn[4][6:8]
        dtutc = datetime.strptime(dtutc, '%Y-%m-%d %H:%M:%S')
        time = dtutc+timedelta(hours=utc)
        # print(jarak)
        # print(dtime1,time,dtime2)
        if dtime1 <= time <= dtime2:
            dist = jarak
            if dist <= rad:
                dis = ('%.1f')%float(dist)
                lat,long,type = str(y),str(x),str(type)
                wkt = time.strftime('%Y-%m-%d %H:%M:%S')
                if type == '0':
                    tipe = 'CG+'
                elif type == '1':
                    tipe = 'CG-'
                else:
                    tipe = 'IC'
                pos = [lat,long,wkt,dis,type]
                poss.append(pos)
    
    return poss



def pelayanan(lat,long,time1,time2,utc,rad,filedb):

    tgl1 = time1.split()[0]
    tgl2 = time2.split()[0]
    wkt1 = time1.split()[1]
    wkt2 = time2.split()[1]
    h1,m1 = wkt1[:2],wkt1[3:5]
    h2,m2 = wkt2[:2],wkt2[3:5]
    rad = float(rad)
    utc = float(utc)
    bts = rad/100

    dtime1 = tgl1+' '+h1+':'+m1+':'+'00.000'
    dtime2 = tgl2+' '+h2+':'+m2+':'+'00.000'

    dtime1 = datetime.strptime(dtime1, '%d-%m-%Y %H:%M:00.000')
    dtime2 = datetime.strptime(dtime2, '%d-%m-%Y %H:%M:00.000')

    dtutc1 = dtime1-timedelta(hours=float(utc))
    dtutc2 = dtime1-timedelta(hours=float(utc))

    latmin,latmax = str(float(lat)-bts),str(float(lat)+bts)
    longmin,longmax = str(float(long)-bts),str(float(long)+bts)
    batas = [longmin,longmax,latmin,latmax]

    rad = float(rad)
    utc = float(utc)
    custloc = (float(lat),float(long))

    sorted = pelayanan_sortir(custloc,tgl1,tgl2,dtime1,dtime2,utc,batas,rad,filedb)

    # print(sorted)
    



    
    print('inii pelayanan petir #########')
    return sorted


def datarange(date2,date1):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

    return 'done'
def range_waktu(dt_0,dt_1):
        #dt_0 = self.ui.export_date1.text()
        #dt_1 = self.ui.export_date2.text()
        fname = dt_0
        y_0 = int(fname.strftime('%Y'))
        m_0 = int(fname.strftime('%m'))
        d_0 = int(fname.strftime('%d'))
        ymd_0 = y_0, m_0, d_0
        tgl0 = fname.strftime('%d-%b-%Y')
        fname = dt_1
        y_1 = int(fname.strftime('%Y'))
        m_1 = int(fname.strftime('%m'))
        d_1 = int(fname.strftime('%d'))
        ymd_1 = y_1, m_1, d_1
        tgl1 = fname.strftime('%d-%b-%Y')
        return ymd_0, ymd_1, tgl0, tgl1

def fromdbsta(dt_0,dt_1):
    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    databases = []
    range_wkt = range_waktu(dt_0,dt_1)
    ymd_0 = range_wkt[0]
    ymd_1 = range_wkt[1]
    start_dt = date(ymd_0[0], ymd_0[1], ymd_0[2])
    end_dt = date(ymd_1[0], ymd_1[1], ymd_1[2])
    for dt in daterange(start_dt, end_dt):
        f_thn = str(dt.strftime('%Y'))
        f_bln = str(dt.strftime('%-m'))
        filename = str(dt.strftime("%Y%m%d") + '.db3')
        dir = 'fungsi/data/DB3/' + f_thn + '/' + f_bln
        # file = os.path.join(dir+os.sep, filename)
        file = dir + '/' + filename
        databases.append(file)

    return databases

def samutc2loc(datasam,utc,fout):
    fo = open(fout, 'w')
    f = open(datasam, 'r')
    baris = f.readlines()
    for i in range(len(baris)):
        baris[i] = baris[i].split()
        dt = baris[i][2]+' '+baris[i][3][:2]+':'+baris[i][3][3:5]+':'+baris[i][3][6:8]
        dtime = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
        dtloc = dtime + timedelta(hours=float(utc))
        dtlocal = dtloc.strftime('%Y-%m-%d\t%H:%M:%S')
        fo.write(baris[i][0]+'\t'+baris[i][1]+'\t'+dtlocal+'\t'+baris[i][4]+ '\n')
    fo.close()


def readdb3(databases,fileout,batas):
    f = open(fileout, 'w')
    xmin,xmax = batas[0],batas[1]
    ymin,ymax = batas[2],batas[3]
    for database in databases:
        try:
            with sqlite3.connect(database) as conn:
                conn.text_factory = str
                cur = conn.cursor()
                values = (ymin,ymax,xmin,xmax,0,1,2)
                sql = '''SELECT DISTINCT longitude,latitude,datetime_utc,type FROM NGXLIGHTNING WHERE 
                latitude between ? and ? and (longitude between ? and ?) and (type in (?,?,?))'''
                c = cur.execute(sql,values)
                for row in c.fetchall():
                    f.write(' '.join(str(r) for r in row) + '\n')

        except sqlite3.Error as err:
            file = (database)
            print("Data " + file + " Error !!")
            print(err)

    f.close()
    f = open(fileout, 'r')
    fcgp = open('fungsi/gmt/sambarancgp.dat', 'w')
    fcgm = open('fungsi/gmt/sambarancgm.dat', 'w')
    fcg = open('fungsi/gmt/sambarancg.dat', 'w')
    fic = open('fungsi/gmt/sambaranic.dat', 'w')
    baris = f.readlines()
    for i in range(len(baris)):
        baris[i] = baris[i].split()
        tipe = baris[i][4]
        if float(tipe) == 0:
            for item in baris[i]:
                fcgp.write("%s\t" % str(item))
            fcgp.write("\n")
        elif float(tipe) == 1:
            for item in baris[i]:
                fcgm.write("%s\t" % str(item))
            fcgm.write("\n")
        else:
            for item in baris[i]:
                fic.write("%s\t" % str(item))
            fic.write("\n")
        if float(tipe) != 2:
            for item in baris[i]:
                fcg.write("%s\t" % str(item))
            fcg.write("\n")

    f.close()
    fcgp.close()
    fcgm.close()
    fcg.close()
    fic.close()
    return 'ok'

def gridding(datasambaran,batas):
    xmin,xmax = batas[0],batas[1]
    ymin,ymax = batas[2],batas[3]
    datagrid = datasambaran+'.xyz'
    os.system("gmt blockmean "+datasambaran+".dat -R"+xmin+"/"+xmax+"/"+ymin+"/"+ymax+
        " -I1k -Sn | gmt xyz2grd -R"+xmin+"/"+xmax+"/"+ymin+"/"+ymax+" -I1k -Gfungsi/gmt/gridding.grd") 
    # gmt blockmean sambaran.dat -R127/128/0.3/1.3 -I1k -Sn | gmt xyz2grd -R127/128/0.3/1.3 -I1k -Gtesblok.grd
    # gmt grd2xyz tesblok.grd -d0> tesblok.xyz
    os.system("gmt grd2xyz fungsi/gmt/gridding.grd -d0 > "+datagrid)
    return datagrid

def interpolasi(datagridxyz):
    idw = saveidw(datagridxyz)
    file = idw[0]
    zmax,zmin = idw[1],idw[2]
    return file,zmax,zmin

def sumwilayah():
    run("fungsi/gmt/sumwilayah.sh", shell=True)


