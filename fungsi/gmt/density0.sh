#! /bin/sh
inc=10e

# gmt blockmean fungsi/gmt/sambaran.dat -I$inc -R127/128/0.4/1.4 -Sn -C -fg | gmt surface -R127/128/0.4/1.4 -I$inc -Gfungsi/gmt/rapat0.grd=sf -T0.25 -fg
gmt surface fungsi/gmt/sambaran.xyz -R127/128/0.4/1.4 -I$inc -Gfungsi/gmt/rapat0.grd=sf -T0.25 -fg
gmt grdmath fungsi/gmt/rapat0.grd 1 DIV = fungsi/gmt/rapat1.grd
gmt grdsample fungsi/gmt/rapat1.grd -I100e -Gfungsi/gmt/rapat2.grd -fg
gmt grdclip fungsi/gmt/rapat2.grd -Sb1/NaN -Gfungsi/gmt/rapat3.grd
gmt grdimage fungsi/gmt/rapat3.grd -JM16c -Ba0.5f0.25 -R127/128/0.4/1.4 -Q -Cfungsi/gmt/kerapatan.cpt -t30 -K  > fungsi/gmt/tes.ps
gmt psxy fungsi/gmt/sambaran.dat -Sc0.1 -G0 -R -J -O >> fungsi/gmt/tes.ps
gmt psconvert fungsi/gmt/tes.ps -Tg -A -P -E256
# rm -r static/mappetir/*density.png
