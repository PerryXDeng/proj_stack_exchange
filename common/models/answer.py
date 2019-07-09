from common.models.post import Post

class Answer(Post):
    def __init__(self, post_id, site_post_id, dateCreated, score, title, body, ownerId, questionId):
        super().__init__(post_id, site_post_id, dateCreated, score, title, body, ownerId)
        self.questionId = questionId

    def __str__(self):
        return f"{str(super())[:-2]}, questionId: {self.questionId}"
