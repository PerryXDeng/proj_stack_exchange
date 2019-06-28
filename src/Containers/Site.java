package Containers;

public class Site {
    private static int siteCount = 0;
    private int id;
    private String name;

    public Site(String name){
        id = ++siteCount;
        this.name =  name;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return String.format("site: {id : %d , name: %s}", id, name);
    }


}
