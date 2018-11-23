file=${1}
lfrom=${2}
lto=${3}
prenum=${4}


prefix="  ${prenum}	"

for ((i=$lfrom; i<=$lto; i++))
do
  sed -i'.bak' "${i}s/^/$prefix/" $file
done
rm -f $file.bak
