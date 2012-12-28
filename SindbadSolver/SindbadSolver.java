
/**
 * class for solving the Sindbad problem
 * @author prashanth
 *
 */

public class SindbadSolver {
	
	/**
	 * method that solves the Sindbad problem. It makes use of Dijkstra's Algorithm to find the shortest path
	 * @param source vertex from which journey will start 
	 * @param destination vertex where the items will be delivered
	 * @param items total number of items to be delivered at the destination
	 * @param costRule Rules that will be used to calculate the Toll fee
	 * @return number of items to start from destination so that desired number of items can be delivered at destination via shortest path
	 * @throws SindbadSolverException
	 */
	public int solve(Vertex source,Vertex destination,int items,ITollFeeRule costRule) throws SindbadSolverException
	{
		if(items < 0) throw new SindbadSolverException("Items count is less than 0");
		if(source == null) throw new SindbadSolverException("source is null");
		if(destination == null) throw new SindbadSolverException("destination is null");
		
		VertexMinHeap minheap = new VertexMinHeap();
		Vertex currentVertex = destination;
		currentVertex.setItems(items);
		while(!currentVertex.equals(source))
		{
			currentVertex.setVisited(true);
			for(Vertex v: currentVertex.getOutGoingVertices())
			{
				if(v.isVisited()) continue;
				int newItems = calculateItemsBeforeToll(v,currentVertex,costRule);
				if(v.getItems() == Constants.DEFAULT_COST)
				{
					v.setItems(newItems);
					minheap.add(v);
				}
				if(v.getItems() > newItems)
				{
					v.setItems(newItems);
					minheap.updateVertexCost(v);
				}
			}
			currentVertex = minheap.getRoot();
			
			if(currentVertex == null) throw new SindbadSolverException("Graph is Incorrectly formed or Invalid Inputs");
		}
		return currentVertex.getItems();
	}
	
	/**
	 * To calculate the number of items that should have been present before paying toll fee
	 * @param from From Vertex
	 * @param to To vertex
	 * @param costRule Rules to calculate the toll fee for village and town
	 * @return number of items that should have been present before paying toll fee
	 */
	private int calculateItemsBeforeToll(Vertex from, Vertex to,ITollFeeRule costRule)
	{
		if(from.isVillage()) 
			return costRule.calculateItemsBeforeTollForVillage(to.getItems());
		else
			return costRule.calculateItemsBeforeTollForTown(to.getItems());
	}
}
