package Containers;

import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.util.ArrayList;

public class Tag {
    private int id;
    private int count;
    private String name;

    public Tag(int id, int count, String name){
        this.id = id;
        this.count = count;
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getCount() {
        return count;
    }

    @Override
    public String toString() {
        return String.format("tag: {id : %d , count : %d , name : %s}", id, count, name);
    }

    public static ArrayList<Tag> parseTagXML(String filename){
        ArrayList<Tag> tags = new ArrayList<>();
        NodeList rows = XMLParserUtilities.getRows(filename);
        for(int row = 0; row < rows.getLength(); row++){
            Node current = rows.item(row);
            if(current.getNodeType() == Node.ELEMENT_NODE){
                Element tag = (Element) current;
                tags.add(new Tag(
                        Integer.parseInt(tag.getAttribute("Id")),
                        Integer.parseInt(tag.getAttribute("Count")),
                        tag.getAttribute("TagName")
                ));
            }
        }
        return tags;
    }
}
