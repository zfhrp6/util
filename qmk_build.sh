echo "target: ${1:-default}";
docker run -e keymap=${1:-default} \
  -e subproject=ez \
  -e keyboard=ergodox \
  --rm -v $('pwd'):/qmk:rw \
  edasque/qmk_firmware ;
