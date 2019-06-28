package Containers;

public class Question extends Post {

    private int acceptedId;
    private String[] tags;

    //posttype = 1
    public Question(int id, String dateCreated, int score, String title, String body, int ownerId, int acceptedId, String[] tags) {
        super(id, dateCreated, score, title, body, ownerId);
        this.acceptedId = acceptedId;
        this.tags = tags;
    }

    public int getAcceptedId() {
        return acceptedId;
    }

    public String[] getTags() {
        return tags;
    }

    @Override
    public String toString() {
        String superString =  super.toString();
        StringBuilder sb = new StringBuilder();
        for (String t : tags){
            sb.append(t);
            sb.append(", ");
        }
        return String.format("%s , acceptedId : %d , tags : %s}",
                superString.substring(0, superString.length() - 2), acceptedId,
                sb.toString().substring(0, sb.length() - 1));
    }
}
