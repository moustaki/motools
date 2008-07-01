import de.fuberlin.wiwiss.d2rq.values.Translator;
import java.lang.String;

public class MySpaceTranslator implements Translator {

	public MySpaceTranslator(){
		
	}

	public String toDBValue(String rdfValue) {
		return rdfValue.replaceFirst("http://dbtune.org/myspace/","http://www.myspace.com/");
	}	

	public String toRDFValue(String dbValue) {
		return dbValue.replaceFirst("http://www.myspace.com/","http://dbtune.org/myspace/");
	}
}

