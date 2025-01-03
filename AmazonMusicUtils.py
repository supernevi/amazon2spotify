from typing import List

from selenium.webdriver.chromium.webdriver import ChromiumDriver

import config
import Progressbar
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

ChromeDriverManager().install()

class Song:
    def __init__(self, title : str, artist : str):
        self.Title = title
        self.Artist = artist
    def __repr__(self) -> str:
        return f"Song({self.Title=}, {self.Artist=})"

class Playlist:
    def __init__(self, name : str, song_list : List[Song]):
        self.name = name
        self.song_list = song_list

def start_chrome_browser() -> ChromiumDriver:
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.headless = True # does not work?!
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox") # linux only
    #chrome_options.add_argument("--headless=new") # must be set to off
    return webdriver.Chrome(options = chrome_options)

def get_playlist():
    driver = start_chrome_browser()
    wait = WebDriverWait(driver, 10)

    driver.get(config.playlist_url_amazon)

    wait.until(ec.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'content') and .//music-link[@title]]")))

    playlist_name_amazon = driver.title.split(" | ")[0]
    playlist_name = playlist_name_amazon  + " [Amazon]"

    print("Playlist '{}' found on Amazon".format(playlist_name_amazon))
    music_rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'content') and .//music-link[@title]]")

    songs = []
    for index, row in enumerate(music_rows):
        Progressbar.show_progress(step=index+1, total_steps=len(music_rows), title="Extracting songs from Amazon Music")
        new_song = create_song_item_by_music_row(row)
        if new_song is not None:
            songs.append(new_song)

    print("\nfound songs total: {}".format(len(songs)))
    driver.quit()
    return Playlist(playlist_name, songs)

def create_song_item_by_music_row(music_row : WebElement):
    song_title = music_row.find_element(By.XPATH, "div[@class='col1']//music-link[@title]").get_attribute("title")
    artist = music_row.find_element(By.XPATH, "div[@class='col2']//music-link[@title]").get_attribute("title")

    if song_title is not None and artist is not None:
        return Song(title = song_title, artist = artist)

    return None
