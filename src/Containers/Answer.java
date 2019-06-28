package Containers;

public class Answer extends Post{

    private int questionId;

    //posttype = 2
    public Answer(int id, String dateCreated, int score, String title, String body, int ownerId, int questionId) {
        super(id, dateCreated, score, title, body, ownerId);
        this.questionId = questionId;
    }

    public int getQuestionId() {
        return questionId;
    }

    @Override
    public String toString() {
        String superString =  super.toString();
        return String.format("%s , questionId : %d}",
                superString.substring(0, superString.length() - 2), questionId);
    }
}
