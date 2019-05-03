from selenium import webdriver
import xml.etree.ElementTree as ET
import time
import sys
import subprocess as sp


apiurl1 = 'http://watch.live.nicovideo.jp/api/getplayerstatus/{}'
apiurl2 = 'https://ow.live.nicovideo.jp/api/getedgestatus?v={}'

def main():
    url = sys.argv[1]
    output_name = None
    if len(sys.argv) >= 3:
        output_name = sys.argv[2]

    passwd, mail_addr = get_niconico_login_info()

    br = webdriver.Chrome('chromedriver')
    try:
        br.implicitly_wait(6)
        br.set_page_load_timeout(15)

        # 遷移
        br.get(url)

        vid = url.split('/watch/')[-1]

        # タイムシフト視聴ボタン
        nico_live_page.start_timeshift(br)

        # ログイン処理
        nico_live_page.login(br, mail_addr, passwd)

        # タイムシフト視聴ボタン
        nico_live_page.start_timeshift_after_login(br)

        time.sleep(1)
        br.get(apiurl1.format(vid))
        api1text = br.find_element_by_tag_name('stream').get_attribute('outerHTML')

        time.sleep(1)
        br.get(apiurl2.format(vid))
        api2text = br.find_element_by_tag_name('rtmp').get_attribute('outerHTML')

        content_urls = get_info1(api1text)
        origin, ticket = get_infof2(api2text)
    finally:
        br.close()

    out_filename, fileext = format_output_name(output_name)
    for content_url in content_urls:
        download_with_rtmpdump(content_url, origin, ticket, out_filename)
        time.sleep(1)


class nico_live_page:
    @staticmethod
    def login(driver, mail_addr, passwd):
        driver.find_element_by_id(nico_live_page.mail_addr_id).send_keys(mail_addr)
        driver.find_element_by_id(nico_live_page.password_id).send_keys(passwd)
        driver.find_element_by_id(nico_live_page.login_id).click()

    @staticmethod
    def start_timeshift(driver):
        driver.find_element_by_id(nico_live_page.start_timeshift_id_before_login).click()
        driver.find_elements_by_xpath(nico_live_page.play_xpath)[0].click()

    @staticmethod
    def start_timeshift_after_login(driver):
        driver.find_elements_by_xpath(nico_live_page.start_timeshift_xpath_after_login)[0].click()

    start_timeshift_xpath_after_login = '//*[@id="comment_arealv319625154"]/div[1]/img'
    start_timeshift_id_before_login = 'timeshift_reservation'
    play_xpath = '/html/body/div[5]/div[2]/div/div[2]/a'
    mail_addr_id = 'input__mailtel'
    password_id = 'input__password'
    login_id = 'login__submit'


def get_niconico_login_info():
    ret = sp.run(['lpass','show','--password','secure.nicovideo.jp'], encoding='utf-8', capture_output=True)
    ret2 = sp.run(['lpass','show','--username','secure.nicovideo.jp'], encoding='utf-8', capture_output=True)
    if ret.returncode != 0 or ret2.returncode != 0:
        print(ret.stdout)
        print(ret.stderr)
        sys.exit(1)
    return ret.stdout.strip(), ret2.stdout.strip()


def get_info1(xmlstring):
    tree = ET.fromstring(xmlstring)
    ques = filter(lambda elm: 'publish' in elm.text and '/content/' in elm.text, list(tree.find('quesheet')))
    return list(map(lambda x: x.text.split()[-1], ques))


def get_infof2(xmlstring):
    tree = ET.fromstring(xmlstring)
    fileorigin = tree.find('url').text
    ticket = tree.find('ticket').text

    return (fileorigin, ticket)


def download_with_rtmpdump(content_url, origin, ticket, output_name = None):
    import datetime
    output_name = output_name + '_' + datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    cmd = f'rtmpdump -r {origin} -y mp4:{content_url} -C S:{ticket} -e -o {output_name}.flv'
    print('cmd: ', cmd)
    print(sp.getoutput(cmd))


def format_output_name(oname):
    if '.' not in oname:
        return (oname, 'flv')
    return '.'.join(oname.split('.')[:-1]), oname.split('.')[-1]


if __name__ == '__main__':
    main()
