


import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;


/**
 * Class for populating the necessary Data Structures 
 * @author prashanth
 *
 */
public class InputGenerator {
	
	/**
	 * Method that parsed the Input file and generated the Data Structures required to solve the problem
	 * @param file Input file
	 * @return List of SolverInputs
	 * @throws IOException When Input file cannot be found/opened
	 */
	public List<Input> getInput(String file) throws IOException
	{
		List<Input> solverInputList = new ArrayList<Input>();
		URL url = getClass().getResource(file);
		BufferedReader reader = new BufferedReader(new FileReader(url.getPath()));
		String currentLine = reader.readLine().trim();
		while(currentLine != null && !currentLine.equals(Constants.INPUT_TERMINATOR))
		{
			int roadCount = Integer.parseInt(currentLine);
			Graph g = new Graph();
			for(int roadIndex=0;roadIndex<roadCount;roadIndex++)
			{
				String roads[] = reader.readLine().trim().split(" ");
				Vertex v1 = new Vertex(roads[0].charAt(0));
				Vertex v2 = new Vertex(roads[1].charAt(0));
				g.addVertices(v1, v2);
			}
			String input[] = reader.readLine().trim().split(" ");
			int item = Integer.parseInt(input[0]);
			Input solverInput = new Input(g, new Character(input[1].charAt(0)),
					new Character(input[2].charAt(0)),item);
			
			solverInputList.add(solverInput);
			
			currentLine = reader.readLine().trim();
		}
		return solverInputList;
	}
}
