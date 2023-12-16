import requests
import os
import telegram
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup 


def find_headline_text_coopland(coopland_content_blok):
        headline_text_coopland = coopland_content_blok.find('h2',class_='title').text
        return headline_text_coopland

def find_subtitle_text(article_content_blok):
    subtitle_text = article_content_blok.find("div", class_="preview-text").text
    return subtitle_text

def get_link_coopland(article_content_blok):
    link_coopland = article_content_blok.find('a')["href"]
    return link_coopland

def get_photo_coopland(soup_coopland):
        image_blok_coopland = soup_coopland.find("div", class_="image")
        a = image_blok_coopland.find('a', class_="img")
        url_img_coopland = 'https://coop-land.ru'+ a.find("img").get('data-src')
        response_coopland_img = requests.get(url_img_coopland)
        with open('picture.jpeg', "wb") as file:
            file = file.write(response_coopland_img.content)


def get_link_igromania(soup_igromania):
        link_igromania = soup_igromania.find('a', class_='style_body__ldkAO')['href']
        link_igromania = 'https://www.igromania.ru' + link_igromania
        return link_igromania

def get_photo_igromania(soup_igromania):
        image_blok_igromania = soup_igromania.find("figure", class_="knb-card--mask-tiny")
        url_img_igromania = image_blok_igromania.find('img', class_="knb-card--image").get('src')
        response_igramania_img = requests.get(url_img_igromania)
        with open('img_igromania.jpeg', "wb") as file:
            file = file.write(response_igramania_img.content)

def find_headline_text_igromania(soup_igromania):
        headline_text_igromania = soup_igromania.find('div',class_='style_desc__9c7ec knb-card--title style_title__uxa72').find('span').text
        return headline_text_igromania


if __name__ == "__main__":

    load_dotenv()

    tg_token = os.getenv('A')
    bot = telegram.Bot(token = tg_token)
    TELEGRAM_CHAT_ID = '6541125634'

    url_coopland = 'https://coop-land.ru/helpguides/new/'
    url_igromania = 'https://www.igromania.ru/reviews/'

    response_coopland_url = requests.get(url_coopland)
    soup_coopland = BeautifulSoup(response_coopland_url.text,"lxml")  
    coopland_content_blok_satrt = soup_coopland.find('div', class_='article-content')
    
    response_igromania_url = requests.get(url_igromania)
    soup_igromania_start = BeautifulSoup(response_igromania_url.text, "lxml")
    headline_text_igromania_start = find_headline_text_igromania(soup_igromania_start)
    
    while True:
        response_coopland_url = requests.get(url_coopland)
        soup_coopland = BeautifulSoup(response_coopland_url.text,"lxml")
        coopland_content_blok = soup_coopland.find('div', class_='article-content')

        response_igromania_url = requests.get(url_igromania)
        soup_igromania = BeautifulSoup(response_igromania_url.text, "lxml")
        headline_text_igromania = find_headline_text_igromania(soup_igromania)

        
        get_photo_coopland(soup_coopland)
        get_photo_igromania(soup_igromania)

        text_coopland = f'{find_headline_text_coopland(coopland_content_blok)}{find_subtitle_text(coopland_content_blok)}Ссылка на источник:{get_link_coopland(coopland_content_blok)}'
        text_igromania = f'{find_headline_text_igromania(soup_igromania)}\nСсылка на обзор: {get_link_igromania(soup_igromania)}'

        if coopland_content_blok != coopland_content_blok_satrt:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open('picture.jpeg', 'rb'),caption = text_coopland )
            coopland_content_blok_satrt = coopland_content_blok
        elif headline_text_igromania != headline_text_igromania_start:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open('img_igromania.jpeg', 'rb'),caption = text_igromania ) 
            headline_text_igromania_start = headline_text_igromania
        else:
            print('Ожидание новых постов \u001b[1A')
            
        time.sleep(0.5)