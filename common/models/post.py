
class Post:

    def __init__(self, post_id, site_post_id, date_created, score, title, body, owner_id):
        self.post_id = post_id
        self.site_post_id = site_post_id
        self.date_created = date_created
        self.score = score
        self.title = title
        self.body = body
        self.owner_id = owner_id

    def __str__(self):
        return f'post {{ id: {self.id}, date: {self.date_created}, score: {self.score}, title: {self.title}, ' \
            f'owner:{self.owner_id}'

    @staticmethod
    def parsePostXML(filename):
        pass
    #     ArrayList < Post > posts = new
    #     ArrayList <> ();
    #     NodeList
    #     rows = XMLParserUtilities.getRows(filename);
    #     for (int row = 0; row < rows.getLength(); row++){
    #     Node current = rows.item(row);
    #     if (current.getNodeType() == Node.ELEMENT_NODE){
    #     Element post = (Element) current;
    #     int id = Integer.parseInt(post.getAttribute("Id"));
    #     int score = Integer.parseInt(post.getAttribute("Score"));
    #     String title = post.getAttribute("Title");
    #     String body = post.getAttribute("Body");
    #     String date = post.getAttribute("CreationDate");
    #     int owner;
    #     try {
    #     owner = Integer.parseInt(post.getAttribute("OwnerUserId"));
    #     }catch (NumberFormatException nfe){
    #     // no owner.post has been deleted
    #     owner = -1;
    #     }
    #     int
    #     type = Integer.parseInt(post.getAttribute("PostTypeId"));
    #     Post
    #     p;
    #     switch(type)
    #     {
    #         case
    #     1:
    #     int
    #     acceptedId;
    #     try{
    #     acceptedId = Integer.parseInt(post.getAttribute("AcceptedAnswerId"));
    #     } catch (NumberFormatException nfe){
    #     // if there is no acceptedID
    #     acceptedId =  -1;
    #     }
    #     String
    #     tags = post.getAttribute("Tags");
    #     // unsure
    #     of
    #     which
    #     chars
    #     are
    #     specific
    #     to
    #     the
    #     xml, so
    #     test
    #     on
    #     all
    #     of
    #     them
    #     String[]
    #     formattedTags = tags.split(whitespace_chars);
    #     posts.add(new
    #     Question(id, date, score, title, body, owner, acceptedId, formattedTags));
    #     break;
    #
    #
    # case
    # 2:
    # // answer
    # int
    # questionId = Integer.parseInt(post.getAttribute("ParentId"));
    # posts.add(new
    # Answer(id, date, score, title, body, owner, questionId));
    # break;
    # default:
    # System.out.println("Type of post not supported:  " + type);
    # }
    #
    # }
    # }
    # return posts;