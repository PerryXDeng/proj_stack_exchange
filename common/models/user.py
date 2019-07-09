class User:
    def __init__(self, id, ts, name, rep):
        self.id = id
        self.ts = ts
        self.name = name
        self.rep = rep

    def __str__(self):
        return f"user: {{ID : {self.id} , CreationDate : {self.ts} , DisplayName : {self.name} , Reputation : {self.rep}}}"

    @staticmethod
    def parseUserXML(filename):
        pass
        # public
        # static
        # ArrayList < User > parseUserXML(String
        # filename){
        #     ArrayList < User > users = new
        # ArrayList <> ();
        # NodeList
        # rows = XMLParserUtilities.getRows(filename);
        # // because
        # users.xml
        # begins
        # with a user that has ID = -1 (community), index starting at 1 to match with the ID col
        # for (int row = 1; row < rows.getLength(); row++){
        # Node current = rows.item(row);
        # if (current.getNodeType() == Node.ELEMENT_NODE){
        # Element user = (Element) current;
        # users.add(new User(
        # Integer.parseInt(user.getAttribute("Id")),
        # user.getAttribute("CreationDate"),
        # user.getAttribute("DisplayName"),
        # Integer.parseInt(user.getAttribute("Reputation"))));
        # }
        # }
        # return users;
        # }