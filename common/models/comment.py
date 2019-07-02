
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
    def parseCommentXML(filename):
        pass

    # ArrayList < Comment > comments = new
    # ArrayList <> ();
    # NodeList
    # rows = XMLParserUtilities.getRows(filename);
    # // because
    # users.xml
    # begins
    # with a user that has ID = -1 (community), index starting at 1 to match with the ID col
    # for (int row = 0; row < rows.getLength(); row++){
    # Node current = rows.item(row);
    # if (current.getNodeType() == Node.ELEMENT_NODE){
    # Element comment = (Element) current;
    # try {
    # comments.add(new Comment(
    # Integer.parseInt(comment.getAttribute("Id")),
    # Integer.parseInt(comment.getAttribute("Score")),
    # comment.getAttribute("Text"),
    # comment.getAttribute("CreationDate"),
    # Integer.parseInt(comment.getAttribute("UserId")),
    # Integer.parseInt(comment.getAttribute("PostId"))));
    # }catch(NumberFormatException nfe){
    # System.out.println("Error while parsing comment. No userId: " + row);
    # }
    #
    # }
    # }
    # return comments;