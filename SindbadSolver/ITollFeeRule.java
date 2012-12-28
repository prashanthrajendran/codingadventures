
/**
 * Interface which specifies the contract for calculating the toll fee for Town and Village
 * @author prashanth
 *
 */
public interface ITollFeeRule {
	
	/**
	 * To calculate the number of Items that has to be present before the Village 
	 * @param itemsAfterToll Number of items in the village after detecting toll fee
	 * @return number of items that has to be present before detecting the toll fee
	 */
	public int calculateItemsBeforeTollForVillage(int itemsAfterToll);
	
	/**
	 * To calculate the number of Items that has to be present before the Town 
	 * @param itemsAfterToll Number of items in the town after detecting toll fee
	 * @return number of items that has to be present before detecting the toll fee
	 */
	public int calculateItemsBeforeTollForTown(int itemsAfterToll);
}
