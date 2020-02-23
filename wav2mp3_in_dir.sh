\find . -maxdepth 1 -name '*.wav' -exec lame --silent -b 192 -h '{}' \;
\find . -maxdepth 1 -name '*.wav' -exec rm {} \;
