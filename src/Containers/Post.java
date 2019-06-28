package Containers;

import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.util.ArrayList;

public class Post {

    public static String whitespace_chars =  ""       /* dummy empty string for homogeneity */
            + "\\u0009" // CHARACTER TABULATION
            + "\\u000A" // LINE FEED (LF)
            + "\\u000B" // LINE TABULATION
            + "\\u000C" // FORM FEED (FF)
            + "\\u000D" // CARRIAGE RETURN (CR)
            + "\\u0020" // SPACE
            + "\\u0085" // NEXT LINE (NEL)
            + "\\u00A0" // NO-BREAK SPACE
            + "\\u1680" // OGHAM SPACE MARK
            + "\\u180E" // MONGOLIAN VOWEL SEPARATOR
            + "\\u2000" // EN QUAD
            + "\\u2001" // EM QUAD
            + "\\u2002" // EN SPACE
            + "\\u2003" // EM SPACE
            + "\\u2004" // THREE-PER-EM SPACE
            + "\\u2005" // FOUR-PER-EM SPACE
            + "\\u2006" // SIX-PER-EM SPACE
            + "\\u2007" // FIGURE SPACE
            + "\\u2008" // PUNCTUATION SPACE
            + "\\u2009" // THIN SPACE
            + "\\u200A" // HAIR SPACE
            + "\\u2028" // LINE SEPARATOR
            + "\\u2029" // PARAGRAPH SEPARATOR
            + "\\u202F" // NARROW NO-BREAK SPACE
            + "\\u205F" // MEDIUM MATHEMATICAL SPACE
            + "\\u3000" // IDEOGRAPHIC SPACE
            ;


    protected int id;
    protected String dateCreated;
    protected int score;
    protected String title;
    protected String body;
    protected int ownerId;

    public Post(int id, String dateCreated, int score, String title, String body, int ownerId){
        this.id = id;
        this.dateCreated = dateCreated;
        this.score = score;
        this.title = title;
        this.body = body;
        this.ownerId = ownerId;
    }

    public int getId() {
        return id;
    }

    public int getOwnerId() {
        return ownerId;
    }

    public int getScore() {
        return score;
    }

    public String getBody() {
        return body;
    }

    public String getDateCreated() {
        return dateCreated;
    }

    public String getTitle() {
        return title;
    }

    @Override
    public String toString() {
        return String.format("post: {id : %d , date : %s , score : %d , title : %s , body : %s , owner : %d}",
                id, dateCreated, score, title, body, ownerId);
    }

    public static ArrayList<Post> parsePostXML(String filename){
        ArrayList<Post> posts = new ArrayList<>();
        NodeList rows = XMLParserUtilities.getRows(filename);
        for(int row = 0; row < rows.getLength(); row++){
            Node current = rows.item(row);
            if(current.getNodeType() == Node.ELEMENT_NODE){
                Element post = (Element) current;
                int id = Integer.parseInt(post.getAttribute("Id"));
                int score = Integer.parseInt(post.getAttribute("Score"));
                String title = post.getAttribute("Title");
                String body = post.getAttribute("Body");
                String date = post.getAttribute("CreationDate");
                int owner;
                try {
                    owner = Integer.parseInt(post.getAttribute("OwnerUserId"));
                }catch (NumberFormatException nfe){
                    //no owner. post has been deleted
                    owner = -1;
                }
                int type = Integer.parseInt(post.getAttribute("PostTypeId"));
                Post p;
                switch (type){
                    case 1:
                        int acceptedId;
                        try{
                            acceptedId = Integer.parseInt(post.getAttribute("AcceptedAnswerId"));
                        } catch (NumberFormatException nfe){
                            //if there is no acceptedID
                            acceptedId =  -1;
                        }
                        String tags = post.getAttribute("Tags");
                        //unsure of which chars are specific to the xml, so test on all of them
                        String[] formattedTags = tags.split(whitespace_chars);
                        posts.add(new Question(id, date, score, title, body, owner, acceptedId, formattedTags));
                        break;
                    case 2:
                        //answer
                        int questionId = Integer.parseInt(post.getAttribute("ParentId"));
                        posts.add(new Answer(id, date, score, title, body, owner, questionId));
                        break;
                    default:
                        System.out.println("Type of post not supported:  " + type);
                }

            }
        }
        return posts;
    }

}
