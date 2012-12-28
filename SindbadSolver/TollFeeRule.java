

/**
 * Implementation for ITollFeeRule
 * @author prashanth
 *
 */
public class TollFeeRule implements ITollFeeRule{
	
	private double townTollRatio; //fee ratio that has to be paid at Toll in Town 
	private int villageTollIncrementer; //fee that has to be paid at Toll in village
	
	public TollFeeRule(double townTollRatio,int villageTollIncrementer){
		this.townTollRatio = townTollRatio;
		this.villageTollIncrementer = villageTollIncrementer;
	}
	
	public int calculateItemsBeforeTollForVillage(int itemsAfterToll)
	{
		return itemsAfterToll + villageTollIncrementer;
	}
	
	public int calculateItemsBeforeTollForTown(int itemsAfterToll)
	{
		 return (int)Math.ceil(((double)itemsAfterToll) / (1-townTollRatio));
	}
}
