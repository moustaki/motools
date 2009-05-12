from SPARQLWrapper import SPARQLWrapper, JSON, XML
import cherrypy

class ProgrammeLocation(object):

    def default(self, place):
        place_uri = "http://dbpedia.org/resource/" + place
        return self.generate_html(place_uri)
    default.exposed = True

    def parse_sparql_xml(self, xml):
        r = []
        sparql = xml.childNodes[1]
        results = sparql.childNodes[3]
        for result in results.childNodes:
            if result.hasChildNodes():
                rr = []
                for binding in result.childNodes:
                    if binding.hasChildNodes():
                        name = binding.getAttribute('name')
                        value = binding.childNodes[1].childNodes[0].data
                        rr.append([name, value])
                r.append(rr)
        print r
        return r


    def generate_html(self, place):
        i = 0
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head></head><body>"""
        filter = """FILTER ((langMatches(lang(?plabel), "en") || lang(?plabel) = "") && (langMatches(lang(?place), "en") || lang(?place) = "" ))"""
        dbpedia = SPARQLWrapper("http://dbpedia.org/sparql")
        dbpedia.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?artist ?p ?plabel ?place WHERE { ?artist <http://dbpedia.org/ontology/currentMembers> ?m . ?artist ?p <" + place + "> . ?p rdfs:label ?plabel . <" + place + "> rdfs:label ?place . " + filter + "}")
        dbpedia.setReturnFormat(JSON)
        results = dbpedia.query().convert()

        for result in results["results"]["bindings"]:
            bbc = SPARQLWrapper("http://api.talis.com/stores/bbc-backstage/services/sparql")
            artist = result["artist"]["value"]
            property = result["p"]["value"]
            plabel = result["plabel"]["value"]
            placelabel = result["place"]["value"]
            bbc.setQuery("PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX po: <http://purl.org/ontology/po/> PREFIX tl: <http://purl.org/NET/c4dm/timeline.owl#> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT DISTINCT ?e ?etitle ?b ?btitle ?name WHERE {?maker owl:sameAs <" +artist+"> . ?maker foaf:name ?name . ?track foaf:maker ?maker . ?s po:track ?track . ?st tl:timeline ?tl .  ?s po:time ?st . ?t tl:timeline ?tl . ?v po:time ?t .  ?e po:version ?v . ?e dc:title ?etitle . ?b po:episode ?e . ?b dc:title ?btitle }")
            bbc.setReturnFormat(XML)
            z = bbc.query().convert()
            r = self.parse_sparql_xml(z)
            for b in r:
                html = html + "<p>The episode <a href=\"" + b[0][1] + "\">"+b[1][1]+"</a> from the brand <a href=\"" + b[2][1] + "\">"+ b[3][1] + "</a> featured <a href=\"" + artist + "\">"+ b[4][1] + "</a> whose <a href=\"" + property + "\">"+ plabel + "</a> is <a href=\"" + place + "\">"+placelabel+ "</a></p>"
                i = i+1
            if i > 10 :
                return html + "</body></html>"
        return html + "</body></html>"

cherrypy.quickstart(ProgrammeLocation())
