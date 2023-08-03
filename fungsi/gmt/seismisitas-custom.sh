#! /bin/sh

SIZE="M16c"
AXIS="a2f1/a2f1NWse"
psfile="fungsi/gmt/seismisitas_custom.ps"
gempa="fungsi/gmt/gempa_custom.txt"
dirasakan="fungsi/gmt/dirasakan_custom.txt"
REGION=125.5/127.5/-2.5/-1.0


#echo %evlon% %evlat% > %parameter%
gmt grdimage fungsi/gmt/map_pgr.nc -R$REGION -J$SIZE -Cfungsi/gmt/batimetri.cpt -Sn -Q -K -V -I+a0+nt0.5 -Y3.5 > $psfile
# gmt pscoast -Dh -R -J -W0.6,gray30 -K -O -V >> $psfile
gmt psxy -R -J -W1.5 -Sf0.4i/0.06ilt -Gblack -m -O -K fungsi/gmt/trench.gmt >> $psfile


awk '{print $1, $2, $3, $4*0.035}' $gempa | gmt psxy -J -R -Sci -Cfungsi/gmt/depth.cpt -W0.5 -O  -K -V >> $psfile
awk '{print $1, $2, $3}' $dirasakan | gmt psxy -J -R -Sa0.25i -Gred -W1 -O  -K -V >> $psfile

gmt psbasemap -J -R -B$AXIS -Lf124.7/3.1/0/100+lkm  --MAP_LABEL_OFFSET=0.1 --FONT_LABEL=17p,Heveltica --MAP_FRAME_TYPE=fancy --FONT_ANNOT=16p -K -O -V >> $psfile
gmt pstext -R -J -O -K -V <<EOF>> $psfile
129.9 2.8 45 90 34  BL \343
129.8 2.55 20 0 1 BR N
EOF



gmt psxy fungsi/gmt/kota-halmahera.txt -J -R -O -K -Sc0.06i -G0 >> $psfile
gmt psxy fungsi/gmt/kota-prop.txt -J -R -O -K -Ss0.08i -G0 >> $psfile
awk '{print $1-0.1, $2, TR, $4}' fungsi/gmt/kota-halmahera.txt | gmt pstext -J -R -F+f10,Times-Bold,black -O -K >> $psfile
awk '{print $1-0.15, $2+0.08, TL, $4}' fungsi/gmt/kota-prop.txt | gmt pstext -J -R -F+f12,Times-Bold,black -O -K >> $psfile

gmt pslegend fungsi/gmt/legenda_custom.txt -R -J -F+gwhite+p -Dx4.75i/0.25i/7.5i/0.95i/TC -C0.1i/0.1i -O -K -Y-1.5 -X-4 >> $psfile

gmt pscoast -Dl -R94/143/-12/12 -JM5 -Ba237wnse -Wthinnest -Swhite -Ggray40 -O -K -V -X14.9 -Y1.6 --MAP_FRAME_TYPE=plain  >> $psfile

gmt psxy -J -R -W3,red -O -V <<EOF>> $psfile
125.5 -1.0
127.5 -1.0
127.5 -2.5
125.5 -2.5
125.5 -1.0
EOF

gmt psconvert $psfile -Tj -A -P

#cp fungsi/gmt/seismisitas_mingguan.jpg static/seismisitas_mingguan.jpg