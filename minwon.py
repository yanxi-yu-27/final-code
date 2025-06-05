from datetime import date

class Minwon:
    def __init__(self, author: str, content: str, latitude: float, longitude: float, created_date: date):
        self.author = author
        self.content = content
        self.latitude = latitude
        self.longitude = longitude
        self.created_date = created_date

    def __str__(self):
        return f"작성자: {self.author}, 내용: {self.content}, 좌표: ({self.latitude}, {self.longitude}), 날짜: {self.created_date}"
    
    def to_list(self):
        return [self.author, self.content, self.latitude, self.longitude, str(self.created_date)]
