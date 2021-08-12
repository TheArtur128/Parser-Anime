import requests
from bs4 import BeautifulSoup
#import os

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
URL = "https://jut.su"
#Вводим адрес аниме с Jut.su
ANIME_URL = input("Enter the URL of the anime from Jut.su\n> ")
#Очистка URL если он был введен неправильно
if ANIME_URL[:15] == "https://jut.su/":
    ANIME_URL = "/" + ANIME_URL[15:]
if ANIME_URL[-1:] == "/":
    ANIME_URL = ANIME_URL[:-1]

print(ANIME_URL)

#Получаем html страницу со всеми видива материаломи
html = requests.get(f"{URL}{ANIME_URL}", headers=HEADERS)
content = BeautifulSoup(html.content, "lxml")

#Оформленное название аниме
ANIME_NAME = content.find("h1", class_="header_video allanimevideo anime_padding_for_title").text[9:-10] #header_video allanimevideo anime_padding_for_title

#Находим ссылки на все чёрные страницы серий
block = content.find_all("a", class_="short-btn black video the_hildi")
links_to_page = []
for item in block:
    links_to_page.append(f"{URL}{item.get('href')}")

#Находим ссылки на все зелёные страницы серий
block = content.find_all("a", class_="short-btn green video the_hildi")
for item in block:
    links_to_page.append(f"{URL}{item.get('href')}")

#Получаем ссылки на все видео
links_to_vidio = []
for i in range(len(links_to_page)):
    print(f"Parse {i + 1} series link...")
    #Подгоняем адресс под серию
    URL = links_to_page[i]
    html = requests.get(URL, headers=HEADERS)
    content = BeautifulSoup(html.content, "lxml")
    #Собираем нужный контент
    block = content.find("div", class_="border_around_video no-top-right-border")
    #Останавливаемся если аниме запрещенно в России или его нет на сайте
    if i == 0 and block.find("source") is None:
        input(f"\nSorry, {ANIME_URL[1:]} is not available in Russia :(\nEnter anything to exit > ")
        raise GeneratorExit ("WE DIDN'T FIND THIS ANIME")
    #Продолжаем собирать
    links_to_vidio.append({f"Series link {i + 1}": block.find("source").get("src")})
    if i == len(links_to_page) - 1:
        print("finished!\n\n\n")

#Выводим все ссылки на все серии
for i in range(len(links_to_vidio)):
    print(links_to_vidio[i], "\n")

#Выбираем путь направления деятельности с уже напарсиными данными
#1. - Текст. файл с ссылками, 2. - Скачиваем видива (Пока не доступно)
your_way = input("\n1. - Copy all links to a text file\n2 - Download all series (hard, hard and hard)\nEnter any key other than the above to exit\n> ")
if int(your_way) == 1:
    with open(f"{ANIME_NAME}.txt", "w") as file:
        for i in range(len(links_to_vidio)):
            file.write(f"{links_to_vidio[i]}\n")
        print("\nfinished!")
