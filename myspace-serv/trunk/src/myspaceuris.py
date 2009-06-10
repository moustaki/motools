#########################################################################################################
# mysapce urls / uris of interest
viewProfileURLbase = "http://profile.myspace.com/index.cfm?fuseaction=user.viewprofile&friendid="
www_myspace = "http://www.myspace.com/"

#						### append user id to this ###
rdfStoreURL = "http://myrdfspace.com/alpha/"

myspaceOntology = 'http://purl.org/ontology/myspace#'


#########################################################################################################

#########################################################################################################
# useful tags
playerTag = """SWFObject("http://musicservices.myspace.com/Modules/MusicServices/Services/Embed.ashx/ptype=4""", ''';'''
#						###	this tag will be terminated by a '.' ###
#<td bgcolor="FFFFFF" align="center" valign="top" width="107" style="word-wrap:break-word">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t
friendTag = '''&nbsp;<a href="http://www.myspace.com/''', '''"'''
# new tag updated 13/1/2009
#"""&nbsp;<a href="http://profile.myspace.com/index.cfm?fuseaction=user.viewprofile&friendid=""", '''"'''
#						### tag will be terminated by a '"' ###
friendNameTag = """_friendLink">""", '''<'''
						### tag terminated by '<' ###
userIDTag = '''"DisplayFriendId":''', ''',"IsLoggedIn"'''
# 13/1/2009
#"""<script type="text/javascript" >var MySpaceClientContext = {"UserId":-1,"DisplayFriendId":""", ''','''
						### tag terminated by ',' ###
#userIDTag = """function getDisplayFriendID() { return """
#						### tag terminated by a ';' ###
nameTag = """<span class="nametext">""", '''<'''
#						### tag term by '<'

non_artist_name_split = ''' |'''

genreTag = '''MySpace.Ads.BandType = {''', '''}'''
#genreTag = '''<font color="#033330" size="1" face="Arial, Helvetica, sans-serif"><strong>\r\n\t\t\t\t\t''', ''' \r'''
#'''<font color="#033330" size="1" face="Arial, Helvetica, sans-serif"><strong>''', '''<'''
#						### tag terminated by '<'
niceURLTag = '''<td><div align="left">&nbsp;&nbsp;<span><a href="''', '''">'''
#						### terminated by '&'
picTag = """href="http://viewmorepics.myspace.com/index.cfm?fuseaction=user.viewAlbums&amp;friendID=""", '''"'''
#						### + self.uid + '''<img src="'''  term with '"'
friendPicTag = '''_friendImageLink"><img src="''', '''"'''
#						### term w/ '""

###
#these two tag scraps are provisional for grabbing the ArtistID and playlist number, which are now nessecary to grab audio
#both of these should be terminated by a comma
playlistIDtag = """plid=""", '''&'''
#artistIDtag = """artid=""",'''&'''
artistIDtag = '''"DisplayFriendId":''',''','''

#########################################################################################################

# myspace uri for downloads  ----this has gotten a bit more complicated in the roll out of myspace's new media player
# this xml file gives the songIDs, the songsIDs must be used individually to request another xml file that then contains the uri to the cached media
#
#
mediaBase = "http://musicservices.myspace.com/Modules/MusicServices/Services/MusicPlayerService.ashx?artistId=","&playlistId=","&artistUserId=","&action=getArtistPlaylist"

#Here's the base to grab the aforementioned song xml file with the cached file location
#
songBase = "http://musicservices.myspace.com/Modules/MusicServices/Services/MusicPlayerService.ashx?songId=","&action=getSong"

defaultdlpath = "./MyspaceMusic/"
defaultRDFpath = ""

#these are the base urls used for writing links.  Hardcoding them is a terrible idea that we need to sort out...
#Also if they are going to be hard coded it should be consistant with respect to the ftp upload...
#leave out the http:// prefix, then this can be referenced by the ftp upload as well which will keep everything consistant
# rdfStoreURL = "myrdfspace.com/person_seed_134901208/"
# rdfStoreMediaURL = "myrdfspace.com/media_seed_134901208/"
rdfStoreURL = "myrdfspace.com/myspace/MusicArtist/"
rdfStoreMediaURL = "myrdfspace.com/myspace/MusicArtist/"
mp3Store = "file:///Datastore/group/omras2/media/myspace_sample/" 

#adding this back in to lessen the broken...
dbtune = 'http://dbtune.org/myspace/'

#new dict for genres valid as of 2009 feb 3
genreDict = {0:"", 61:"2-step", 59:"A'cappella", 125:"Acousmatic / Tape music", 1:"Acoustic", 73:"Afro-beat", 2:"Alternative", 3:"Ambient", 93:"Americana", 98:"Anime Song", 65:"Big Beat", 51:"Black Metal", 4:"Bluegrass", 5:"Blues", 105:"Bossa Nova", 60:"Breakbeat", 129:"Breakcore", 118:"Celtic", 109:"Children", 134:"Chinese pop", 135:"Chinese traditional", 6:"Christian", 7:"Christian Rap", 8:"Classic Rock", 77:"Classical", 110:"Classical - Opera and Vocal", 9:"Club", 10:"Comedy", 126:"Concrete", 11:"Country", 12:"Death Metal", 63:"Disco House", 70:"Down-tempo", 50:"Drum & Bass", 68:"Dub", 123:"Dutch pop", 67:"Electro", 127:"Electroacoustic", 13:"Electronica", 14:"Emo", 133:"Emotronic", 15:"Experimental", 107:"Flamenco", 16:"Folk", 17:"Folk Rock", 119:"French pop", 18:"Funk", 124:"Fusion", 56:"Garage", 120:"German pop", 79:"Glam", 112:"Gospel", 46:"Gothic", 95:"Grime", 47:"Grindcore", 19:"Grunge", 71:"Happy Hardcore", 57:"Hard House", 20:"Hardcore", 104:"Healing & EasyListening", 21:"Hip Hop", 22:"House", 69:"IDM", 97:"Idol", 23:"Indie", 45:"Industrial", 121:"Italian pop", 24:"Jam Band", 103:"Japanese Classic Music", 100:"Japanese Pop", 25:"Jazz", 58:"Jungle", 101:"Korean Pop", 49:"Latin", 128:"Live Electronics", 75:"Lounge", 113:"Lyrical", 102:"Melodramatic Popular Song", 26:"Metal", 131:"Minimalist", 76:"New Wave", 66:"Nu-Jazz", 27:"Other", 28:"Pop", 29:"Pop Punk", 130:"Post punk", 31:"Powerpop", 32:"Progressive", 62:"Progrsv House", 33:"Psychedelic", 43:"Psychobilly", 34:"Punk", 35:"R&B", 36:"Rap", 37:"Reggae", 111:"Religious", 38:"Rock", 44:"Rockabilly", 94:"Roots Music", 115:"Salsa", 116:"Samba", 39:"Screamo", 78:"Shoegaze", 96:"Showtunes", 40:"Ska", 41:"Soul", 106:"Soundtracks / Film music", 42:"Southern Rock", 122:"Spanish pop", 48:"Surf", 114:"Swing", 108:"Tango", 53:"Techno", 54:"Thrash", 52:"Trance", 132:"Trance", 55:"Trip Hop", 92:"Tropical", 99:"Visual", 117:"Zouk"}

def setRDFStoreURL(url):
	'''set the rdf uri path'''
	rdfStoreURL = url
	
