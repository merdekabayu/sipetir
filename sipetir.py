from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_mysqldb import MySQL
from calendar import monthrange
from datetime import datetime, timedelta
import openpyxl
import time
import fungsi.inputmanual as input
import fungsi.mapping as mapping
import fungsi.infogempa as infogempa
import fungsi.filter as f
import fungsi.infografis as ig
from fungsi.stat_petir import *
from fungsi.dataproc import *
from fungsi.nex2db import nex2db
from fungsi.statistik import hitung_wilayah, hitung_chart
from fungsi.filter import filter_area
from fungsi.arrival import  esdx2pha, arrival2spk, arrivalsc4tnt, arrivalsc3pst
from fungsi.stat_sensor import status,slinktool, tabel_slinktool
from fungsi.waveform import waveformplot, allwaveform, down_waveformbyevent
import subprocess,os
import bcrypt
from zipfile import ZipFile

#os.system('whoami')


app = Flask(__name__)
app.secret_key = "membuatLOginFlask1"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sigempa2023'
app.config['MYSQL_DB'] = 'sistem_diseminasi'
app.config["UPLOAD_FOLDER"] = "static/upload/"

mysql = MySQL(app)

@app.route('/htmltes')
def tes():
    
    return render_template('htmltes.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login(): 

    if request.method == 'POST':
        usr = request.form['username']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM users WHERE user=%s",(usr,))
        user = curl.fetchone()
        #print(user['password'])
        curl.close()

        if user is not None and len(user) > 0 :
            #print(password)
            if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
                session['id'] = user[0]
                session['user'] = user[1]
                return redirect(url_for('index'))
            else :
                #session.clear()
                flash("Wrong Password !!")
                return render_template("loginpage.html")
                #return redirect(url_for('login'))
        else :
            flash("User Not Found !!")
            return render_template("loginpage.html")
    else:
        #session.clear()
        return render_template("loginpage.html")
    
    #return render_template("loginpage.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) 


@app.route('/')

def index():
    if 'user' in session:
        
        
        return render_template('mainpetir.html')
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    

@app.route('/index/tabelgempa')
def tabelgempa():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM db_gempa ORDER BY 2 DESC, 3 DESC LIMIT 0, 50")
        parameter = cur.fetchall()
        cur.close()
        noshakemap = '../static/noshakemap.jpg'
        return render_template('tabeleq.html', data=parameter, shakemap=noshakemap)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))


@app.route('/infografis/mingguan')
def ig_mingguan():
    hari = 7
    tdy = datetime.today()
    end = (tdy - timedelta(days=1))
    start = (tdy - timedelta(days=hari))
    
    chart = ig.infografis(start,end)
    sam = chart[0][3]
    z = chart[1]
    total = chart[2]
    sumharian = chart[3][0]
    sumwil = chart[3][1]
    print(sumharian)
    
    rangedate = chart[4]

    
    # print(sam)

    return render_template('infog_mingguan.html',z=z, sam=sam,
                                                total=total, sumharian=sumharian,sumwil=sumwil,
                                                rangedate=rangedate)


@app.route('/infografis/bulanan')
def ig_bulanan():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    thn = last_month.year
    bulan = last_month.month
    lhari = last_month.day
    end = datetime(thn,bulan,lhari)
    start = datetime(thn,bulan,1)
    
    chart = ig.infografis(start,end)
    sam = chart[0][3]
    z = chart[1]
    total = chart[2]
    sumharian = chart[3][0]
    sumwil = chart[3][1]
    print(sumharian)
    
    rangedate = chart[4]

    
    # print(sam)

    return render_template('infog_bulanan.html',z=z, sam=sam,
                                                total=total, sumharian=sumharian,sumwil=sumwil,
                                                rangedate=rangedate)



@app.route('/infografis/custom', methods=["POST","GET"])
def customig():
    if 'user' in session:
        if request.method == 'POST':
            date = request.form['datefilter']
            
            datestart = date.split()[0]
            dateend = date.split()[2]
            
            start = datetime.strptime(datestart, '%d-%b-%y')
            end = datetime.strptime(dateend, '%d-%b-%y')

            chart = ig.infografis(start,end)
            sam = chart[0][3]
            z = chart[1]
            total = chart[2]
            sumharian = chart[3][0]
            sumwil = chart[3][1]
            print(sumharian)
            
            rangedate = chart[4]

            
            # print(sam)

            return render_template('infog_custom.html',z=z, sam=sam,
                                                        total=total, sumharian=sumharian,sumwil=sumwil,
                                                        rangedate=rangedate)
        else:
            return redirect(url_for('ig_mingguan'))
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

@app.route('/pelayanan-petir')
def pelayananpetir():
    if 'user' in session:
        
        
        cust = [0.777, 127.3667]

        return render_template('pelayanan.html', cust=cust)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
@app.route('/pelayanan-petir/sorted', methods=["POST","GET"])
def filter_tabel():
    # try:
        if request.method == 'POST':
            lat = request.form['lat']
            long = request.form['long']
            time1 = request.form['date1']
            time2 = request.form['date2']
            rad = request.form['rad']
            utc = request.form['utc']
            filedb = request.files.getlist("file")

            sambaran = pelayanan(lat,long,time1,time2,utc,rad,filedb)
            print('iniiii leenn',len(sambaran))
            cust = [lat,long]
            # filter = f.filter_parameter(date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2)
            return render_template('pelayanan.html',cust=cust,sambaran=sambaran, date = [time1,time2])
        else:
            today = datetime.today()
            filter = f.filter_parameter()
            today = today.strftime('%d-%m-%Y %H:%M')
            
            return render_template('pelayanan.html',data=filter, date = [today,today])
    # except:
        return redirect(url_for('pelayananpetir'))

@app.route('/data-processing')
def data_proc():
    if 'user' in session:
        
        
        cust = [0.777, 127.3667]

        return render_template('prosesing_data.html', cust=cust)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
@app.route('/data-processing/nex2db', methods=["POST"])
def proc_nex2db():
    if 'user' in session:
        if request.method == 'POST':
            lat = request.form['lat']
            long = request.form['long']
            utc = request.form['utc']
            filenexs = request.files.getlist("file")
            fileout = request.form['fileout']
            
            nexs = []
            for files in filenexs:
                fname = secure_filename(files.filename)
                files.save(app.config['UPLOAD_FOLDER'] + fname)
                nexs.append(app.config['UPLOAD_FOLDER'] + fname)

            fouts = []
            for nex in nexs:
                fout = nex2db(long,lat,utc,nex)
                fdb,fcsv = fout[0],fout[1]
                fouts.append(fdb)
                fouts.append(fcsv)

            with ZipFile('fungsi/nxutil/'+fileout+'.zip','w') as zip:
                for file in fouts:
                    zip.write(file,file.split('/')[2])


            return send_file('fungsi/nxutil/'+fileout+'.zip', as_attachment=True)
        
        
            # return redirect(url_for('pelayananpetir'))
            
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
@app.route('/data-processing/gridding', methods=["POST"])
def proc_gridding():
    if 'user' in session:
        if request.method == 'POST':
            latmin = request.form['latmin']
            longmin = request.form['longmin']
            latmax = request.form['latmax']
            longmax = request.form['longmax']
            filedb = request.files.getlist("file")
            fileout = request.form['fileout']

            batas = [longmin,longmax,latmin,latmax]
            databases = []
            for files in filedb:
                fname = secure_filename(files.filename)
                files.save(app.config['UPLOAD_FOLDER'] + fname)
                databases.append(app.config['UPLOAD_FOLDER'] + fname)
            
            
            fdat = 'fungsi/'+fileout+'.dat'
            # fdat = 'fungsi/dataproc_sumharian.dat'
            readdb3(databases,fdat,batas)
            fdat = 'fungsi/'+fileout
            filexyz = gridding(fdat,batas)

            dir = 'fungsi/export/'
            fpath = dir+fileout+'.csv'
            df = pd.read_csv(filexyz,delim_whitespace=True,names=['Long','Lat','Sum'],index_col=False)
            df.to_csv(fpath,index=False)

            print(databases)
            # path = 'fungsi/export/Statistik Petir Mingguan Periode 2023-07-10 sd 2023-07-16.csv'
            return send_file(fpath, as_attachment=True)
        
        
            # return redirect(url_for('pelayananpetir'))
            
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

@app.route('/data-processing/sumharian', methods=["POST","GET"])
def proc_sumharian():
    if 'user' in session:
        if request.method == 'POST':
            latmin = request.form['latmin']
            longmin = request.form['longmin']
            latmax = request.form['latmax']
            longmax = request.form['longmax']
            time1 = request.form['date1']
            time2 = request.form['date2']
            filedb = request.files.getlist("file")
            fileout = request.form['fileout']

            batas = [longmin,longmax,latmin,latmax]
            start = datetime.strptime(time1,'%d-%m-%Y')
            end = datetime.strptime(time2,'%d-%m-%Y')

            print(filedb)
            databases = []
            for files in filedb:
                print(files)
                fname = secure_filename(files.filename)
                files.save(app.config['UPLOAD_FOLDER'] + fname)
                databases.append(app.config['UPLOAD_FOLDER'] + fname)
            
            
            fdat = 'fungsi/'+fileout+'.dat'
            # fdat = 'fungsi/dataproc_sumharian.dat'
            readdb3(databases,fdat,batas)

            dir = 'fungsi/export/'
            fpath = dir+fileout+'.csv'
            exp_sumharian(fdat,start,end,fpath)

            print(databases)
            # path = 'fungsi/export/Statistik Petir Mingguan Periode 2023-07-10 sd 2023-07-16.csv'
            return send_file(fpath, as_attachment=True)
        
        
            # return redirect(url_for('pelayananpetir'))
            
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

@app.route('/infografis/filter')
def filterig():
    if 'user' in session:
        tdy = datetime.today()
        end = tdy
        start = tdy - timedelta(days=30)
        
        chart = ig.infografis(start,end)
        par = chart[0]
        stat = chart[1]
        jml_gempa = stat[0][0]
        jml_drskn = stat[0][1]
        hist_harian = stat[0][2]
        mag = stat[0][3]
        depth = stat[0][4]
        hist_mag = stat[0][5]
        hist_tab = stat[0][6]
        wilayah = stat[1][:7]
        rangedate = chart[2]

        start,end = "a","a"
        #mapping.map_seismisitas_mingguan(start,end)

        today = datetime.today()
        day30ago = today - timedelta(days=30)
        today = today.strftime('%d-%m-%Y %H:%M')
        day30ago = day30ago.strftime('%d-%m-%Y %H:%M')
        depth1 = 0
        depth2 = 1000
        mag1 = 1.0
        mag2 = 9.0
        lat1 = 3.50
        lat2 = -2.75
        long1 = 124.00
        long2 = 130.00
        felt = 0
        #submit_ok = True
        filemap = subprocess.check_output('ls static/seismisitas*.jpg',shell=True)
        mapf = filemap.decode().split('\n')[1]
        return render_template('infog_filter.html', mapfile=mapf,data=par,
                                                    jml_gempa=jml_gempa,
                                                    jml_drskn=jml_drskn,
                                                    hist_harian=hist_harian,
                                                    mag=mag,
                                                    depth=depth,
                                                    hist_mag=hist_mag,
                                                    hist_tab=hist_tab,
                                                    wilayah=wilayah,
                                                    rangedate=rangedate, date = [day30ago,today,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2,felt])
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

@app.route('/infografis/filteredig', methods=["POST","GET"])
def filtered_ig():
    try:
        if request.method == 'POST':
            date1 = request.form['date1']
            date2 = request.form['date2']
            depth1 = request.form['depth1']
            depth2 = request.form['depth2']
            mag1 = request.form['mag1']
            mag2 = request.form['mag2']
            lat1 = request.form['lat1']
            lat2 = request.form['lat2']
            long1 = request.form['long1']
            long2 = request.form['long2']
            felt = request.form.getlist('felt')
            felt = len(felt)
            print('halo0000 disini felt ############',felt)
            start = datetime.strptime(date1, '%d-%m-%Y %H:%M').date()
            end = datetime.strptime(date2, '%d-%m-%Y %H:%M').date()
            hari = (end - start).days+1
            date_list = [end - timedelta(days=x) for x in range(hari)]
            date_list.sort()
            chart = ig.infografis_parfilter(date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2,felt)
            par = chart[0]
            stat = chart[1]
            jml_gempa = stat[0][0]
            jml_drskn = stat[0][1]
            hist_harian = stat[0][2]
            mag = stat[0][3]
            depth = stat[0][4]
            hist_mag = stat[0][5]
            hist_tab = stat[0][6]
            wilayah = stat[1][:7]
            rangedate = chart[2]
            filemap = subprocess.check_output('ls static/seismisitas*.jpg',shell=True)
            mapf = filemap.decode().split('\n')[1]
            return render_template('infog_filter.html',mapfile=mapf, data=par,
                                                    jml_gempa=jml_gempa,
                                                    jml_drskn=jml_drskn,
                                                    hist_harian=hist_harian,
                                                    mag=mag,
                                                    depth=depth,
                                                    hist_mag=hist_mag,
                                                    hist_tab=hist_tab,
                                                    wilayah=wilayah,
                                                    rangedate=rangedate, date = [date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2,felt])
        else:
            today = datetime.today()
            filter = f.filter_parameter()
            today = today.strftime('%d-%m-%Y %H:%M')

            filemap = subprocess.check_output('ls static/seismisitas*.jpg',shell=True)
            mapf = filemap.decode().split('\n')[0]
            
            return render_template('infog_filter.html',mapfile=mapf,data=filter, date = [today,today])

    except:
        return redirect(url_for('filterig'))

# @app.route('/database')
# def database():
#     if 'user' in session:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM db_gempa ORDER BY 2 DESC, 3 DESC LIMIT 0, 50")
#         parameter = cur.fetchall()
#         cur.close()
#         today = datetime.today()
#         day30ago = today - timedelta(days=30)
#         today = today.strftime('%d-%m-%Y %H:%M')
#         day30ago = day30ago.strftime('%d-%m-%Y %H:%M')
#         depth1 = 0
#         depth2 = 1000
#         mag1 = 1.0
#         mag2 = 9.0
#         lat1 = 3.50
#         lat2 = -2.75
#         long1 = 124.00
#         long2 = 130.00
#         return render_template('database.html',data=parameter, date = [day30ago,today,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2])
#     else:
#         flash("Please, Login First !!")
#         return redirect(url_for('login'))

# @app.route('/database/sorted', methods=["POST","GET"])
# def filter_tabel():
#     try:
#         if request.method == 'POST':
#             date1 = request.form['date1']
#             date2 = request.form['date2']
#             depth1 = request.form['depth1']
#             depth2 = request.form['depth2']
#             mag1 = request.form['mag1']
#             mag2 = request.form['mag2']
#             lat1 = request.form['lat1']
#             lat2 = request.form['lat2']
#             long1 = request.form['long1']
#             long2 = request.form['long2']
#             filter = f.filter_parameter(date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2)
#             return render_template('database.html',data=filter, date = [date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2])
#         else:
#             today = datetime.today()
#             filter = f.filter_parameter()
#             today = today.strftime('%d-%m-%Y %H:%M')
            
#             return render_template('database.html',data=filter, date = [today,today])
#     except:
#         return redirect(url_for('database'))

    

@app.route('/export/<string:tipe>', methods=["GET"])
def exp(tipe):
    if 'user' in session:
        tdy = datetime.today()
        type = tipe.split('!')[0]
        datasam = 'fungsi/gmt/sambaran.dat'
        if type == 'mingguan':
            hari = 7
            end = (tdy - timedelta(days=1))
            start = (tdy - timedelta(days=hari))
            fpath = 'fungsi/export/Statistik Petir Mingguan Periode '
        elif type == 'bulanan':
            first = tdy.replace(day=1)
            last_month = first - timedelta(days=1)
            thn = last_month.year
            bulan = last_month.month
            lhari = last_month.day
            end = datetime(thn,bulan,lhari)
            start = datetime(thn,bulan,1)
            date_list = [end - timedelta(days=x) for x in range(lhari)]
            date_list.sort()
            fpath = 'fungsi/export/Statistik Gempa Bulanan '
            chart = ig.infografis(start,end)
        elif type == 'customig':
            tgl = tipe.split('!')[1]
            start = tgl.split('@')[0]
            end = tgl.split('@')[1]
            start = datetime.strptime(start, '%d-%B-%Y').date()
            end = datetime.strptime(end, '%d-%B-%Y').date()
            hari = (end - start).days+1
            date_list = [end - timedelta(days=x) for x in range(hari)]
            date_list.sort()
            fpath = 'fungsi/export/Statistik Gempa Periode '
            chart = ig.infografis(start,end)
        

        dt0 = start.strftime('%Y-%m-%d')
        dt1 = end.strftime('%Y-%m-%d')
        path = fpath+dt0+' sd '+dt1+'.csv'
            
        
        export(datasam,start,end,fpath=path)
        
        return send_file(path, as_attachment=True)
        
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))


@app.route('/database/arrival')
def arrival():
    if 'user' in session:
        today = datetime.today()
        day30ago = today - timedelta(days=30)
        today = today.strftime('%d-%m-%Y %H:%M')
        day30ago = day30ago.strftime('%d-%m-%Y %H:%M')
        depth1 = 0
        depth2 = 1000
        mag1 = 1.0
        mag2 = 9.0
        lat1 = 3.50
        lat2 = -2.75
        long1 = 124.00
        long2 = 130.00
        return render_template('database_arrival.html', date = [day30ago,today,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2])
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

@app.route('/database/downloadarrival', methods=["POST"])
def arrival_download():
    if 'user' in session:
        date1 = request.form['date1']
        date2 = request.form['date2']
        depth1 = request.form['depth1']
        depth2 = request.form['depth2']
        mag1 = request.form['mag1']
        mag2 = request.form['mag2']
        lat1 = request.form['lat1']
        lat2 = request.form['lat2']
        long1 = request.form['long1']
        long2 = request.form['long2']
        felt = 0
        format = request.form['format_arrival']
        source = request.form['data_source']

        resptnt = os.system('ping -c 1 scproc')
        resppst=os.system("sshpass -p 'bmkg212$' ssh -t -p2222 sysop@scproc ping -c 1 172.19.3.51")
        print('disini respon',resppst,resptnt)
        if source == 'SPK':
            path = arrival2spk(date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2,felt)
            nfile = path.split('.')[0]
            nfile = nfile.split('/')[2]
            namefile = nfile+'_'+date1+'_'+date2+'_'+depth1+'_'+depth2+'_'+mag1+'_'+mag2+'_'+lat1+'_'+lat2+'_'+long1+'_'+long2+'.txt'
        
        
        elif source == 'Seiscomp4 Ternate' and resptnt == 0:
            path = arrivalsc4tnt(date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2,felt)
            nfile = path.split('.')[0]
            nfile = nfile.split('/')[2]
            namefile = nfile+'_'+date1+'_'+date2+'_'+depth1+'_'+depth2+'_'+mag1+'_'+mag2+'_'+lat1+'_'+lat2+'_'+long1+'_'+long2+'.txt'
        elif source == 'Repogempa PGN'and resptnt == 0 and resppst == 0:
            path = arrivalsc3pst(date1,date2,depth1,depth2,mag1,mag2,lat1,lat2,long1,long2,felt)
            nfile = path.split('.')[0]
            nfile = nfile.split('/')[2]
            namefile = nfile+'_'+date1+'_'+date2+'_'+depth1+'_'+depth2+'_'+mag1+'_'+mag2+'_'+lat1+'_'+lat2+'_'+long1+'_'+long2+'.txt'
        elif resptnt != 0 or resppst != 0:
            flash("Request Fail",'fail')
            return redirect(request.referrer)


    
        
        if format == 'HypoDD (*.pha)':
            finp = path
            path = esdx2pha(finp)
            nfile = path.split('.')[0]
            nfile = nfile.split('/')[2]
            namefile = nfile+'_'+date1+'_'+date2+'_'+depth1+'_'+depth2+'_'+mag1+'_'+mag2+'_'+lat1+'_'+lat2+'_'+long1+'_'+long2+'.pha'
        
        print(namefile)
        #path ='fungsi/export/Data Arrival Format 2.txt'
        return send_file(path, as_attachment=True, download_name=namefile)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))



@app.route('/sensor/status', methods=["POST","GET"])
def sensor_stat():
    
    resptnt = os.system('ping -c 1 scproc')
    if resptnt == 0:
        print('ini sensor/status')
        data = slinktool()
        print('ini slibktool ok')
        last_data = data[0]
        print(last_data)
        today = data[1]
        stat = status(last_data,today)
        tabel = tabel_slinktool(last_data,today)
        #waveform = 

        utcnow = datetime.utcnow()
        utctime = utcnow.time()
        timerange = datetime(2023,1,1,15,0,1).time()
        timerange1 = datetime(2023,1,1,23,55,0).time()
        dt = datetime.utcnow()
        yes = (dt - timedelta(days=1))
        yest = yes.strftime('%d%m%y')
        
        fileav='static/availability_'+yest+'.png'
        print('sampee siniiii ####',fileav)
        if not os.path.exists(fileav):
            os.system('sshpass -p "bmkg212$" ssh -p2222 sysop@36.91.152.130 sh run_availability.sh')
            command = 'sshpass -p "bmkg212$" scp -P 2222 -r sysop@36.91.152.130:availability_new.png '+fileav
            os.system(command)

        if request.method == 'GET':
            sta = 'TNTI'
        else:
            sta = request.form['station']
        try:
            waveformplot(sta)
            nodata = ''
            fwav = subprocess.check_output('ls static/waveform/waveform24h'+sta+'*.jpg',shell=True)
            wavf = fwav.decode().split('\n')[0]
            
        except:
            nodata = 'nodata'
            wavf = ''
        
        filemap = subprocess.check_output('ls static/sensor_status*.jpg',shell=True)
        mapf = filemap.decode().split('\n')[0]
        return render_template('sensor_stat.html', ping=resptnt,gambar=[mapf,wavf], data=tabel,fileav=fileav,sta=sta,nodata = nodata)
    else:
        return render_template('sensor_stat.html', ping=resptnt)
    
    #os.system('ls static/waveform/waveform24h'+sta+'*.jpg')
    
     

    
if __name__ == "__main__":
	app.run(debug=True)
