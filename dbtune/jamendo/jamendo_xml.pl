:- module(jamendo_xml,[parsed_dump/1]).

xml_dump('dbdump.en.xml').

:- dynamic parsed_dump/1.

load_xml_dump :-
        xml_dump(Dump),
        load_xml_file(Dump,Content),
        assert(parsed_dump(Content)).

:- load_xml_dump.

