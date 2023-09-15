import os
from googleapiclient.discovery import build

api_key: str = os.getenv('youtube_API')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, id_video):
        self.id_video = id_video

        try:
            self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=self.id_video
                                                   ).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.url_video = self.video_response['items'][0]['snippet']
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url_video = None
            self.view_count = None
            self.like_count = None
    def __str__(self):
        """
        Метод, возвращающий название видео
        """
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.id_playlist,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

    def __str__(self):
        """
        Метод, возвращающий название видео
        """
        return f'{self.title}'
