from bs4 import BeautifulSoup
import requests
from os import path, mkdir
import random
from time import sleep

WAIT = 30

def main():
    page_link = 'https://www.azlyrics.com/w/west.html'
    page_response = requests.get(page_link, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    artist_name = "kanyewest"
    # mkdir("lyrics/" + artist_name)
    try:
        albumArea = soup.find(id="listAlbum")
        links = albumArea.find_all("a", href=True)
    except AttributeError:
        print("error!")
    for i in links[186:]:
        dirty = i['href']
        cleanedLink = dirty[2:]
        songName = path.basename(cleanedLink)[:-5]
        sleep(random.randint(0, WAIT))
        getNextPage(cleanedLink, songName, artist_name)
    print("Done!")
    

def getNextPage(link, songName, artist_name):
    baseLink = "https://www.azlyrics.com"
    path = baseLink + link
    site = requests.get(path)
    soup = BeautifulSoup(site.content, "html.parser")
    overallDiv = soup.find("div", class_="col-xs-12 col-lg-8 text-center")
    if type(overallDiv) is None:
        raise AttributeError
    div = overallDiv.find_all("div", recursive=False)
    lyrics = div[4].get_text()
    f = open("lyrics/" + artist_name + "/" + songName + ".txt", "a")
    try:
        f.write(lyrics)
    except UnicodeEncodeError as e:
        if '\x80' in lyrics:
            lyrics = lyrics.replace('\x80', '')
        elif '\u2032' in lyrics:
            lyrics = lyrics.replace('\u2032', '')
        elif '\u0101' in lyrics:
            lyrics = lyrics.replace('\u0101', '')
        elif '\u2015' in lyrics:
            lyrics = lyrics.replace('\u2015', '')
        else:
            character = (e.split('\''))[3]
            if character in lyrics:
                lyrics = lyrics.replace(character, '')
        f.write(lyrics)
    f.close()    
    print("Finished " + songName)

    
if __name__ == "__main__":
    main()