import Containers.*;

import java.util.ArrayList;

public class DBMain {

    static final String DATAPATH = "worldbuilding.meta.stackexchange.com\\";

    public static void main(String[] args){
       Site wordbuilding = new Site("worldbuilding");
       System.out.println(wordbuilding);
       ArrayList<User> users = User.parseUserXML(DATAPATH + "Users.xml");
       users.forEach(System.out::println);
       ArrayList<Tag> tags = Tag.parseTagXML(DATAPATH + "tags.xml");
       tags.forEach(System.out::println);
        ArrayList<Comment> comments = Comment.parseCommentXML(DATAPATH + "comments.xml");
        comments.forEach(System.out::println);
        ArrayList<Post> posts = Post.parsePostXML(DATAPATH + "posts.xml");
        posts.forEach(System.out::println);
    }


}
