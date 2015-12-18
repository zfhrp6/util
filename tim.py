#!/usr/env/bin python
# coding: utf-8

import time


def tim():
  starttime = time.time()
  i = 0
  while 1:
    _now = time.time() - starttime
    now = int(_now)
    print('\r\t\t{} 時間 {} 分 {} 秒 {} '.format(now // 3600, str((now // 60) % 60).zfill(2), str(now % 60).zfill(2), str(i).zfill(2)), end='')
    time.sleep(0.01)
    if i < 99:
      i += 1
    else:
      i = 0

if __name__ == "__main__":
  print('\v' * 4)
  tim()

