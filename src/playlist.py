import os
import datetime
import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('youtube_API')
youtube = build('youtube', 'v3', developerKey=api_key)

class PlayList():
    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.playlists = youtube.playlists().list(id=self.id_playlist,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.id_playlist,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list='+self.id_playlist


    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """

        total_time = datetime.timedelta(seconds=0)
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    def show_best_video(self):
        id_best_video = ''
        like_count_max = 0
        for likeCount in self.video_response['items']:
            if int(likeCount['statistics']['likeCount']) > like_count_max:
                like_count_max = int(likeCount['statistics']['likeCount'])
                id_best_video = likeCount['id']
        return f'https://youtu.be/'+ id_best_video







