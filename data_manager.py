import json
from classes.exceptions import DataSourceBrokenException

class DataManager:

    def __init__(self, path):
        self.path = path #Путь к файлу с данными


    def load_data(self):
        """Загружает все данные из json файла"""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise DataSourceBrokenException("Файл с данными поврежден")

        return data


    def save_data(self, data):
        """Перезаписывает данные в json файле"""
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


    def get_all(self):
        """Получаем полный список данных"""
        data = self.load_data()
        return data


    def search(self, substring):
        """Ищем посты, которые содержат substring"""
        matching_posts = []
        posts = self.load_data()

        for post in posts:
            content = post.get("content")
            if substring.lower() in content.lower():
                matching_posts.append(post)

        return matching_posts


    def add(self, post):
        """добавляем в хранилище пост"""
        if type(post) != dict:
            raise TypeError("Dict expected for adding post")
        posts = self.load_data()
        posts.append(post)
        self.save_data(posts)

