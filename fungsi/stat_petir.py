import pandas as pd
from datetime import datetime, timedelta

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def xyz2xls(filexyz,fileout):
    df = pd.read_csv(filexyz, delim_whitespace=True,header=None)
    df.to_excel(fileout)
    

def exp_sumharian(datasam,start,end,fpath):
    f1 = pd.read_csv(datasam, delim_whitespace=True,header=None)
    total = f1[0].count()
    tot_cgp= f1[f1[4] == 0].count()
    tot_cgm= f1[f1[4] == 1].count()
    tot_ic= f1[f1[4] == 2].count()
    dt0 = start.strftime('%Y-%m-%d')
    dt1 = end.strftime('%Y-%m-%d')

    f = open(fpath, 'w')
    header = ("Tipe", "Jumlah")
    f.write('SAMBARAN TOTAL' + '\n')
    f.write(','.join(header) + '\n')
    f.write('CG+,'+str(tot_cgp[1])+ '\n')
    f.write('CG-,'+str(tot_cgm[1])+ '\n')
    f.write('IC,'+str(tot_ic[1])+ '\n')
    f.write('Jumlah Total,'+str(total)+ '\n')
    f.write('\n')

    header = ("Tanggal","CG+","CG-","IC", "Jumlah")
    f.write('SAMBARAN PER HARI' + '\n')
    f.write(','.join(header) + '\n')

    f1 = pd.read_csv(datasam, delim_whitespace=True, header=None)
    for dt in daterange(start, end):
        date = str(dt.strftime('%Y-%m-%d'))
        tgl = str(dt.strftime('%d-%b-%y'))
        #print(date)
        #print(f1[0])
        tot_tglcgp = f1[(f1[2] == str(date)) & (f1[4] == 0)].count()
        tot_tglcgm = f1[(f1[2] == str(date)) & (f1[4] == 1)].count()
        tot_tglic = f1[(f1[2] == str(date)) & (f1[4] == 2)].count()
        tot_tgl = f1[f1[2] == str(date)].count()
        f.write(tgl+','+str(tot_tglcgp[1]) +','+str(tot_tglcgm[1]) +','+str(tot_tglic[1]) +','+str(tot_tgl[1]) + '\n')

def export(datasam,start,end,fpath):
    f1 = pd.read_csv(datasam, delim_whitespace=True,header=None)
    total = f1[0].count()
    tot_cgp= f1[f1[4] == 0].count()
    tot_cgm= f1[f1[4] == 1].count()
    tot_ic= f1[f1[4] == 2].count()
    dt0 = start.strftime('%Y-%m-%d')
    dt1 = end.strftime('%Y-%m-%d')

    f = open(fpath, 'w')
    header = ("Tipe", "Jumlah")
    f.write('SAMBARAN TOTAL' + '\n')
    f.write(','.join(header) + '\n')
    f.write('CG+,'+str(tot_cgp[1])+ '\n')
    f.write('CG-,'+str(tot_cgm[1])+ '\n')
    f.write('IC,'+str(tot_ic[1])+ '\n')
    f.write('Jumlah Total,'+str(total)+ '\n')
    f.write('\n')

    header = ("Tanggal","CG+","CG-","IC", "Jumlah")
    f.write('SAMBARAN PER HARI' + '\n')
    f.write(','.join(header) + '\n')

    f1 = pd.read_csv(datasam, delim_whitespace=True, header=None)
    for dt in daterange(start, end):
        date = str(dt.strftime('%Y-%m-%d'))
        tgl = str(dt.strftime('%d-%b-%y'))
        #print(date)
        #print(f1[0])
        tot_tglcgp = f1[(f1[2] == str(date)) & (f1[4] == 0)].count()
        tot_tglcgm = f1[(f1[2] == str(date)) & (f1[4] == 1)].count()
        tot_tglic = f1[(f1[2] == str(date)) & (f1[4] == 2)].count()
        tot_tgl = f1[f1[2] == str(date)].count()
        f.write(tgl+','+str(tot_tglcgp[1]) +','+str(tot_tglcgm[1]) +','+str(tot_tglic[1]) +','+str(tot_tgl[1]) + '\n')

    f.write('\n')
    kecamatan=['Ternate Selatan','Ternate Tengah','Ternate Utara','Pulau Ternate',
            'Tidore','Tidore Selatan','Tidore Utara','Tidore Timur','Oba Utara',
            'Jailolo Selatan','Jailolo']

    f.write('SAMBARAN PER WILAYAH' + '\n')
    f1 = pd.read_csv('fungsi/gmt/sumwilayah.dat', delim_whitespace=True, header=None)
    header = ("KECAMATAN","CG+","CG-","IC", "Jumlah")
    f.write(','.join(header) + '\n')

    for i in range(len(kecamatan)):
        tot_keccgp = f1[(f1[3] == i) & (f1[2] == 0)].count()
        tot_keccgm = f1[(f1[3] == i) & (f1[2] == 1)].count()
        tot_kecic = f1[(f1[3] == i) & (f1[2] == 2)].count()
        tot_kec = f1[f1[3] == i].count()
        f.write(kecamatan[i]+','+str(tot_keccgp[0])+','+str(tot_keccgm[0])+','+str(tot_kecic[0])+','+str(tot_kec[0])+'\n')

    return dt0,dt1

def chartpetir(datasam,start,end):
    f1 = pd.read_csv(datasam, delim_whitespace=True, header=None)
    sumharian = []
    for dt in daterange(start, end):
        date = str(dt.strftime('%Y-%m-%d'))
        tgl = str(dt.strftime('%d-%b-%y'))
        tot_tglcgp = f1[(f1[2] == str(date)) & (f1[4] == 0)].count()
        tot_tglcgm = f1[(f1[2] == str(date)) & (f1[4] == 1)].count()
        tot_tglic = f1[(f1[2] == str(date)) & (f1[4] == 2)].count()
        tot_tgl = f1[f1[2] == str(date)].count()
        sumharian += [[tgl,tot_tglcgp[1],tot_tglcgm[1],tot_tglic[1],tot_tgl[1]]]


    kecamatan=['Ternate Selatan','Ternate Tengah','Ternate Utara','Pulau Ternate',
            'Tidore','Tidore Selatan','Tidore Utara','Tidore Timur','Oba Utara',
            'Jailolo Selatan','Jailolo']
    f1 = pd.read_csv('fungsi/gmt/sumwilayah.dat', delim_whitespace=True, header=None)
    sumwil = []
    for i in range(len(kecamatan)):
        tot_keccgp = f1[(f1[3] == i) & (f1[2] == 0)].count()
        tot_keccgm = f1[(f1[3] == i) & (f1[2] == 1)].count()
        tot_kecic = f1[(f1[3] == i) & (f1[2] == 2)].count()
        tot_kec = f1[f1[3] == i].count()
        sumwil += [[kecamatan[i],tot_keccgp[0],tot_keccgm[0],tot_kecic[0],tot_kec[0]]]

    return sumharian,sumwil

    