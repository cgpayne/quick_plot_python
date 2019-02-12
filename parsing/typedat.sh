file=${1}      # file name
lfrom=${2}     # line from
lto=${3}       # line to
prenum=${4}    # the number to insert before the line's content from $lfrom to $lto in $file

prefix="  ${prenum}	"
sed -i'.bak' "${lfrom},${lto}s/^/$prefix/" $file; rm -f $file.bak
less +$(($lfrom-1)) $file
