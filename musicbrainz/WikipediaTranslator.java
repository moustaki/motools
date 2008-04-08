import de.fuberlin.wiwiss.d2rq.values.Translator;
import java.lang.String;

public class WikipediaTranslator implements Translator {

	public WikipediaTranslator(){
		
	}

	public String toDBValue(String rdfValue) {
		return rdfValue.replaceFirst("http://dbpedia.org/resource/","http://en.wikipedia.org/wiki/");
	}	

	public String toRDFValue(String dbValue) {
		return dbValue.replaceFirst("http://en.wikipedia.org/wiki/","http://dbpedia.org/resource/");
	}
}

