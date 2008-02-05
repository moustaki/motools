:- module(match,[
		op(500,xfx,'eq')
	,	op(500,xfx,'leq')
	,	op(400,xfx,'advertise_if')
	]).

:- multifile match:eq/2.
:- multifile match:leq/2.
