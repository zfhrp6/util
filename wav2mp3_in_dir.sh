find . -name '*.wav' -maxdepth 1 -exec lame --silent -b 192 -h '{}' \;
find . -name '*.wav' -maxdepth 1 -exec rm {} \;
