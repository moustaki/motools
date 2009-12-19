#!/usr/bin/python
# -*- coding: utf8 -*-
#
# SpecGen v5, ontology specification generator tool
# <http://forge.morfeo-project.org/wiki_en/index.php/SpecGen>
# 
# Copyright (c) 2003-2008 Christopher Schmidt <crschmidt@crschmidt.net>
# Copyright (c) 2005-2008 Uldis Bojars <uldis.bojars@deri.org>
# Copyright (c) 2007-2008 Sergio Fernández <sergio.fernandez@fundacionctic.org>
#
# Previous versions of SpecGen:
#     v1,2,3 by Christopher Schmidt <http://crschmidt.net/semweb/redland>
#     v4 by Uldis Bojars <http://sioc-project.org/specgen>
# 
# This software is licensed under the terms of the MIT License.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__version__ = "5.4.2"
__authors__ = "Christopher Schmidt, Uldis Bojars, Sergio Fernández"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "specgen-devel@lists.morfeo-project.org"
__date__    = "2008-12-02"
 
import os
import sys
import time
import re
import urllib

try:
    import RDF
except ImportError:
    version = sys.version.split(" ")[0]
    if version.startswith("2.5"):
        sys.path.append("/usr/lib/python2.4/site-packages/")
    else:
        sys.path.append("/usr/lib/python2.5/site-packages/")
    try:
        import RDF
    except:
        sys.exit("Error importing RedLand bindings for Python; check if it is installed correctly")

#global vars
classranges = {}
classdomains = {}
spec_url = None
spec_ns = None
spec_pre = None
ns_list = { "http://www.w3.org/1999/02/22-rdf-syntax-ns#"   : "rdf",
            "http://www.w3.org/2000/01/rdf-schema#"         : "rdfs",
            "http://www.w3.org/2002/07/owl#"                : "owl",
            "http://www.w3.org/2001/XMLSchema#"             : "xsd",
            "http://rdfs.org/sioc/ns#"                      : "sioc",
            "http://xmlns.com/foaf/0.1/"                    : "foaf", 
            "http://purl.org/dc/elements/1.1/"              : "dc",
            "http://purl.org/dc/terms/"                     : "dct",
            "http://usefulinc.com/ns/doap#"                 : "doap",
            "http://www.w3.org/2003/06/sw-vocab-status/ns#" : "status",
            "http://purl.org/rss/1.0/modules/content/"      : "content", 
            "http://www.w3.org/2003/01/geo/wgs84_pos#"      : "geo",
            "http://www.w3.org/2004/02/skos/core#"          : "skos"
          }

rdf = RDF.NS('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = RDF.NS('http://www.w3.org/2000/01/rdf-schema#')
owl = RDF.NS('http://www.w3.org/2002/07/owl#')
vs = RDF.NS('http://www.w3.org/2003/06/sw-vocab-status/ns#')

termdir = './doc' #TODO


def niceName(uri):
    regexp = re.compile( "^(.*[/#])([^/#]+)$" )
    rez = regexp.search( uri )
    pref = rez.group(1)
    #return ns_list.get(pref, pref) + ":" + rez.group(2)
    if ns_list.has_key(pref):
        return ns_list.get(pref, pref) + ":" + rez.group(2)
    else:
        return uri


def setTermDir(directory):
    global termdir
    termdir = directory


def termlink(string):
    """FOAF specific: function which replaces <code>foaf:*</code> with a 
    link to the term in the document."""
    return re.sub(r"<code>" + spec_pre + r":(\w+)</code>", r"""<code><a href="#term_\1">""" + spec_pre + r""":\1</a></code>""", string)    


def return_name(m, urinode):
    "Trims the FOAF namespace out of a term to give a name to the term."
    return str(urinode.uri).replace(spec_url, "")


def get_rdfs(m, urinode):
    "Returns label and comment given an RDF.Node with a URI in it"
    comment = ''
    label = ''
    if (type(urinode)==str):
        urinode = RDF.Uri(urinode)
    l = m.find_statements(RDF.Statement(urinode, rdfs.label, None))
    if l.current():
        label = l.current().object.literal_value['string']
    c = m.find_statements(RDF.Statement(urinode, rdfs.comment, None))
    if c.current():
        comment = c.current().object.literal_value['string']
    return label, comment


def get_status(m, urinode):
    "Returns the status text for a term."
    status = ''
    s = m.find_statements(RDF.Statement(urinode, vs.term_status, None))
    if s.current():
        return s.current().object.literal_value['string']


def htmlDocInfo( t ):
    """Opens a file based on the term name (t) and termdir directory (global).
       Reads in the file, and returns a linkified version of it."""
    doc = ""
    try:
        f = open("%s/%s.en" % (termdir, t), "r")
        doc = f.read()
        doc = termlink(doc)
    except:
        return "" 	# "<p>No detailed documentation for this term.</p>"
    return doc


def owlVersionInfo(m):
    v = m.find_statements(RDF.Statement(None, owl.versionInfo, None))
    if v.current():
        return v.current().object.literal_value['string']
    else:
        return ""


def rdfsPropertyInfo(term,m):
    """Generate HTML for properties: Domain, range, status."""
    global classranges
    global classdomains
    doc = ""
    range = ""
    domain = ""

    #find subPropertyOf information
    o = m.find_statements( RDF.Statement(term, rdfs.subPropertyOf, None) )
    if o.current():
        rlist = ''
        for st in o:
            k = getTermLink(str(st.object.uri))
            rlist += "<dd>%s</dd>" % k
        doc += "<dt>sub-property-of:</dt> %s" % rlist

    #domain stuff
    domains = m.find_statements(RDF.Statement(term, rdfs.domain, None))
    domainsdoc = ""
    for d in domains:
        collection = m.find_statements(RDF.Statement(d.object, owl.unionOf, None))
        if collection.current():
            uris = parseCollection(m, collection)
            for uri in uris:
                domainsdoc += "<dd>%s</dd>" % getTermLink(uri)
                add(classdomains, uri, term.uri)
        else:
            if not d.object.is_blank():
                domainsdoc += "<dd>%s</dd>" % getTermLink(str(d.object.uri))
    if (len(domainsdoc)>0):
        doc += "<dt>Domain:</dt> %s" % domainsdoc

    #range stuff
    ranges = m.find_statements(RDF.Statement(term, rdfs.range, None))
    rangesdoc = ""
    for r in ranges:
        collection = m.find_statements(RDF.Statement(r.object, owl.unionOf, None))
        if collection.current():
            uris = parseCollection(m, collection)
            for uri in uris:
                rangesdoc += "<dd>%s</dd>" % getTermLink(uri)
                add(classranges, uri, term.uri)
        else:
            if not r.object.is_blank():
                rangesdoc += "<dd>%s</dd>" % getTermLink(str(r.object.uri))
    if (len(rangesdoc)>0):
        doc += "<dt>Range:</dt> %s" % rangesdoc

    return doc


def parseCollection(model, collection):
    # #propertyA a rdf:Property ;
    #   rdfs:domain [
    #      a owl:Class ;
    #      owl:unionOf [
    #        rdf:parseType Collection ;
    #        #Foo a owl:Class ;
    #        #Bar a owl:Class
    #     ]
    #   ]
    # 
    # seeAlso "Collections in RDF"

    uris = []

    rdflist = model.find_statements(RDF.Statement(collection.current().object, None, None))
    while rdflist and rdflist.current() and not rdflist.current().object.is_blank():
        one = rdflist.current()
        if not one.object.is_blank():
            uris.append(str(one.object.uri))
        rdflist.next()
        one = rdflist.current()
        if one.predicate == rdf.rest:
            rdflist = model.find_statements(RDF.Statement(one.object, None, None))
    
    return uris


def getTermLink(uri):
    uri = str(uri)
    if (uri.startswith(spec_url)):
        return '<a href="#term_%s" style="font-family: monospace;">%s</a>' % (uri.replace(spec_url, ""), niceName(uri))
    else:
        return '<a href="%s" style="font-family: monospace;">%s</a>' % (uri, niceName(uri))


def rdfsClassInfo(term,m):
    """Generate rdfs-type information for Classes: ranges, and domains."""
    global classranges
    global classdomains
    doc = ""

    #patch to control incoming strings (FIXME, why??? drop it!)
    try:
        term.uri
    except:
        term = RDF.Node(RDF.Uri(term))

    # Find subClassOf information
    o = m.find_statements( RDF.Statement(term, rdfs.subClassOf, None) )
    if o.current():
        doc += "<dt>sub-class-of:</dt>"
        superclasses = []
        for st in o:
            if not st.object.is_blank():
                uri = str(st.object.uri)
                if (not uri in superclasses):
                    superclasses.append(uri)
        for superclass in superclasses:
            doc += "<dd>%s</dd>" % getTermLink(superclass)

    # Find out about properties which have rdfs:domain of t
    d = classdomains.get(str(term.uri), "")
    if d:
        dlist = ''
        for k in d:
            dlist += "<dd>%s</dd>" % getTermLink(k)
        doc += "<dt>in-domain-of:</dt>" + dlist

    # Find out about properties which have rdfs:range of t
    r = classranges.get(str(term.uri), "")
    if r:
        rlist = ''
        for k in r:
            rlist += "<dd>%s</dd>" % getTermLink(k)
        doc += "<dt>in-range-of:</dt>" + rlist

    return doc

def rdfsInstanceInfo(term,m):
    """Generate rdfs-type information for instances"""
    doc = ""
    
    t = m.find_statements( RDF.Statement(RDF.Node(RDF.Uri(term)), rdf.type, None) )
    if t.current():
        doc += "<dt>RDF Type:</dt>"
    while t.current():
        doc += "<dd>%s</dd>" % getTermLink(str(t.current().object.uri))
        t.next()

    return doc


def owlInfo(term,m):
    """Returns an extra information that is defined about a term (an RDF.Node()) using OWL."""
    res = ''

    # FIXME: refactor this code
    
    # Inverse properties ( owl:inverseOf )
    o = m.find_statements( RDF.Statement(term, owl.inverseOf, None) )
    if o.current():
        res += "<dt>Inverse:</dt>"
        for st in o:
            res += "<dd>%s</dd>" % getTermLink(str(st.object.uri))
    
    # Datatype Property ( owl.DatatypeProperty )
    o = m.find_statements( RDF.Statement(term, rdf.type, owl.DatatypeProperty) )
    if o.current():
        res += "<dt>OWL Type:</dt><dd>DatatypeProperty</dd>\n"
	
    # Object Property ( owl.ObjectProperty )
    o = m.find_statements( RDF.Statement(term, rdf.type, owl.ObjectProperty) )
    if o.current():
        res += "<dt>OWL Type:</dt><dd>ObjectProperty</dd>\n"

    # Annotation Property ( owl.AnnotationProperty )
    o = m.find_statements( RDF.Statement(term, rdf.type, owl.AnnotationProperty) )
    if o.current():
        res += "<dt>OWL Type:</dt><dd>AnnotationProperty</dd>\n"

    # IFPs ( owl.InverseFunctionalProperty )
    o = m.find_statements( RDF.Statement(term, rdf.type, owl.InverseFunctionalProperty) )
    if o.current():
        res += "<dt>OWL Type:</dt><dd>InverseFunctionalProperty (uniquely identifying property)</dd>\n"

    # Symmertic Property ( owl.SymmetricProperty )
    o = m.find_statements( RDF.Statement(term, rdf.type, owl.SymmetricProperty) )
    if o.current():
        res += "<dt>OWL Type:</dt><dd>SymmetricProperty</dd>\n"
	
    return res


def docTerms(category, list, m):
    """
    A wrapper class for listing all the terms in a specific class (either
    Properties, or Classes. Category is 'Property' or 'Class', list is a 
    list of term names (strings), return value is a chunk of HTML.
    """
    doc = ""
    nspre = spec_pre
    for t in list:
        if (t.startswith(spec_url)) and (len(t[len(spec_url):].split("/"))<2):
            term = t
            t = t.split(spec_url[-1])[-1]
            curie = t#"%s:%s" % (nspre, t)
        else:
            if t.startswith("http://"):
                term = t
                curie = getShortName(t)
                t = getAnchor(t)
            else:
                term = spec_ns[t]
                curie = "%s:%s" % (nspre, t)
        
        doc += """<div class="specterm" id="term_%s">\n<h3>%s: %s</h3>\n""" % (t, category, curie)
        try:
            term_uri = term.uri
        except:
            term_uri = term
        doc += """<p style="font-family:monospace; font-size:0.em;">URI: <a href="%s">%s</a></p>""" % (term_uri, term_uri)
        label, comment = get_rdfs(m, term)    
        status = get_status(m, term)
        doc += "<p><em>%s</em> - %s </p>" % (label, comment)
        terminfo = ""
        if category=='Property':
            terminfo += owlInfo(term,m)
            terminfo += rdfsPropertyInfo(term,m)
        if category=='Class':
            terminfo += rdfsClassInfo(term,m)
        if category=='Instance':
            terminfo += rdfsInstanceInfo(term,m)
        if (len(terminfo)>0): #to prevent empty list (bug #882)
            doc += "\n<dl>%s</dl>\n" % terminfo 
        doc += htmlDocInfo(t)
        doc += "<p style=\"float: right; font-size: small;\">[<a href=\"#sec-glance\">back to top</a>]</p>\n\n"
        doc += "\n\n</div>\n\n"
    
    return doc


def getShortName(uri):
    if ("#" in uri):
        return uri.split("#")[-1]
    else:
        return uri.split("/")[-1]


def getAnchor(uri):
    if (uri.startswith(spec_url)):
        return uri[len(spec_url):].replace("/","_")
    else:
        return getShortName(uri)


def buildazlist(classlist, proplist, instalist=None):
    """
    Builds the A-Z list of terms. Args are a list of classes (strings) and 
    a list of props (strings)
    """
    azlist = '<div style="padding: 1em; border: dotted; background-color: #ddd;">'

    if (len(classlist)>0):
        azlist += "<p>Classes: "
        classlist.sort()
        for c in classlist:
            if c.startswith(spec_url):
                c = c.split(spec_url[-1])[1]
            azlist = """%s <a href="#term_%s">%s</a>, """ % (azlist, c, c)
        azlist = """%s\n</p>""" % azlist

    if (len(proplist)>0):
        azlist += "<p>Properties: "
        proplist.sort()
        for p in proplist:
            if p.startswith(spec_url):
                p = p.split(spec_url[-1])[1]
            azlist = """%s <a href="#term_%s">%s</a>, """ % (azlist, p, p)
        azlist = """%s\n</p>""" % azlist

    if (instalist!=None and len(instalist)>0):
        azlist += "<p>Instances: "
        for i in instalist:
            p = getShortName(i)
            anchor = getAnchor(i)
            azlist = """%s <a href="#term_%s">%s</a>, """ % (azlist, anchor, p)
        azlist = """%s\n</p>""" % azlist

    azlist = """%s\n</div>""" % azlist
    return azlist


def build_simple_list(classlist, proplist, instalist=None):
    """
    Builds a simple <ul> A-Z list of terms. Args are a list of classes (strings) and 
    a list of props (strings)
    """

    azlist = """<div style="padding: 5px; border: dotted; background-color: #ddd;">"""
    azlist = """%s\n<p>Classes:""" % azlist
    azlist += """\n<ul>"""

    classlist.sort()
    for c in classlist:
        azlist += """\n  <li><a href="#term_%s">%s</a></li>""" % (c.replace(" ", ""), c)
    azlist = """%s\n</ul></p>""" % azlist

    azlist = """%s\n<p>Properties:""" % azlist
    azlist += """\n<ul>"""
    proplist.sort()
    for p in proplist:
        azlist += """\n  <li><a href="#term_%s">%s</a></li>""" % (p.replace(" ", ""), p)
    azlist = """%s\n</ul></p>""" % azlist

    #FIXME: instances

    azlist = """%s\n</div>""" % azlist
    return azlist


def add(where, key, value):
    if not where.has_key(key):
        where[key] = []
    if not value in where[key]:
        where[key].append(value)


def specInformation(m, ns):
    """
    Read through the spec (provided as a Redland model) and return classlist
    and proplist. Global variables classranges and classdomains are also filled
    as appropriate.
    """
    global classranges
    global classdomains

    # Find the class information: Ranges, domains, and list of all names.
    classtypes = [rdfs.Class, owl.Class]
    classlist = []
    for onetype in classtypes:
        for classStatement in  m.find_statements(RDF.Statement(None, rdf.type, onetype)):
            for range in m.find_statements(RDF.Statement(None, rdfs.range, classStatement.subject)):
                if not m.contains_statement( RDF.Statement( range.subject, rdf.type, owl.DeprecatedProperty )):
                    if not classStatement.subject.is_blank():
                        add(classranges, str(classStatement.subject.uri), str(range.subject.uri))
            for domain in m.find_statements(RDF.Statement(None, rdfs.domain, classStatement.subject)):
                if not m.contains_statement( RDF.Statement( domain.subject, rdf.type, owl.DeprecatedProperty )):
                    if not classStatement.subject.is_blank():
                        add(classdomains, str(classStatement.subject.uri), str(domain.subject.uri))
            if not classStatement.subject.is_blank():
                uri = str(classStatement.subject.uri)
                name = return_name(m, classStatement.subject)
                if name not in classlist and uri.startswith(spec_url):
                    classlist.append(return_name(m, classStatement.subject))

    # Create a list of properties in the schema.
    proptypes = [rdf.Property, owl.ObjectProperty, owl.DatatypeProperty, owl.AnnotationProperty]
    proplist = []
    for onetype in proptypes: 
        for propertyStatement in m.find_statements(RDF.Statement(None, rdf.type, onetype)):
            uri = str(propertyStatement.subject.uri)
            name = return_name(m, propertyStatement.subject)
            if uri.startswith(ns) and not name in proplist:
                proplist.append(name)

    return classlist, proplist

def getInstances(model, classes, properties):
    """
    Extract all resources instanced in the ontology
    (aka "everything that is not a class or a property")
    """
    instances = []
    for one in classes:
        for i in model.find_statements(RDF.Statement(None, rdf.type, spec_ns[one])):
            uri = str(i.subject.uri)
            if not uri in instances:
                instances.append(uri)
    for i in model.find_statements(RDF.Statement(None, rdfs.isDefinedBy, RDF.Uri(spec_url))):            
            uri = str(i.subject.uri)
            if (uri.startswith(spec_url)):
                uri = uri[len(spec_url):]
            if ((not uri in instances) and (not uri in classes)):
                instances.append(uri)
    return instances
   
 
def specgen(specloc, template, instances=False, mode="spec"):
    """The meat and potatoes: Everything starts here."""

    global spec_url
    global spec_ns
    global ns_list
        
    m = RDF.Model()
    p = RDF.Parser()
    try:
        p.parse_into_model(m, specloc)
    except IOError, e:
        print "Error reading from ontology:", str(e)
        usage()
    except RDF.RedlandError, e:
        print "Error parsing the ontology"

    spec_url = getOntologyNS(m)
    spec_ns = RDF.NS(spec_url)
    ns_list[spec_url] = spec_pre

    classlist, proplist = specInformation(m, spec_url)
    classlist = sorted(classlist)
    proplist = sorted(proplist)

    instalist = None
    if instances:
        instalist = getInstances(m, classlist, proplist)
        instalist.sort(lambda x, y: cmp(getShortName(x).lower(), getShortName(y).lower()))
    
    if mode == "spec":
        # Build HTML list of terms.
        azlist = buildazlist(classlist, proplist, instalist)
    elif mode == "list":
        # Build simple <ul> list of terms.
        azlist = build_simple_list(classlist, proplist, instalist)

    # Generate Term HTML
    termlist = docTerms('Property', proplist, m)
    termlist = docTerms('Class', classlist, m) + termlist
    if instances:
        termlist += docTerms('Instance', instalist, m)
    
    # Generate RDF from original namespace.
    u = urllib.urlopen(specloc)
    rdfdata = u.read()
    rdfdata = re.sub(r"(<\?xml version.*\?>)", "", rdfdata)
    rdfdata = re.sub(r"(<!DOCTYPE[^]]*]>)", "", rdfdata)
    #rdfdata.replace("""<?xml version="1.0"?>""", "")
    
    # print template % (azlist.encode("utf-8"), termlist.encode("utf-8"), rdfdata.encode("ISO-8859-1"))
    template = re.sub(r"^#format \w*\n", "", template)
    template = re.sub(r"\$VersionInfo\$", owlVersionInfo(m).encode("utf-8"), template) 
    
    # NOTE: This works with the assumtpion that all "%" in the template are escaped to "%%" and it
    #       contains the same number of "%s" as the number of parameters in % ( ...parameters here... )
    template = template % (azlist, termlist.encode("utf-8"));    
    template += "<!-- specification regenerated by SpecGen5 at " + time.strftime('%X %x %Z') + " -->"
    
    return template


def save(path, text):
    try:
        f = open(path, "w")
        f.write(text)
        f.flush()
        f.close()
    except Exception, e:
        print "Error writting in file \"" + path + "\": " + str(e)


def getOntologyNS(m):
    ns = None
    o = m.find_statements(RDF.Statement(None, rdf.type, owl.Ontology))
    if o.current():
        s = o.current().subject
        if (not s.is_blank()):
            ns = str(s.uri)
            if (ns[-1]!="/" and ns[-1]!="#"):
                ns += "#"

    if (ns == None):
        sys.exit("Impossible to get ontology's namespace")
    else:
        return ns


def __getScriptPath():
    path = sys.argv[0]
    if path.startswith("./"):
        return path
    else:
        base = "/".join(path.split("/")[:-1])
        for one in os.environ["PATH"].split(":"):
            if base == one:
                return path.split("/")[-1]
        return path


def usage():
    script = __getScriptPath()
    print """Usage: 
    %s ontology prefix template destination [flags]

        ontology    : path to ontology file
        prefix      : prefix for CURIEs
        template    : HTML template path
        destination : specification destination (by default)

        optional flags:
                -i   : add instances on the specification (disabled by default)

examples:
    %s example.owl ex template.html example.owl.html -i

""" % (script, script)
    sys.exit(-1)

if __name__ == "__main__":
    """Ontology specification generator tool"""
    
    args = sys.argv[1:]
    if (len(args) < 4):
        usage()
    else:
        
        #ontology
        specloc = "file:" + str(args[0])
        spec_pre = args[1]

        #template
        temploc = args[2]
        template = None
        try:
            f = open(temploc, "r")
            template = f.read()
        except Exception, e:
            print "Error reading from template \"" + temploc + "\": " + str(e)
            usage()

        #destination
        dest = args[3]
 
        #flags
        instances = False
        if len(args) > 3:
            flags = args[3:]
            if '-i' in flags:
                instances = True
        
        save(dest, specgen(specloc, template, instances=instances))

