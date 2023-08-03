set gempa=seismisitas-kalimantan.dat
set dirasakan=dirasakan-kalimantan.dat
set name=kalimantan
set REGION=107/122/-7/8
set SIZE=M16c
set AXIS=a2f1/a2f1NWse
set psfile=%name%.ps
set stasiun=stasiun.dat

grdimage indo.nc -R%region% -J%size% -Cbatimetri.cpt -Sn -Q -K -V -I+a0+nt0.5 -Y3.5 > %psfile%
#pscoast -Dh -R%region% -J%size% -W0.6,gray30 -K -O -V >> %psfile%
psxy -R -JM -W1.5 -Sf0.4i/0.06ilt -Gblack -m -O -K  trench.gmt >> %psfile%
psxy -R -JM -W1.5 -O -K transform.gmt -Dh -m >> %psfile%
psxy -R -JM -W0.6 -O -K indo_prop.gmt -Dh -m >> %psfile%


gawk "{print $1, $2, $3, $4*0.035}" %gempa% | psxy -J -R -Sci -Cdepth.cpt -W0.5 -O  -K -V >> %psfile%
gawk "{print $1, $2, $3}" %dirasakan% | psxy -J -R -Sa0.25i -Cdepth.cpt -W1 -O  -K -V >> %psfile%
gawk "{print $1, $2, $3}" %stasiun% | psxy -J -R -St0.25i -Ggreen -W0.5 -O  -K -V >> %psfile%
gawk "{print $1+0.5, $2+0.15, BR, $3}" %stasiun% | pstext -J -R -F+f9,Times-Bold,black -O -K >> %psfile%
echo 126.23 0.41 > garis
echo 125.5 0 >> garis
psxy garis -J -R -W0.8,black -O -K -V >> %psfile%
psmeca focal.gmt -R -J -B -Sa0.8 -O -K >> %psfile%

psbasemap -J -R -B%axis% -Lf109.5/6/0/200+lkm  --MAP_LABEL_OFFSET=0.1 --FONT_LABEL=13p,Heveltica --MAP_FRAME_TYPE=fancy --FONT_ANNOT=12p -K -O -V >> %psfile%

echo 128.72 0.72 45 90 34  BL \343 > kompas
echo 128.7 0.69 20 0 1 BR N >> kompas
pstext kompas -R -J -O -K -V  >> %psfile%

psxy kota-kalimantan.txt -J -R -O -K -Sc0.06i -G0 >> %psfile%
psxy kota-prop.txt -J -R -O -K -Ss0.08i -G0 >> %psfile%
gawk "{print $1+0.5, $2+0.15, BR, $3, $4}" kota-kalimantan.txt | pstext -J -R -F+f9,Times-Bold,black -O -K >> %psfile%
gawk "{print $1-0.15, $2+0.08, TL, $4}" kota-prop.txt | pstext -J -R -F+f12,Times-Bold,black -O -K >> %psfile%

pslegend legenda-kalimantan.txt -R -J -F+gwhite+p -Dx4.75i/0.25i/7.5i/0.95i/TC -C0.1i/0.1i -O -K -Y-1.5 -X-4 >> %psfile%

@REM pscoast -JM8c -R90/144/-12/10 -Ba180nwse -Dh -W0.6,black -Swhite -Ggrey -O --MAP_FRAME_TYPE=plain -X4.2 -Y1.8>> %psfile%

pscoast -Dl -R95/140/-12/10 -JM6 -Blrbt -Wthinnest -Swhite -Ggray40 -O -K -V -X4.15 -Y1.6 --MAP_FRAME_TYPE=plain >> %psfile%

107/122/-7/8
echo 107 -7  > kotak
echo 107 8 >> kotak
echo 122 8 >> kotak
echo 122 -7 >> kotak
echo 107 -7 >> kotak
psxy kotak -J -R -W2,red -O -V >> %psfile%

#echo 1.5 12 70 7 TC Molluca Sea > Laut_maluku
#pstext Laut_maluku -J -R -O -F+f14,Times-BoldItalic,gray30 -K >> %psfile%


psconvert %psfile% -TG -A -P
call %name%.png