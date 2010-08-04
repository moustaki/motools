:- module(log,[log/1,log/2]).

/** <module> Logging

Some logging facilities

@author		Yves Raimond
@version	1.0 
@copyright	Yves Raimond; 2006
*/

%%	log_file(+LOG_FILE_NAME)
%
%	Defines the logging file name.

log_file('server.log').

%% 	log(+MessageFormat, +Vars)
%
%	Formates the log string.

log(MessageFormat,Vars) :-
	sformat(String,MessageFormat,Vars),
	log(String).

%% 	log(+Message)
%
%	Writes the log string into a file (with time stamp).

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


