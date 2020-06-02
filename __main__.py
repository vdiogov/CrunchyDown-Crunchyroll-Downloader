import os
from selenium import webdriver
import sys
import re
import requests
import subprocess

def ArgvReader():
    try:
        argsuri = sys.argv.index("-url") + 1
        return sys.argv[argsuri]
    except ValueError:
        print("Erreur lors de la récupération de l'url")
        sys.exit()

def launchFirefox():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.crunchyroll.com/login")
    writelogs(driver)

def writelogs(driver):
    username = driver.find_element_by_id('login_form_name')
    username.send_keys('[login here]')
    password = driver.find_element_by_id('login_form_password')
    password.send_keys('[password here]')
    button = driver.find_element_by_id('login_submit_button')
    button.click()
    getM3U8(driver)

def getM3U8(driver):
    driver.get(ArgvReader())
    html = driver.page_source
    first_part = re.search(r'{"format":"adaptive_hls","audio_lang":"jaJP","hardsub_lang":null,"url":"+[^\s]+","resolution":"adaptive"},', html)
    second_part = (first_part.group(0).split("}"))
    url_m3u8 = (((second_part[0]).replace('{"format":"adaptive_hls","audio_lang":"jaJP","hardsub_lang":null,"url":"','')).replace('","resolution":"adaptive"','')).replace("\\/","/")
    driver.quit()
    downloader(url_m3u8)

def downloader(url_download):
    r = requests.get(url_download)
    fichier = open("master.m3u8", "a")
    fichier.write(r.text)
    fichier.close()
    ffmpeg("test.mp4")

def ffmpeg(output):
    command = "ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i master.m3u8 -c copy output.mp4"
    subprocess.call(command,shell=True)


launchFirefox()