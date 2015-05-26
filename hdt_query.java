/**

Example: 
javac hdt_convert.java

java hdt_query TCGA-06-1087-01A-01-BS1.hdt 300 temp.txt


 */
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;

import org.rdfhdt.hdt.enums.RDFNotation;
import org.rdfhdt.hdt.hdt.HDT;
import org.rdfhdt.hdt.hdt.HDTManager;
import org.rdfhdt.hdt.header.Header;
import org.rdfhdt.hdt.options.HDTSpecification;
import org.rdfhdt.hdtjena.HDTGraph;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.ResultSetFormatter;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;


public class hdt_query {

	public static void main(String[] args) throws Exception {
		
		if( args.length < 3 ) {
			System.out.println("Try format: \njava className input_file area output_file");
			return;
		}
		
		String query_file = args[0];
		String area = args[1];
		String output_file = args[2];
		QueryHDT A = new QueryHDT();
		A.query(query_file, area, output_file);
		
		return;
	}
}

class QueryHDT {
	
	public void query(String query_file, String area, String output_file) throws Exception {
		
		// Load HDT file using the hdt-java library
		HDT hdt2 = HDTManager.mapIndexedHDT(query_file, null);
		 
		// Create Jena Model on top of HDT.
		HDTGraph graph = new HDTGraph(hdt2);
		Model model = ModelFactory.createModelForGraph(graph);
		
		String queryString = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" + 
				"SELECT ?sX ?p ?o WHERE { ?sX <http://a.b/Area> ?oX; ?p ?o FILTER (xsd:decimal(?oX) > " + area + " )}";
				
		Query query = QueryFactory.create(queryString);

		// Execute the query and obtain results
		QueryExecution qe = QueryExecutionFactory.create(query, model);
		ResultSet results = qe.execSelect();
		// ResultSetFormatter.outputAsCSV(System.out, results);
		
		try {
			
			FileWriter fileWriter = new FileWriter(output_file, true);
			BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);;
			
			String prev_item = "";
			String record = "";
			while ( results.hasNext() ) {
				QuerySolution qs = results.next();
				
				if( prev_item.equals(qs.get("sX").toString()) )
					record = record + qs.get("o") + "\t";
				else {			
					record = record.trim();
					if( !record.equals("") )
						bufferedWriter.write(record + "\n");
					record = qs.get("o") + "\t";
				}
				prev_item = qs.get("sX").toString();
			}
			bufferedWriter.write(record);
		}
		catch(FileNotFoundException ex) {
            System.out.println("Unable to open file.");          
        }
		catch(IOException ex) {
			System.out.println("Unable to read/write file."); 
		}
		// Important - free up resources used running the query
		qe.close();
	}
}
