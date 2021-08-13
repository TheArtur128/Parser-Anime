import requests
#import urllib.request
from bs4 import BeautifulSoup
import os

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
URL = "https://jut.su"
#Вводим адрес аниме с Jut.su
ANIME_URL = input("Enter the URL of the anime from Jut.su\n\> ")
#Очистка URL
if ANIME_URL[:5] == "https":
    ANIME_URL = "/" + ANIME_URL.split("/")[3]

if ANIME_URL[0] != "/":
    ANIME_URL = "/" + ANIME_URL

if ANIME_URL[-4:] == "html":
    ANIME_URL = "/" + ANIME_URL.split("/")[1]

print("")
#/gintamas - Примерно такое мы должны получить после очистки

#Получаем html страницу со всеми видива материаломи
html = requests.get(f"{URL}{ANIME_URL}", headers=HEADERS)
content = BeautifulSoup(html.content, "lxml")

#Оригинальное название аниме
ANIME_NAME = content.find("div", class_="under_video_additional the_hildi").text.split(".")[-1:][0][23:-24].replace(" ", "-")
name_exceptions = [":", "/", "*", "\"", "<", ">", "|", " "]
for i in range(len(name_exceptions)):
    ANIME_NAME = ANIME_NAME.replace(name_exceptions[i], "")

#Находим ссылки на все страницы серий и также фильмов
links_to_page = []
#Определяем класс первых серий
if content.find("div", class_="watch_l").find_all("a")[0].get("href")[:-4] == "html":
    video_class = " ".join(content.find("div", class_="watch_l").find("a").get("class"))
else:
    video_class = " ".join(content.find("div", class_="watch_l").find_all("a")[1].get("class"))

#Находим ссылки видео первого класса
block = content.find_all("a", class_=video_class)
for item in block:
    links_to_page.append(f"{URL}{item.get('href')}")

#Меняем класс
if video_class == "short-btn black video the_hildi":
    video_class = "short-btn green video the_hildi"
elif video_class == "short-btn green video the_hildi":
    video_class = "short-btn black video the_hildi"

#Находим ссылки видео второго класса
block = content.find_all("a", class_=video_class)
for item in block:
    links_to_page.append(f"{URL}{item.get('href')}")

#Офомляем красивые имена видеов
video_name = []
for i in range(len(links_to_page)):
    video_name.append(links_to_page[i][len(URL+ANIME_URL)+1:-5].replace("/", " "))

#Получаем ссылки на все видео
links_to_vidio = []
for i in range(len(links_to_page)):
    print(f"Parse {i + 1} video link...")
    #Подгоняем адресс под серию
    URL = links_to_page[i]
    html = requests.get(URL, headers=HEADERS)
    content = BeautifulSoup(html.content, "lxml")

    #Определяем конкретный блок видео
    block = content.find("div", class_="border_around_video no-top-right-border")
    if block is None:
        block = content.find("div", class_="border_around_video")

    #Останавливаемся если аниме запрещенно в России или его нет на сайте
    if i == 0 and block.find("source") is None:
        input(f"\nSorry, {ANIME_NAME} is not available in Russia :(\nEnter anything to exit > ")
        raise GeneratorExit ("WE DIDN'T FIND THIS ANIME")

    #Парсим ссылки
    links_to_vidio.append({video_name[i]: block.find("source").get("src")})
    #Завершение
    if i == len(links_to_page) - 1:
        print("finished!\n\n\n")

#Выводим все ссылки на все серии
for i in range(len(links_to_vidio)):
    print(links_to_vidio[i], "\n")

#Создаем католог с аниме
try:
    os.mkdir("Anime")
except FileExistsError: pass
#Создаем папку под конкретное Аниме
try:
    os.mkdir(f"Anime/{ANIME_NAME}")
except FileExistsError: pass

#Выбираем путь направления деятельности с уже напарсиными данными
#1. - Текст. файл с ссылками, 2. - Скачиваем видива (Пока не доступно)
your_way = int(input("\n1. - Copy all links to a text file\n2 - Download all series\n*Enter any key other than the above to exit*\n\> "))

#Добовляем в нашу папку текст. файл со всеми ссылками
if your_way == 1:
    with open(f"Anime/{ANIME_NAME}/{ANIME_NAME}.txt", "w") as file:
        for i in range(len(links_to_vidio)):
            file.write(f'{links_to_vidio[i]}\n')

#Добовляем видео
#if your_way == 2:
#    #Смотрим есть-ли уже скачиный контент
#    for i in range(len(video_name)):
#        if os.path.exists(f"Anime/{ANIME_NAME}/{ANIME_NAME}-{video_name[i]}.mp4"):
#            links_to_vidio.remove(links_to_vidio[i])
#            video_name.remove(video_name[i])
#
#    #Начинаем скачивание
#    for i in range(len(links_to_vidio)):
#        com = input(f"\nStart downloading file {ANIME_NAME}-{video_name[i]} ?\ny - yes, n - no\n\> ")
#        if com == "y" or com == "yes":
#            print(f"\nDownload {ANIME_NAME}-{video_name[i]}...")
#            video = requests.get(links_to_vidio[i][video_name[i]], allow_redirects=True)
#            with open(f"Anime/{ANIME_NAME}/{ANIME_NAME}-{video_name[i]}.mp4", "wb") as file:
#                file.write(video.content)
#            print("\nfinished!")
#        else:
#            break

print("\nfinished!")
