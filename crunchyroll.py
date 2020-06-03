import os
from selenium import webdriver
import sys
import re
import subprocess
import json
from unidecode import unidecode

tag_team = '[CrunchyDown] '

def launchFirefox():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.crunchyroll.com/login")
    writelogs(driver)

def writelogs(driver):
    username = driver.find_element_by_id('login_form_name')
    username.send_keys(getUsername(driver))
    password = driver.find_element_by_id('login_form_password')
    password.send_keys(getPassword(driver))
    button = driver.find_element_by_id('login_submit_button')
    button.click()
    getM3U8(driver)

def getM3U8(driver):
    driver.get(getURL())
    html = driver.page_source
    first_part = re.search(r'{"format":"adaptive_hls","audio_lang":"jaJP","hardsub_lang":null,"url":"+[^\s]+","resolution":"adaptive"},', html)
    second_part = (first_part.group(0).split("}"))
    url_m3u8 = (((second_part[0]).replace('{"format":"adaptive_hls","audio_lang":"jaJP","hardsub_lang":null,"url":"','')).replace('","resolution":"adaptive"','')).replace("\\/","/")
    ffmpeg(tag_team + filename(html, driver) + ".mp4", driver, url_m3u8)

def ffmpeg(output, driver, url):
    driver.quit()
    command = 'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -loglevel error -stats -i "{url_m3u8}" -c copy "{outputName}"'.format(outputName = output, url_m3u8 = url)
    subprocess.call(command,shell=True)

def getURL():
    try:
        if sys.argv.count("-url") == 1:
            argsuri = sys.argv.index("-url") + 1
            if "https://www.crunchyroll.com/" in sys.argv[argsuri]:
                return sys.argv[argsuri]
            else:
                print("Please enter a valid Crunchyroll link.")
                driver.quit()
                sys.exit()
        else:
            print("Please enter a link.")
            driver.quit()
            sys.exit()
    except ValueError:
        print("Error when fetching url.")
        driver.quit()
        sys.exit()

def getUsername(driver):
    try:
        if sys.argv.count("-u") == 1:
            argsusr = sys.argv.index("-u") + 1
            if sys.argv.count(sys.argv[argsusr]) != 0:
                return sys.argv[argsusr]
            else:
                print("Please enter a user.")
                driver.quit()
                sys.exit()
        else:
            print("Please enter a user.")
            driver.quit()
            sys.exit()
    except ValueError:
        print("Error when fetching username.")
        driver.quit()
        sys.exit()

def getPassword(driver):
    try:
        if sys.argv.count("-p") == 1:
            argspsr = sys.argv.index("-p") + 1
            if sys.argv.count(sys.argv[argspsr]) != 0:
                return sys.argv[argspsr]
            else:
                print("Please enter a password.")
                driver.quit()
                sys.exit()
        else:
            print("Please enter a password.")
            driver.quit()
            sys.exit()
    except ValueError:
        print("Error when fetching pasword.")
        driver.quit()
        sys.exit()

def filename(html, driver):
    jsonall = json.loads(re.findall(r'vilos\.config\.media = ({.*})', html)[0])
    if jsonall['metadata']['episode_number'] != '':
        number = (jsonall['metadata']['episode_number'])
        anime_name = driver.find_element_by_id('showmedia_about_episode_num').text
        return clean_text(anime_name + " - " + number)

def clean_text(text_):
    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - ', u'”': "''", '«': '((', '»': '))', '“': "''", '>': "}", '<':'{'}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], text_))

launchFirefox()