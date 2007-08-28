:- module(rdf_http_plugin,[]).


:- use_module(library(date)).
:- use_module(library('http/http_open')).

:- use_module(config).


/**
 * A replacement from the SWI rdf_http_plugin,
 * for custom timeouts and Accept headers in the
 * http request
 */


:- multifile
        rdf_db:rdf_open_hook/3,
        rdf_db:rdf_input_info/3,
        rdf_db:url_protocol/1.


rdf_db:rdf_open_hook(url(http,URL), Stream, Format) :-
        timeout(TimeOut),
        http_open(URL, Stream,
                [header(content_type, Type),
                timeout(TimeOut),
                request_header('Accept'='application/rdf+xml') % size?
                ]),
        rdf_http_plugin:guess_format(Type, URL, Format).


guess_format('text/rdf+xml',          _, xml).
guess_format('text/xml',	      _,xml).
guess_format('application/rdf+xml',   _, xml).
guess_format('application/x-turtle',  _, turtle).
guess_format('application/turtle',    _, turtle).
guess_format('text/rdf+n3',           _, turtle). % Bit dubious
guess_format('text/html',             _, xhtml).
guess_format('application/xhtml+xml', _, xhtml).
guess_format(_, URL, Format) :-
        file_name_extension(_, Ext, URL),
        rdf_db:rdf_file_type(Ext, Format).
guess_format(_,_,xml).

/**rdf_db:rdf_input_info(url(http, URL), Modified, Format) :-
 http_open(URL, Stream,
                  [ header(content_type, Type),
                    header(last_modified, Date),
                    method(head)
                  ]),
        close(Stream),
        Date \== '',
        guess_format(Type, URL, Format),
        parse_time(Date, Modified).*/

rdf_db:url_protocol(http).
