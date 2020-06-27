import os
from selenium import webdriver
import sys
import re
import subprocess
import json
from unidecode import unidecode
import requests
import time
import glob

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
    if sys.argv.count("-url") == 1:
        getM3U8(driver)
    else:
        print("Please enter a link.")

def getM3U8(driver):
    driver.get(getURL(driver))
    html = driver.page_source

    if sys.argv.count("-subs") == 1:
        argssubs = sys.argv.index("-subs") + 1
        if sys.argv.count(sys.argv[argssubs]) != 0:
            subs(html, sys.argv[argssubs], driver)

    if sys.argv.count("-skipdownload") == 0:
        first_part = re.search(r'{"format":"adaptive_hls","audio_lang":"jaJP","hardsub_lang":null,"url":"+[^\s]+","resolution":"adaptive"},', html)
        second_part = (first_part.group(0).split("}"))
        url_m3u8 = (((second_part[0]).replace('{"format":"adaptive_hls","audio_lang":"jaJP","hardsub_lang":null,"url":"','')).replace('","resolution":"adaptive"','')).replace("\\/","/")
        name = filename(html, driver)
        downloader(tag_team + name + ".mp4", driver, url_m3u8, name)

def downloader(output, driver, url, name):
    driver.quit()

    ass = ""
    for file in glob.glob(name + "/*.ass"):
        ass = ass + '"' + file + ' " '

    print(ass)

    command = 'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -loglevel error -stats -i "{url_m3u8}" -c copy "{outputName}"'.format(outputName=output, url_m3u8=url)
    subprocess.call(command, shell=True)

    command2 = 'mkvmerge -o "{tag}{namerelease}.mkv" "{outputName}" {subs}'.format(outputName=output, namerelease=name, tag=tag_team, subs=ass)
    subprocess.call(command2, shell=True)

def getURL(driver):
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

def subs(html, need, driver):
    jsonall = json.loads(re.findall(r'vilos\.config\.media = ({.*})', html)[0])
    print("Downloading subtitles:   ", end="", flush=True)
    nom = filename(html, driver)
    os.mkdir(nom)
    if need == "all":
        for i in jsonall['subtitles']:
            print(i["language"] + " ", end="", flush=True)
            r = requests.get(i["url"], allow_redirects=True)
            r.encoding = r.apparent_encoding
            NomFichier = (tag_team + " " + nom + "." + i["language"] + ".ass")
            Fichier = open(nom + "/" + NomFichier, 'wb')
            Fichier.write((r.text).encode('UTF8'))
            Fichier.close()
    else:
        for i in jsonall['subtitles']:
            if i["language"] == need:
                print(i["language"] + " ", end="", flush=True)
                r = requests.get(i["url"], allow_redirects=True)
                r.encoding = r.apparent_encoding
                NomFichier = (tag_team + " " + nom + "." + i["language"] + ".ass")
                Fichier = open(nom + "/" + NomFichier, 'wb')
                Fichier.write((r.text).encode('UTF8'))
                Fichier.close()

def clean_text(text_):
    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - ', u'”': "''", '«': '((', '»': '))', '“': "''", '>': "}", '<':'{'}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], text_))

launchFirefox()