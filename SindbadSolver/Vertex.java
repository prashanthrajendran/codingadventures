


import java.util.ArrayList;
import java.util.List;

/**
 * Class that represents a vertex in the Graph
 * @author prashanth
 *
 */
public class Vertex implements Comparable<Vertex>{
	
	private char label;//name of the vertex
	private int items;// number of items in the vertex at the moment
	private boolean visited;//flag to indicate whether this vertex has been included in solution set
	private List<Vertex> outGoingVertices = new ArrayList<Vertex>();//List of outgoing vertices to this vertex
	
	public Vertex(char label)
	{
		this.label = label;
		this.items = Constants.DEFAULT_COST;
	}
	
	public char getLabel() {
		return label;
	}

	public void addOutGoingVertex(Vertex v)
	{
		outGoingVertices.add(v);
	}
	
	public List<Vertex> getOutGoingVertices()
	{
		return outGoingVertices;
	}
	
	public boolean isVisited() {
		return visited;
	}

	public void setVisited(boolean visited) {
		this.visited = visited;
	}
	
	public int getItems() {
		return items;
	}

	public void setItems(int items) {
		this.items = items;
	}

	public boolean isVillage()
	{
		return Character.isLowerCase(label);
	}
	
	@Override
	public int compareTo(Vertex o) {
		if(this.items > o.items) 
			return 1;
		else if(o.items > this.items)
			return -1;
		return 0;
	}
	
	@Override
	public boolean equals(Object obj)
	{
		if(obj == null) 
			return false;
		if(this == obj)
			return true;
		if(obj.getClass() != this.getClass())
			return false;
		Vertex v = (Vertex)obj;
		return this.label == v.label;
	}
	
	@Override
	public int hashCode()
	{
		return label;
	}
}
