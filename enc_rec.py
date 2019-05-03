import os
# import time
import subprocess as sp
import re
import multiprocessing
# import threading


def sun(s):
    ret = ''
    for c in s:
        if c in ' \'\"()&!@?$':
            ret += '\\'
        ret += c
    return ret


def conv(fpath):
    print(fpath)
    sp.getoutput('opusenc --quiet --bitrate 128 {} {}'.format(fpath, fpath.replace('.flac', '.opus')))


def metaconv(fpaths):
    # ths = []
    for fpath in fpaths:
        conv(fpath)
    #     try:
    #         time.sleep(0)
    #         thread = threading.Thread(target=conv, args=(fpath,))
    #         ths.append(thread)
    #         thread.start()
    #     except BlockingIOError as e:
    #         time.sleep(5)
    # [th.join() for th in ths]


def main():
    targets = [[], [], []]
    cnt = 0
    for dn, ds, fs in os.walk(os.getcwd()):
        for f in fs:
            fpath = sun(dn + '/' + f)
            # print(fpath)
            if re.search('\.flac$', fpath):
                if cnt % 3 == 1:
                    targets[1].append(fpath)
                elif cnt % 3 == 2:
                    targets[2].append(fpath)
                else:
                    targets[0].append(fpath)
                cnt += 1
    jobs = []
    job0 = multiprocessing.Process(target=metaconv, args=(targets[0],))
    jobs.append(job0)
    job0.start()
    job1 = multiprocessing.Process(target=metaconv, args=(targets[1],))
    jobs.append(job1)
    job1.start()
    job2 = multiprocessing.Process(target=metaconv, args=(targets[2],))
    jobs.append(job2)
    job2.start()
    [job.join() for job in jobs]


main()
