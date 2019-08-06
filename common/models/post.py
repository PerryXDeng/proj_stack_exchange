from xml.etree.ElementTree import Element
from typing import Dict, Union

class Post:

    def __init__(self, id: int, site_id: int, date_created: str, body):
        self.id = id
        self.site_id = site_id
        self.date_created = date_created
        self.body = body

    def __str__(self):
        return f'post {{ id: {self.id}, date: {self.date_created}'

    @staticmethod
    def parsePostXMLNode(node: Element, site_id: int):
        id = int(node.get("Id"))
        body = node.get("Body")
        date = node.get("CreationDate")
        return Post(id, site_id, date, body)

class Question(Post):
    def __init__(self, post_id, site_id, dateCreated, score, title, body, owner_id, acceptedId, tags):
        super().__init__(post_id, site_id, dateCreated, score, title, body, owner_id)
        self.acceptedId = acceptedId
        self.tags = tags

    def __str__(self):
        return f"{super().__str__()[:-2]}, questionId: {self.acceptedId}, tags: {', '.join(self.tags)}"

class Answer(Post):
    def __init__(self, post_id, site_post_id, dateCreated, score, title, body, ownerId, questionId):
        super().__init__(post_id, site_post_id, dateCreated, score, title, body, ownerId)
        self.questionId = questionId

    def __str__(self):
        return f"{super().__str__()[:-2]}, questionId: {self.questionId}"