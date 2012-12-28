


import java.util.PriorityQueue;

/**
 * MinHeap Implementation for Vertex of Graph
 * @author prashanth
 *
 */
public class VertexMinHeap {
	
	/**
	 * Min heap data structure
	 */
	private PriorityQueue<Vertex> vertexQueue = new PriorityQueue<Vertex>();
	
	/**
	 * adds a vertex to the min heap
	 * @param vertex vertex to be added
	 */
	public void add(Vertex vertex)
	{
		vertexQueue.add(vertex);
	}
	
	/**
	 * Gets the root of min heap which is the minimum element
	 * @return Vertex which has minimum number of items in the min heap
	 */
	public Vertex getRoot()
	{
		return vertexQueue.poll();
	}
	
	/**
	 * Updates the items of particular vertex in the heap (to heapify) 
	 * @param vertex vertex whose items has to be updated in the heap
	 */
	public void updateVertexCost(Vertex vertex)
	{
		vertexQueue.remove(vertex);
		add(vertex);
	}
}
