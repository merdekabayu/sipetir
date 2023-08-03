#! /bin/sh

xmin=$1
xmax=$2
ymin=$3
ymax=$4
R=$xmin/$xmax/$ymin/$ymax
input=$5
fileinp="$input.xyz"
fileout="$input-density.ps"

gmt surface $fileinp -R$R -I1m -Gfungsi/gmt/idw.grd=sf -T0.25 -fg
# gmt xyz2grd $fileinp -R$R -I1k -Gfungsi/gmt/idw.grd
gmt grdsample fungsi/gmt/idw.grd -I100e -Gfungsi/gmt/idw1.grd -fg
gmt grdclip fungsi/gmt/idw1.grd -Sb0.7/NaN -Gfungsi/gmt/idw2.grd
gmt grdinfo fungsi/gmt/idw2.grd -C > fungsi/gmt/info
# gmt psxy -J -R -W0.05,white -O -K fungsi/gmt/shpmalut_gab.gmt >> $fileout
# gmt psxy fungsi/gmt/kota_malut.dat -R -J -O -K -Sc0.05i -Wthin,0 -Gwhite >> $fileout
# awk '{ print $1+0.01,$2,$3-1.5,$4,$5,$6,$7}' fungsi/gmt/kota_malut.dat | gmt pstext -R -JM -Gyellow -O >> $fileout

