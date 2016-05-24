if [ -x "`which flac`" ]; then
  find . -type f -print0 | xargs -I{} -0 flac -8 -V --delete-input-file --replay-gain {}
else
  echo 'ERROR: flac not found'
fi
