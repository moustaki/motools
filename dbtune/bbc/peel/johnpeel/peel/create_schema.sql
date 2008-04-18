# Artists table
drop table if exists artists;

create table artists (
id int(4) unsigned not null,
name varchar (250),
image varchar (250),
biog text,
url_key char(5),
primary key (id)
);
	
	
# Festive 50s table	
drop table if exists festive_fifties;

create table festive_fifties (
id int (4) unsigned not null auto_increment,
artist_id int(4),
year int(4),
chart_position int(3),
track_title varchar(250),
folder int(4),
isrc varchar(50),
file varchar(50),
url_key char(5),
constraint fk_artist foreign key (artist_id) references artists(id),
primary key (id)
);
	
	
# Sessions table
drop table if exists sessions;

create table sessions (
artist_id int(4),
id int(4),
tx_date date,
record_date date,
producer varchar(50),
engineer1 varchar(50),
engineer2 varchar(50),
studio varchar(50),
url_key char(5),
constraint fk_artist foreign key (artist_id) references artists(id),
primary key (id)
);
	
	
# Session band members table
drop table if exists session_band_members;

create table session_band_members (
id int (4) unsigned not null auto_increment,
session_id int(4),
performer varchar(75),
instrument varchar(75),
constraint fk_session foreign key (session_id) references sessions(id),
primary key (id)
);
	
	
# Session tracks table
drop table if exists session_tracks;

create table session_tracks(
id int (4) unsigned not null auto_increment,
session_id int(4),
track_title varchar (50),
file varchar(50),
constraint fk_session foreign key (session_id) references sessions(id),
primary key (id)
);
	

# url_keys table
drop table if exists url_keys;

create table url_keys (
count int not null
);
