#! /bin/sh

xmin=$1
xmax=$2
ymin=$3
ymax=$4
R=$xmin/$xmax/$ymin/$ymax
input=$5
fileinp="$input.xyz"
fileout="$input-density.ps"

gmt surface $fileinp -R$R -I1m -Gfungsi/gmt/rapat01.grd=sf -T0.25 -fg
gmt grdsample fungsi/gmt/rapat01.grd -I100e -Gfungsi/gmt/ikl_cut1.nc -fg
gmt grdclip fungsi/gmt/ikl_cut1.nc -Sb1/NaN -Gfungsi/gmt/malutclip3.nc
gmt grdimage fungsi/gmt/malutclip3.nc -JM16c -R$R -Q -Cfungsi/gmt/kerapatan.cpt -t30  > $fileout
gmt psconvert $fileout -TG -A -P -E256
gmt grdinfo fungsi/gmt/malutclip3.nc -C > fungsi/gmt/info
# rm -r static/mappetir/*density.png
cp -r $input-density.png static/mappetir/
