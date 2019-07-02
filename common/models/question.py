from common.models.post import Post

class Answer(Post):
    def __init__(self, post_id, site_post_id, dateCreated, score, title, body, owner_id, acceptedId, tags):
        super().__init__(post_id, site_post_id, dateCreated, score, title, body, owner_id)
        self.acceptedId = acceptedId
        self.tags = tags

    def __str__(self):
        return f"{str(super())[:-2]}, questionId: {self.acceptedId}, tags: {', '.join(self.tags)}"
