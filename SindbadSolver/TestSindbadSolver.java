

import static org.junit.Assert.assertEquals;

import org.junit.Assert;
import org.junit.Test;


/**
 * Test Class for SindbadSolver
 * @author prashanth
 *
 */
public class TestSindbadSolver {

	@Test
	public void test() {
		ITollFeeRule rule = new TollFeeRule(0.05, 1);
		SindbadSolver solver = new SindbadSolver();
		
		Vertex a1 = new Vertex('a');
		Vertex z1 = new Vertex('Z');
		a1.addOutGoingVertex(z1);
		z1.addOutGoingVertex(a1);
		try
		{
			assertEquals(20, solver.solve(a1, z1, 19, rule));
		}
		catch(SindbadSolverException ex)
		{
			Assert.fail(ex.getMessage());
		}
		
		Vertex a = new Vertex('A');
		Vertex b = new Vertex('b');
		Vertex c = new Vertex('c');
		Vertex d = new Vertex('D');
		Vertex x = new Vertex('X');
		
		a.addOutGoingVertex(d);
		a.addOutGoingVertex(b);
		
		b.addOutGoingVertex(a);
		b.addOutGoingVertex(c);
		
		c.addOutGoingVertex(b);
		c.addOutGoingVertex(x);
		
		d.addOutGoingVertex(a);
		d.addOutGoingVertex(x);
		
		x.addOutGoingVertex(d);
		x.addOutGoingVertex(c);
		
		try
		{
			assertEquals(44, solver.solve(a, x, 39, rule));
		}
		catch(SindbadSolverException ex)
		{
			Assert.fail(ex.getMessage());
		}
	}
}
