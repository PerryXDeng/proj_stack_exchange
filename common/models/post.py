from xml.etree.ElementTree import Element
from typing import Dict, Union

class Post:

    def __init__(self, id, site_id, date_created, score, title, body, owner_id):
        self.id = id
        self.site_id = site_id
        self.date_created = date_created
        self.score = score
        self.title = title
        self.body = body
        self.owner_id = owner_id

    def __str__(self):
        return f'post {{ id: {self.id}, date: {self.date_created}, score: {self.score}, title: {self.title}, ' \
            f'owner:{self.owner_id}'

    @staticmethod
    def parsePostXMLNode(node: Element, site_id: int):
        pass
        isQuestion = node.get("PostTypeId") == "1"

        id = int(node.get("Id"))
        score = int(node.get("Score"))
        title = node.get("Title")
        body = node.get("Body")
        date = node.get("CreationDate")

        ownerUserId = None if node.get("OwnerUserId") == None else int(node.get("OwnerUserId"))

        if isQuestion:
            acceptedId = None if node.get("AcceptedAnswerId") == None else int(node.get("AcceptedAnswerId"))
            tags = node.get("Tags").split("><")
            tags[0] = tags[0][1:]
            tags[-1] = tags[-1][:-1]
            return Question(id, site_id, date, score, title, body, ownerUserId, acceptedId, tags)
        else:
            questionId = None if node.get("ParentId") == None else int(node.get("ParentId"))
            return Answer(id, site_id, date, score, title, body, ownerUserId, questionId)

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