import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.ResultSetFormatter;
import com.hp.hpl.jena.rdf.model.Literal;
import com.hp.hpl.jena.rdf.model.Resource;

// simple demo class that queries the gnarql endpoint on the cluster

// dependencies:
// add all the .jar files in the /lib directory of Jena (jena.sourceforge.net) to your classpath

public class SparqlClient {

	public static void main(String[] args) {
		
		SparqlClient sparqlClient = new SparqlClient();
		
		String[] artists = {"The Beatles", "The Clash", "The Police"};
		sparqlClient.findTracksForArtists(artists);

	}

	public void findTracksForArtists(String[] artists) {
		
		//	iterate over artists
		for (int i = 0; i < artists.length; i++) {

			String queryString = "";
			try {
				
				// create a sparql query by hand
				queryString = 
					"PREFIX dc:   <http://purl.org/dc/elements/1.1/> " +
					"PREFIX mo: <http://purl.org/ontology/mo/> " +
					"PREFIX foaf: <http://xmlns.com/foaf/0.1/> " + 
					"SELECT ?title ?fileURI " +
					"WHERE {" +
					"      ?trackURI foaf:maker ?artist  . " +
					"	   ?artist foaf:name \"" + artists[i] + "\" . " +
					"      ?trackURI dc:title ?title . " +
					"	   ?trackURI mo:available_as ?fileURI . " +
					"      }";			

				Query query = QueryFactory.create(queryString) ;
				
				// print out the query
				query.serialize(System.out) ;
				System.out.println();

				// run the query against the endpoint
				QueryExecution qExec = QueryExecutionFactory.sparqlService("http://dsp-cluster:3021/sparql/", query);
				ResultSet rs = qExec.execSelect() ;

				// iterate over the results
				// - note that the order of results is undefined
				for ( ; rs.hasNext() ; )
				{
					// the next solution i.e. returned result set
					QuerySolution rb = rs.nextSolution() ;

					// get nodes from the solution and cast them appropriately
					Literal title = (Literal) rb.get("title") ;		// ?title is just an untyped literal
					Resource fileURI = (Resource) rb.get("fileURI") ;	// ?fileURI is a uri and so will be a resource

					// print out the result
					System.out.println(artists[i] + ": " + title + "\t" + fileURI.getURI());
					
					// do something useful with it
					// ...
				}

				// or use a Jena utility class to print all the results in a standard format
				// ResultSetFormatter.out(System.out, qExec.execSelect(), query) ;
				
				qExec.close() ;

			}
			catch (Exception ex) {
				System.out.println("problem with: \n" + queryString);
				ex.printStackTrace();
			}
		}				
	}
}

