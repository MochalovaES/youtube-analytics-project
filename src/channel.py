import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id  # id канала
        info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = info['items'][0]['snippet']['title']  # название канала
        self.description = info['items'][0]['snippet']['description']  # описание канала
        self.url = info['items'][0]['snippet']['thumbnails']['default']['url']  # ссылка на канал
        self.subscriber = info['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = info['items'][0]['statistics']['videoCount']  # количество видео
        self.view_count = info['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def __str__(self):
        """
        Метод, возвращающий название и ссылку на канал по шаблону <название_канала> (<ссылка_на_канал>)
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """
        Метод оператора сложения
        """
        return int(self.subscriber) + int(other.subscriber)

    def __sub__(self, other):
        """
        Метод оператора вычитания
        """
        return int(self.subscriber) - int(other.subscriber)

    def __gt__(self, other):
        """
        Определяет поведение оператора сравнения '>'
        """
        return int(self.subscriber) > int(other.subscriber)

    def __ge__(self, other):
        """
        Определяет поведение оператора сравнения '>='
        """
        return int(self.subscriber) >= int(other.subscriber)

    def __lt__(self, other):
        """
        Определяет поведение оператора сравнения '<'
        """
        return int(self.subscriber) < int(other.subscriber)

    def __le__(self, other):
        """
        Определяет поведение оператора сравнения '<='
        """
        return int(self.subscriber) <= int(other.subscriber)

    def __eq__(self, other):
        """
        Определяет поведение оператора сравнения '=='
        """
        return int(self.subscriber) == int(other.subscriber)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(info, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('youtube_API')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, file_name):
        """
        Метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = {'channel_id': self.channel_id, 'title': self.title, 'description': self.description, 'url': self.url,
                'subscriber': self.subscriber, 'video_count': self.video_count, 'view_count': self.view_count}
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile, indent=2, ensure_ascii=False)
