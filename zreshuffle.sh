myopt=${1}

if [ -z $myopt ]
then
  myopt=off
fi

if [ $myopt = 'reset' ]
then
  echo 'making directories...'
  mkdir -p data
  mkdir -p data/data_final
  mkdir -p data/data_parsed
  mkdir -p data/data_raw
  mkdir -p parsing
  mkdir -p plotting
  mkdir -p stored_plots
  
  echo 'reshuffling files...'
  mv parsecolm.py parsing 2>/dev/null
  mv typedat.sh parsing 2>/dev/null
  mv xyplot.py plotting 2>/dev/null
  
  echo 'making symlinks...'
  cd parsing
  ln -sf ../data/* .
  cd ../plotting
  ln -sf ../data/data_final .
  ln -sf ../stored_plots .
  cd ..
elif [ $myopt = 'clear' ]
then
  echo 'making tarball for backup...'
  cd ..
  tar -zcf quick_plot_python.tar.gz quick_plot_python
  cd quick_plot_python
  
  echo 'reshuffling files...'
  mv parsing/parsecolm.py .
  mv parsing/typedat.sh .
  mv plotting/xyplot.py .
  
  echo 'deleting the fat...'
  command rm -rf data
  command rm -rf parsing
  command rm -rf plotting
  command rm -rf stored_plots
else
  echo 'read/understand this script first!'
  echo 'exiting...'
  exit 1
fi

echo 'FIN'
