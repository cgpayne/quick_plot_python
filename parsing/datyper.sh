file=181029_ar40_both.dat
prefix='  0	'
lfrom=3
lto=73

for ((i=$lfrom; i<=$lto; i++))
do
  sed -i'.bak' "${i}s/^/$prefix/" $file
done
rm -f $file.bak
