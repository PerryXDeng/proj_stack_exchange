package Containers;

import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.util.ArrayList;

/**
 *   Simple container class for user info.
 *   Intermediary between xml and db
 */
public class User {
    private int id;
    private String dateCreated;
    private String userName;
    private int rep;

    public User(int id, String ts, String name, int rep){
        this.id =  id;
        this.dateCreated = ts;
        this.userName = name;
        this.rep = rep;
    }

    public int getId() {
        return id;
    }

    public String getDateCreated() {
        return dateCreated;
    }

    public int getRep() {
        return rep;
    }

    public String getUserName() {
        return userName;
    }

    @Override
    public String toString() {
        return String.format("user: {ID : %d , CreationDate : %s , DisplayName : %s , Reputation : %d}",
                id, dateCreated, userName, rep);
    }

    public static ArrayList<User> parseUserXML(String filename){
        ArrayList<User> users = new ArrayList<>();
        NodeList rows = XMLParserUtilities.getRows(filename);
        // because users.xml begins with a user that has ID = -1 (community), index starting at 1 to match with the ID col
        for(int row = 1; row < rows.getLength(); row++){
            Node current = rows.item(row);
            if(current.getNodeType() == Node.ELEMENT_NODE){
                Element user = (Element) current;
                users.add(new User(
                        Integer.parseInt(user.getAttribute("Id")),
                        user.getAttribute("CreationDate"),
                        user.getAttribute("DisplayName"),
                        Integer.parseInt(user.getAttribute("Reputation"))));
                }
            }
        return users;
    }
}
