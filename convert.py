import json
import urllib.request
import sys
import re


def _main():
    if len(sys.argv) <= 1:
        print('Arguments not given.')
        sys.exit()
    else:
        val,unit = re.match(r'(\d+(?:\.*\d+){0,1})([a-zA-Z]+)', sys.argv[1]).groups()

    # table = json.loads(urllib.request.urlopen('https://www.gaitameonline.com/rateaj/getrate').read().decode('utf-8'))

    conv_url = 'http://fx.monegle.com/fx.php?rate={VAL}&q={UNIT}'.format(VAL=val,UNIT=unit.upper())

    print(re.search(r'<b>(.*(?:[\d,]+\.\d+\s*円).*)</b>', urllib.request.urlopen(conv_url).read().decode('utf-8')[4057:4500]).groups()[0])


if __name__ == '__main__':
    _main()
