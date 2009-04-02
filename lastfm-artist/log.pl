/**
 * Some logging facilities
 * Copyright Yves Raimond (c) 2006
 */
:- module(log,[log/1,log/2]).


log_file('/var/log/lastartist/server.log').

log(MessageFormat,Vars) :-
	sformat(String,MessageFormat,Vars),
	log(String).

log(Message) :-
	get_time(A),
	convert_time(A,Y,M,D,H,Min,S,_),
	sformat(Stamp,'<~d/~d/~d-~d:~d:~d> ',[Y,M,D,H,Min,S]),
	log_file(File),
	open(File,append,Stream,[]),
	write(Stream,Stamp),
	write(Stream,Message),
	write(Stream,'\n'),
	close(Stream).


