import json
import os.path
import requests
from bs4 import BeautifulSoup

def get_data(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    project_data_list = []
    iteration_count = 3
    print(f"Всего итераций: #{iteration_count}")

    for item in range(1,4):
        req = requests.get(url + f"page={item}", headers)

        folder_name = f"data/data_{item}"

        if os.path.exists(folder_name):
            print("Папка уже существует!")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/project_{item}.html", "w", encoding="utf-8") as file:
            file.write(req.text)

        with open(f"{folder_name}/project_{item}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        articles = soup.find_all("div", class_="preview-box-platform")

        project_urls = []
        for article in articles:
            project_url = "https://theoryandpractice.ru" + article.find("a").get("href")
            project_urls.append(project_url)

        for project_url in project_urls:
            req = requests.get(project_url, headers)
            project_name = project_url.split("/")[-1]

            with open (f"{folder_name}/{project_name}.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            with open(f"{folder_name}/{project_name}.html", encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            project_data = soup.find("body", class_="backgrounded_page backgrounded_page-tnp")
            try:
                project_logo = project_data.find("div", class_="platform-info-card-imgwrapper").find("img").get("data-original")
            except Exception:
                project_logo = "Non project logo"

            try:
                project_name = project_data.find("div", class_="platform-header-left").find("h2").text
            except Exception:
                project_name = "Non project name"

            try:
                project_date = project_data.find("div", class_="platform-header-date platform-header-date-column").text
            except Exception:
                project_date = "Non project date"

            try:
                project_city = project_data.find("div", class_="platform-header-number tnp-city-or-online").text.strip()
            except Exception:
                project_city = "Non project city"

            try:
                project_price = project_data.find_all("div", class_="platform-header-number")[-1].text.strip()
                for i in project_price:
                    if i.isdigit():
                        final_project_price = project_price + "₽"
                    else:
                        final_project_price = project_price
            except Exception:
                project_price = final_project_price
                final_project_price = "Non project price"

            try:
                project_description = project_data.find("div", class_="platform-info-description platform-info-block platform-info-wrapper").find("div", class_="tnp-display-body").text.strip()
            except Exception:
                project_description = "Non project description"

            project_data_list.append(
                {
                    "Имя проекта": project_name.replace(" ", " "),
                    "URL логотипа проекта": project_logo,
                    "Дата проведения проекта": project_date,
                    "Город проведения проекта": project_city,
                    "Цена проекта": final_project_price,
                    "Описание проекта": project_description.replace("\n", " ").replace(" ", " ")
                }
            )

        iteration_count -= 1
        print(f"Итерация: #{item} завершена, осталось итераций: #{iteration_count}")
        if iteration_count == 0:
            print("Сбор данный завершен")

    with open("data/projects_data.json", "a", encoding="utf-8") as file:
        json.dump(project_data_list, file, indent=4, ensure_ascii=False)

def main():
    get_data("https://theoryandpractice.ru/courses?")

if __name__== "__main__":
    main()