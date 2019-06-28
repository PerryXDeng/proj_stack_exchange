package Containers;

import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.util.ArrayList;

public class Comment {
    private int id;
    private int score;
    private String body;
    private String dateCreated;
    private int userid;
    private int postid;

    public Comment(int id, int score, String body, String dateCreated, int userid, int postid){
        this.id = id;
        this.score = score;
        this.body = body;
        this.dateCreated = dateCreated;
        this.userid = userid;
        this.postid = postid;
    }

    public String getDateCreated() {
        return dateCreated;
    }

    public int getScore() {
        return score;
    }

    public String getBody() {
        return body;
    }

    public int getId() {
        return id;
    }

    public int getPostid() {
        return postid;
    }

    public int getUserid() {
        return userid;
    }

    @Override
    public String toString() {
        return String.format("comment: {id: %d , score : %d , body : %s, date_created : %s , user : %d , post : %d}",
                id, score, body, dateCreated, userid, postid);
    }

    public static ArrayList<Comment> parseCommentXML(String filename){
        ArrayList<Comment> comments = new ArrayList<>();
        NodeList rows = XMLParserUtilities.getRows(filename);
        // because users.xml begins with a user that has ID = -1 (community), index starting at 1 to match with the ID col
        for(int row = 0; row < rows.getLength(); row++){
            Node current = rows.item(row);
            if(current.getNodeType() == Node.ELEMENT_NODE){
                Element comment = (Element) current;
                try {
                    comments.add(new Comment(
                            Integer.parseInt(comment.getAttribute("Id")),
                            Integer.parseInt(comment.getAttribute("Score")),
                            comment.getAttribute("Text"),
                            comment.getAttribute("CreationDate"),
                            Integer.parseInt(comment.getAttribute("UserId")),
                            Integer.parseInt(comment.getAttribute("PostId"))));
                }catch(NumberFormatException nfe){
                    System.out.println("Error while parsing comment. No userId: " + row);
                }

            }
        }
        return comments;
    }
}
