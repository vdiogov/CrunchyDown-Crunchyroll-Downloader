# CrunchyDown - Crunchyroll-Downloader
> This project is about creating a Crunchyroll Downloader with ideas from the community.

## Dependencies:
> ['os', 'selenium', 'sys', 're', 'subprocess', 'json', 'unidecode', 'requests', 'glob']

## Features of V1.2:
* Connection System  
* m3u8 capture  
* HLS Downloader  
* Team tag management
* Subtitles Downloader
* Mux Video with Subtitles

## Necessary bin :
* [geckodriver.exe](https://github.com/mozilla/geckodriver/releases)  
* [ffmpeg.exe](https://ffmpeg.org/)  
* [Firefox](https://www.mozilla.org/)
* [mkvmerge](https://anonfiles.com/Dcx5P9C3oa/mkvmerge_exe)

## Path:
![path](https://imgur.com/AaAy9G0.png)

## View sample request:

`py crunchyroll.py -url https://www.crunchyroll.com/princess-connect-re-dive/episode-9-a-gourmet-getaway-fragrant-tentacles-on-the-beach-794695 -u "[IDENTIFIANT_HERE]" -p "[PASSWORD_HERE]"` - Download only video

`py crunchyroll.py -url https://www.crunchyroll.com/princess-connect-re-dive/episode-9-a-gourmet-getaway-fragrant-tentacles-on-the-beach-794695 -u "[IDENTIFIANT_HERE]" -p "[PASSWORD_HERE]" -subs all` - Download video with all available subtitles

`py crunchyroll.py -url https://www.crunchyroll.com/princess-connect-re-dive/episode-9-a-gourmet-getaway-fragrant-tentacles-on-the-beach-794695 -u "[IDENTIFIANT_HERE]" -p "[PASSWORD_HERE]" -subs frFR` - Download video with French subtitles

`py crunchyroll.py -url https://www.crunchyroll.com/princess-connect-re-dive/episode-9-a-gourmet-getaway-fragrant-tentacles-on-the-beach-794695 -u "[IDENTIFIANT_HERE]" -p "[PASSWORD_HERE]" -skipdownload -subs frFR` - Download only French subtitles
