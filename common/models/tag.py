
class Tag:
    def __init__(self, id, count, name):
        self.id = id
        self.count = count
        self.name = name

    def __str__(self):
       return  f"tag: {{id : {self.id} , count : {self.count} , name : {self.name}}}"
    
    @staticmethod
    def parseTagXML(filename):
        pass
        # public
        # static
        # ArrayList < Tag > parseTagXML(String
        # filename){
        #     ArrayList < Tag > tags = new
        # ArrayList <> ();
        # NodeList
        # rows = XMLParserUtilities.getRows(filename);
        # for (int row = 0; row < rows.getLength(); row++){
        # Node current = rows.item(row);
        # if (current.getNodeType() == Node.ELEMENT_NODE){
        # Element tag = (Element) current;
        # tags.add(new Tag(
        # Integer.parseInt(tag.getAttribute("Id")),
        # Integer.parseInt(tag.getAttribute("Count")),
        # tag.getAttribute("TagName")
        # ));
        # }
        # }
        # return tags;
        # }