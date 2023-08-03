#! /bin/sh

xmin=$1
xmax=$2
ymin=$3
ymax=$4
R=$xmin/$xmax/$ymin/$ymax
input=$5
fileinp="$input.xyz"
fileout="$input-densityclip.ps"

gmt surface $fileinp -R$R -I1m -Gfungsi/gmt/idw.grd=sf -T0.25 -fg
# gmt xyz2grd $fileinp -R$R -I1.01k -Gfungsi/gmt/idw.grd
gmt grdsample fungsi/gmt/idw.grd -I100e -Gfungsi/gmt/idw1.grd -fg
gmt grdmask fungsi/gmt/shpmalut_gab.gmt -Rfungsi/gmt/idw1.grd -NNaN/1/1 -Gfungsi/gmt/mask.nc
gmt grdmath fungsi/gmt/idw1.grd fungsi/gmt/mask.nc MUL = fungsi/gmt/malutclip.nc
gmt grdclip fungsi/gmt/malutclip.nc -Sb0.7/NaN -Gfungsi/gmt/idw2.grd
gmt grdinfo fungsi/gmt/idw2.grd -C > fungsi/gmt/info
