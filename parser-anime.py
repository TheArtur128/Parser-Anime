import requests
from bs4 import BeautifulSoup
import os

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
URL = "https://jut.su"
#Вводим адрес аниме с Jut.su
try:
    ANIME_URL = input("Enter the URL of the anime from Jut.su\n\> ")
#Ловим ошибку если ввели несуществующий URL
except AttributeError:
    input("You entered the URL incorrectly, please try to enter /anime-name\nEnter anything to exit > ")
    raise GeneratorExit ("WE DIDN'T FIND THIS ANIME")

#Очистка URL
if ANIME_URL[:5] == "https":
    ANIME_URL = "/" + ANIME_URL.split("/")[3]

elif ANIME_URL[:6] == "jut.su":
    ANIME_URL = "/" + ANIME_URL.split("/")[1]

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

#Определяем разрешение спарсиных видео. При quick_parsing будет парсить в 480p
if input("Parse to FullHD ?\ny - yes, every button - no\n\> ").replace(" ", "").lower() in ["y", "yes"]:
    quick_parsing = False
    file_name = f"Anime-catalog/{ANIME_NAME}-1080p.txt"
else:
    quick_parsing = True
    file_name = f"Anime-catalog/{ANIME_NAME}-480p.txt"
print("")

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
    if i == 0:
        if block.find("source") is None:
            input(f"\nSorry, {ANIME_NAME} is not available in Russia :(\nEnter anything to exit > ")
            raise GeneratorExit ("WE DIDN'T FIND THIS ANIME")
            pass

    #Находим ссылку
    if not quick_parsing:
        video_resolution = block.find("source").get("src")
    elif quick_parsing:
        video_resolution = block.find("source", res="480").get("src")

    #Запихиваем найденую ссылку в общий тер. лист
    links_to_vidio.append({video_name[i]: video_resolution})

    #Завершение
    if i == len(links_to_page) - 1:
        print("finished!\n")

#Выводим все ссылки на все серии
for i in range(len(links_to_vidio)):
    print("\n", links_to_vidio[i])

#Создаем католог с аниме
try:
    os.mkdir("Anime-catalog")
except FileExistsError: pass

#Добовляем в нашу папку текст. файл со всеми ссылками
with open(file_name, "w") as file:
    for i in range(len(links_to_vidio)):
        file.write(f"{links_to_vidio[i]}\n")

print("\nfinished!")

input("Enter anything to exit > ")
