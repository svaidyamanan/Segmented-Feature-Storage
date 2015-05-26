/**

Example: 
javac hdt_convert.java

java hdt_convert TCGA-AA-3870-01Z-00-DX1.txt output/
java hdt_convert TCGA-AA-3870-01Z-00-DX1.txt output/ log/

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
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.ResultSetFormatter;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;


public class hdt_convert {

	public static void main(String[] args) throws Exception {
		
		if( args.length < 3 ) {
			System.out.println("Try format: \njava className input output log");
			return;
		}
		
		long start_time, end_time, time_taken;
		String output_path, log_file;
		String input_file, output_file;
		
		ConvertHDT A = new ConvertHDT();
		
		long input_size = 0, output_size = 0;
		input_file = args[0];
		output_path = args[1];
		log_file = args[2] + "/log_hdt.txt";
		
		if( input_file.lastIndexOf("/") > -1 )
			output_file = output_path + "/" + input_file.substring(input_file.lastIndexOf("/"), input_file.lastIndexOf(".")) + ".hdt";
		else
			output_file = output_path + "/" + input_file.substring(0, input_file.lastIndexOf(".")) + ".hdt";
		
		// System.out.println("Input file :" + input_file);
		// System.out.println("Output file :" + output_file);

	    start_time = System.nanoTime();
		A.convert(input_file, output_file, log_file);
		end_time = System.nanoTime();
	    
		time_taken = (end_time - start_time) / 1000000000;  
	    System.out.println("HDT Creation Time :  : " + time_taken + " s");
		// System.out.println("Input Size : " + input_size);
		// System.out.println("Output Size : " + output_size);
		
		return;
	}
}

class ConvertHDT {
	
	public void convert(String input_file, String output_file, String log_file) throws Exception {
		String baseURI = "http://a.b/mydata";
		String inputTSV = input_file;
		String inputType = "tsv";
		String hdtOutput = output_file;
		
		// Create HDT from RDF file
		HDT hdt = HDTManager.generateHDT(inputTSV, baseURI, RDFNotation.parse(inputType), new HDTSpecification(), null);
		
		
		// Add additional domain-specific properties to the header:
		Header header = hdt.getHeader();
		header.insert("myResource1", "property" , "value");
		
		gen_log(input_file, output_file, log_file);
		// Save generated HDT to a file
		hdt.saveToHDT(hdtOutput, null);
	}
	
	private void gen_log(String input_file, String output_file, String log_file) {
		
		String file_read = "";
		double x_val = 0.0, y_val = 0.0;
		double min_X = 99999, min_y = 99999, max_X = -1, max_y = -1;
		String file_split[];
		String tile;
		
		if( input_file.lastIndexOf("/") > -1 ) {
			tile = input_file.substring(input_file.lastIndexOf("/")+1, input_file.lastIndexOf(".")) + ".txt";
		}
		else {
			tile = input_file.substring(0, input_file.lastIndexOf(".")) + ".txt";
		}
		// System.out.println("Input file :" + input_file);
		// System.out.println("Log file :" + log_path);
		
		try {
		
			FileReader fileReader = new FileReader(input_file);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			FileWriter fileWriter;
			BufferedWriter bufferedWriter;
			
			File log_dir = new File(log_file);
			if (!log_dir.exists()) {
				// System.out.println("Creating log path");
				fileWriter = new FileWriter(log_file);
				bufferedWriter = new BufferedWriter(fileWriter);
				bufferedWriter.write("tile\tmin_X\tmin_Y\tmax_X\tmax_Y\n");
			}
			else {
				fileWriter = new FileWriter(log_dir, true);
				bufferedWriter = new BufferedWriter(fileWriter);
			}
			file_read = bufferedReader.readLine();
			
			while((file_read = bufferedReader.readLine()) != null) {
                file_split = file_read.split("\t");
				x_val = Double.parseDouble(file_split[1]);
				y_val = Double.parseDouble(file_split[2]);
				
				min_X = min_X > x_val ? x_val : min_X;
				min_y = min_y > y_val ? y_val : min_y;
				max_X = max_X < x_val ? x_val : max_X;
				max_y = max_y < y_val ? y_val : max_y;
            }
			bufferedWriter.write(output_file + '\t' + min_X + '\t' + min_y + '\t' + max_X + '\t' + max_y + '\n');
			
			bufferedReader.close();
			bufferedWriter.close();
		}
		catch(FileNotFoundException ex) {
            System.out.println("Unable to open file.");          
        }
		catch(IOException ex) {
			System.out.println("Unable to read/write file."); 
		}
	}
}