#! /bin/sh
REGION=126/128/0/2
SIZE="M17.38c"
gmt grdimage fungsi/gmt/map_pgr.nc -R$REGION -J$SIZE -Cfungsi/gmt/batimetri.cpt -V -I+a0+nt0.5 -Y8 -P > bat.ps
gmt psconvert bat.ps -TG -A -P -E256