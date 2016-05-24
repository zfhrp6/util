find . -name '*.wav' -maxdepth 1 -exec lame -b 160 -h '{}' \;
find . -name '*.wav' -maxdepth 1 -exec rm {} \;
