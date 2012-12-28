

import java.util.HashMap;

/**
 * class that will hold the entire graph
 * @author prashanth
 *
 */
public class Graph {
	/**
	 * Vertex will be hashed based on the label . so that it can retrieved in constant time.
	 */
	HashMap<Character, Vertex> vertexHolder = new HashMap<Character,Vertex>();
	
	public Vertex getVertex(Character vertextName)
	{
		return vertexHolder.get(vertextName);
	}
	
	/**
	 * method for adding the vertices to the graph
	 * @param v1 vertex1
	 * @param v2 vertex2
	 */
	public void addVertices(Vertex v1,Vertex v2)
	{
		addVertex(v1);
		addVertex(v2);
		setLink(vertexHolder.get(v1.getLabel()),vertexHolder.get(v2.getLabel()));
	}
	
	/**
	 * helper method for adding the vertex
	 * @param v1 vertex to be added
	 */
	private void addVertex(Vertex v1)
	{
		if(!vertexHolder.containsKey(v1.getLabel()))
			vertexHolder.put(v1.getLabel(),v1);
	}
	
	/**
	 * To add vertices as outgoing vertex of each other
	 * @param v1 vertex
	 * @param v2 outgoing vertex
	 */
	private void setLink(Vertex v1, Vertex v2)
	{
		v1.addOutGoingVertex(v2);
		v2.addOutGoingVertex(v1);
	}
}
