query('#786778',[W,N],[name(W,N),time(W,T),sometimeago(years,T),featured(W,Lesson),agent(Lesson,'Rodney Jerkins'),agent(Lesson,'Max Martin'),content(W,Content)],5).
query('#786627',[T,G],[broadcast(A,B),during(B,ncaa),featured(A,S),time(S,70s),genre(S,disco),similar(S,'Sister Sledge - We are family'),context,singer(S,Singer),gender(Singer,female),rhythm(S,upbeat),title(S,T),group(S,G)],11).
query('#786307',[S],[genre(S,indyrock),lyrics(S,L),about(L,school)],3).
query('#786306',[Info],[about(Show,Info)],1).
query('#786175',[M],[title(M,rollingstone),featured(M,Ad),about(Ad,F),title(F,ozarkmusicfestival),place(F,misouri),time(F,'july 1974')],6).
query('#786067',[A,T],[genre(S,techno),context,lyrics(S,Lyrics),contains(Lyrics,allthepeople),artist(S,A),title(S,T)],4).
query('#786065',[A,T],[context,listened(S,Evt),time(Evt,Time),sometimeago(12years,Time),thought_artist(S,'reba mc intyre'),lyrics(S,L),about(L,'littlegirl'),contains(L,'doll'),artist(S,A),title(S,T)],6).
query('#785974',[T],[title(S,T),broadcast(S,B),time(B,Time),sometimeago(16years,Time),lyrics(S,L),about(L,daughter),beginning(S,Beg),sounds_like(Beg,girlsinging),middle(S,Middle),sounds_like(Middle,teengirlsinging),end(S,End),sounds_like(End,woman_singing),context,rhythm(S,slow)],12).
query('#785956',[L],[lyrics(S,L),artist(S,A),name(A,thepentangle),context,title(Song,titles)],[4]).
query('#785951',[MS],[market_share(MS),about(MS,majorandindependent)],1).
query('#785926',[SM],[title(S,godonlyknows),artist(S,beachboys),album(S,A),title(A,petsounds),arrangement(S,Arr),instrument(Arr,stringquartet),score(Arr,SM),context],7). % no instrument per arrangement
query('#785763',[T],[title(S,T),clue(T,wita)],1). % do i count 3 clues, or one?
query('#785747',[R],[title(S1,odetojoy),title(S2,angels),similar(S1,S2),relation(R,S1,S2)],3).
query('#785729',[O],[person(bonjovi),performer(P,bonjovi),place(P,miltonkeys),time(P,2001),performer(P,O)],5).
query('#785332',[N],[featured(V,P),title(V,tipdrill),name(P,N),wear(N,W),beginning(V,B),take_off(B,bikinibottom),atlanta_falcon(V),usual_video_model(P),context],3]).
query('#785203',[Length,N],[genre(S,rock),how_much(S,N),religious(S,christian),playlist(S,P),length(P,Length)],2).
query('#785088',[Chord],[title(W,aleichem),religious(W,jewish),chord(W,Chord)],2).
query('#784871',[P],[performance_of(heartandsoul,P),recorded(P,V),artist(heartandsoul,carmichael),downloaded(V,itunes),context,singer(P,S),gender(S,male),instrument(P,strings),sounds_like(P,'60s'),performance_of(A,P),similar_to(A,oohbabybaby),similar_to(S,smokey),different_from(P,cleftone)],9). %similar arrangements?
query('#784805',[Place],[instrumental_perfomance_of(S,P),recording(P,Version),sold_at(Version,Place),lyrics(S,Lyrics),clue(Lyrics,l)],2).
query('#784674',[A],[broadcast(Song,B),service(B,radio),end(B,End),dj_says(End,boston),not_artist(Song,nin),genre(Song,indus),instrument(Song,drums),lyrics(Song,Lyrics),contains(Lyrics,clue),length(Song,ten),context,artist(Song,A)],8).
query('#784406',[W],[composed_in(C,W),time(C,T),during(T,'mid80s'),genre(W,poprock),performed(W,P),performer(P,A),sounds_like(A,mikemechanics),lyrics(C,L),contains(L,clue)],7]).
query('#784346',[Pl],[sold_at(Item,Pl),item_for(Item,homecomingdance)],1).
query('#784310',[A],[artist(S,A),genre(S,ranchera),lyrics(S,L),contains(L,clue),played_a_lot_on(S,service),location(service,columbia)],4).
query('#783992',[V],[performance_of(angels,P),artist(angels,dishwalla),featured(TV,P),during(TV,smallvilebroadcast),during(P,liveatthelounge)],4).
query('#783805',[L],[lyrics(P,L),author(L,orwell),performance_of(internationale,P)],3).
query('#783223',[Title],[broadcast(V,B),service(B,mtv),featured(V,B),genre(B,punk),depicted_place(V,forest),singer_in_video(V,S),trapped_under(S,ice),title(V,Title)],4).
query('#783125',[Name,Place],[title(Song,Name),sold_at(Song,Place),genre(Song,electronica),genre_slightly(Song,hiphop),lyrics(Song,L),most_language(L,french),contains(L,longtermfocus),repeated(S,longtermfocus),played(Song,Played),place(Played,lobby),time(Played,nov)],6).
query('#782545',[Name,A],[title(Song,Name),time(Song,T),during(T,earlynineties),artist(Song,A),lots_of_broadcasts_between(Song,'93-95'),lyrics(Song,L),contains(L,paytherent),emotion(Song,intense),genre(Song,rock)],5).
query('#782533',[Song],[context,start(Song,Start),emotion(Start,peaceful),slowly_builds_up(Start,Duration),magnificent_combination(Start,Duration),event_every_10_s_or_so(Song,sunrise),genre(Song,trance),not_longer_than(Song,ten)],3).
query('#782460',[Place,Time],[place(Comp,Place),genre(Comp,freestyle),close_to(Place,boston),as_far_as(Place,nyc),time(Comp,Time),context],3).
query('#782140',[L2,H,Mp3],[title(Song,gutermond),lyrics(Song,L),translation(L,L2),language(L2,english),history(Song,H),available_as(Song,Mp3)],5).
query('#781933',[Song],[title(Song,untitled),artist(Song,anniversary)],2).
query('#781688',[License],[myspace(Profile),license(Profile,License)],0).
query('#781133',[Song],[lyrics(Song,L),context,learned_by_someone_borned_in(L,midlands),contains(L,clue)],1).
query('#781103',[Future],[future_of(electronic,Future)],0).
query('#780627',[Venue],[place(Venue,Place),in(Place,england),genre(Venue,rock),context,order_by(Place)],4).
query('#780488',[Song],[played_a_lot_on(Song,S),service_in(S,turkey),service_time(S,'2002'),emotion(Song,calm),instrument(Song,flute),uncertain_instrument(Song,drums),language_uncertain(Song,turkish),singer(Song,Singer),gender(Singer,male),theme(Song,Theme),played_by(Theme,Singer),played_by(Theme,flute),end(Song,End),emotion(End,stronger),melody_similar_to(Song,ccdef)],8).
query('#780431',[Title],[name(Song,Title),context,at_least_yr_old(5,Song),played_a_couple_of_times(Song,S),service_in(S,australia),start(Song,Start),available_as(Start,D)],4).
query('#780175',[Place],[sold_at(Rec,Place),title(Rec,pizza),artist(Rec,jack),description(Rec,desc),isbn(Rec,isbn),medium(Rec,cd),copyright(Rec,copyright)],6).
query('#779787',[Name,Title],[name(Band,Name),time(Band,early80s),genre(Band,pop),made(Band,Album),title(Album,Title),based_near(Band,ohio),signed_on(Band,capitol),member(Band,P1,P2,P3),brother(P1,P2)],7).


% solve featured

