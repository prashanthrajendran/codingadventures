


import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;


/**
 * Entry class for the program 
 * @author prashanth
 *
 */
public class SolverLauncher 
{
	/**
	 * Entry function
	 * @param args
	 */
	public static void main(String[] args) 
	{
		new SolverLauncher().coordinate();
	}
	
	/**
	 * co-ordinates work between various methods to generate the output
	 */
	private void coordinate()
	{
		try
		{
			InputGenerator inputGenerator = new InputGenerator();
			List<Input> solverInputList = new ArrayList<Input>();
			try
			{
				solverInputList = inputGenerator.getInput(Constants.INPUT_FILE);
			}
			catch(IOException ioEx)
			{
				System.out.println(appendString("Error while parsing the input :",ioEx.getMessage()));
				System.exit(0);
			}
			solveAll(solverInputList);
		}
		catch(Exception ex)
		{
			System.out.println(appendString("Unexpected error occured :",ex.getMessage()));
		}
	}
	
	/**
	 * calls the SindbadSolver and solves all the Input read from the Input file
	 * @param solverInputList List of Inputs read from the Input file
	 */
	private void solveAll(List<Input> solverInputList)
	{
		SindbadSolver solver = new SindbadSolver();
		int caseCount = 0;
		ITollFeeRule tollRule = getTollRule();
		BufferedWriter writer = null;
		try
		{
			File file = new File(Constants.OUTPUT_FILE);
			writer = new BufferedWriter(new FileWriter(file));
			for(Input input : solverInputList)
			{
				caseCount++;
				String result = null;
				StringBuilder resultBuilder = getCaseStringBuilder(caseCount);
				try
				{
					int totalItems = solver.solve(input.getRoadGraph().getVertex(input.getSource()), 
							input.getRoadGraph().getVertex(input.getDestination()), input.getItems(), tollRule);
					result = resultBuilder.append(String.valueOf(totalItems)).toString();
				}
				catch(SindbadSolverException sEx)
				{
					result = resultBuilder.append(sEx.getMessage()).toString();
				}
				writer.write(result);
				writer.newLine();
			}
		}
		catch(IOException ioEx)
		{
			System.out.println(appendString("Error while writing output :",ioEx.getMessage()));
			System.exit(0);
		}
		finally
		{
			if(writer!= null)
			{
				try
				{
					writer.close();
					java.awt.Desktop.getDesktop().edit(new File(Constants.OUTPUT_FILE));
				}
				catch(IOException ioEx)
				{
					System.out.println(appendString("Error while trying to close output file :",ioEx.getMessage()));
				}
			}
		}
	}
	
	/**
	 * Reads the properties file and instantiates an Implementation for ITollFeeRule  
	 * @return Implementation of ITollFeeRule
	 */
	private ITollFeeRule getTollRule()
	{
		Properties prop = new Properties();
		ITollFeeRule tollRule;
		try
		{
			prop.load(new FileInputStream(getClass().getResource(Constants.PROPERTIESFILE).getPath()));
			tollRule = new TollFeeRule(Double.parseDouble(prop.getProperty(Constants.TOWN_TOLL_RATIO_PROPERTY).trim()), 
					Integer.parseInt(prop.getProperty(Constants.VILLAGE_TOLL_INCREMENT_PROPERTY).trim()));
		}
		catch(IOException ex)
		{
			System.out.println("Config file cannot be read default rules taken");
			tollRule = new TollFeeRule(0.05, 1);
		}
		return tollRule;
	}
	
	/**
	 * Helper method for forming the part of the string that will be written to output file
	 * @param caseCount test case number
	 * @return StringBuilder which will have part of the string that will be written as output
	 */
	private StringBuilder getCaseStringBuilder(int caseCount)
	{
		StringBuilder resultBuilder = new StringBuilder();
		resultBuilder.append(Constants.CASE);
		resultBuilder.append(Constants.SPACE);
		resultBuilder.append(String.valueOf(caseCount));
		resultBuilder.append(Constants.SEMICOLON);
		resultBuilder.append(Constants.SPACE);
		return resultBuilder; 
	}
	
	/**
	 * Method for appending two strings 
	 * @param s1 string one
	 * @param s2 string two
	 * @return
	 */
	private String appendString(String s1,String s2)
	{
		StringBuilder str = new StringBuilder();
		str.append(s1);
		str.append(s2);
		return str.toString();
	}
}
