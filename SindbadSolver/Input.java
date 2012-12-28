

/**
 * Input that will be read from the input file
 * @author prashanth
 *
 */
public class Input 
{
	private int items; // Number of items that has to be sent to destination , read from the input file.
	private Graph roadGraph; // Graph read from the Input file
	private Character source; // source read from the input file 
	private Character destination; // destination read from the input file
	
	public Input(Graph roadGraph, Character source, Character destination, int items)
	{
		this.items = items;
		this.roadGraph = roadGraph;
		this.source = source;
		this.destination = destination;
	}
	
	public int getItems() {
		return items;
	}
	
	public Character getSource() {
		return source;
	}
	
	public Graph getRoadGraph() {
		return roadGraph;
	}
	
	public Character getDestination() {
		return destination;
	}
	
}
