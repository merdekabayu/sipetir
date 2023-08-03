#! /bin/sh

xmin=$1
xmax=$2
ymin=$3
ymax=$4
R=$xmin/$xmax/$ymin/$ymax
input=$5
fileinp="$input.xyz"
fileout="$input-clip-density.ps"

gmt surface $fileinp -R$R -I1m -Gfungsi/gmt/rapat0.grd=sf -T0.25 -fg
gmt grdsample fungsi/gmt/rapat0.grd -I100e -Gfungsi/gmt/ikl_cut.nc -fg
gmt grdmask fungsi/gmt/shpmalut_gab.gmt -Rfungsi/gmt/ikl_cut.nc -NNaN/1/1 -Gfungsi/gmt/mask.nc
gmt grdmath fungsi/gmt/ikl_cut.nc fungsi/gmt/mask.nc MUL = fungsi/gmt/malutclip.nc
gmt grdclip fungsi/gmt/malutclip.nc -Sb1/NaN -Gfungsi/gmt/malutclip2.nc
gmt grdimage fungsi/gmt/malutclip2.nc -JM16c -R$R -Q -Cfungsi/gmt/kerapatan.cpt -t30  > $fileout
gmt psconvert $fileout -TG -A -P -E256
gmt grdinfo fungsi/gmt/malutclip2.nc -C > fungsi/gmt/info
# rm -r static/mappetir/*density.png
cp -r $input-clip-density.png static/mappetir/
