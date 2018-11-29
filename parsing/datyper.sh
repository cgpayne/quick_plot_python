file=${1}      # file name
lfrom=${2}     # line from
lto=${3}       # line to
prenum=${4}    # the number to insert before the line's content from $lfrom to $lto in $file


prefix="  ${prenum}	"

for ((i=$lfrom; i<=$lto; i++))
do
  sed -i'.bak' "${i}s/^/$prefix/" $file
done
rm -f $file.bak
