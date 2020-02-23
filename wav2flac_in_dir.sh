XARGS=xargs
if type parallel >/dev/null 2>&1; then
  XARGS=parallel
fi

if [ -x "`which flac`" ]; then
  \find . -name "*.wav" -type f -print0 | $XARGS -I{} -0 flac -8 -V --silent --delete-input-file --replay-gain {}
else
  echo 'ERROR: flac not found'
fi
