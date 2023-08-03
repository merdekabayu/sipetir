#! /bin/sh

fin=fungsi/gmt/sambaran.dat
fout=fungsi/gmt/sumwilayah.dat

awk -F' ' '{print $1" "$2" "$5" "0}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tte_selatan.gmt > $fout
awk -F' ' '{print $1" "$2" "$5" "1}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tte_tengah.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "2}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tte_utara.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "3}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/pulau_tte.gmt >> $fout

awk -F' ' '{print $1" "$2" "$5" "4}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tdr_tdr.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "5}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tdr_tdr_selatan.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "6}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tdr_tdr_utara.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "7}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tdr_tdr_timur.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "8}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/tdr_oba_utara.gmt >> $fout

awk -F' ' '{print $1" "$2" "$5" "9}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/halbar_jailolo_selatan.gmt >> $fout
awk -F' ' '{print $1" "$2" "$5" "10}' $fin | gmt gmtselect -Ffungsi/gmt/gmtkec/halbar_jailolo.gmt >> $fout
