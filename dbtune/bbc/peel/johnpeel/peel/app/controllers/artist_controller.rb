class ArtistController < ApplicationController

	# List artists
	def index
		@artists = Artist.find(:all,
			:order => 'name')	
	end
	
	# Show an artist
	def show
		@artist = Artist.find_by_url_key(params[:url_key])
	end
end