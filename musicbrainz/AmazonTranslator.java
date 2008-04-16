import de.fuberlin.wiwiss.d2rq.values.Translator;
import java.lang.String;

public class AmazonTranslator implements Translator {

	public AmazonTranslator(){
		
	}

	public String toDBValue(String rdfValue) {
		String r = null;
		if((rdfValue.split("images/P/")).length==2) r = "http://www.amazon.com/gp/product/"+(rdfValue.split("images/P/"))[1];
		else r = rdfValue;
		return r; // What if the original URI was in another domain?
	}	

	public String toRDFValue(String dbValue) {
		String asin = (dbValue.split("gp/product/"))[1];
		return "http://images.amazon.com/images/P/"+asin;
	}
}

