from __future__ import annotations
from xml.etree.ElementTree import Element

class Comment:
    def __init__(self, id, body, date_created, score, user_id, post_id):
        self.id = id
        self.body = body
        self.date_created = date_created
        self.score = score
        self.user_id = user_id
        self.post_id = post_id

    def __str__(self):
        return f"comment: {{id: {self.id} , score : {self.score} , body : {self.body}, " \
            f"date_created : {self.date_created} , user : {self.user_id} , post : {self.post_id}}}"

    @staticmethod
    def parseCommentXMLNode(node: Element):
        return Comment(node.get("Id"),
                       node.get("Text"),
                       node.get("CreationDate"),
                       int(node.get("Score")),
                       -1 if node.get("UserId") is None else int(node.get("UserId")),
                       int(node.get("PostId")))