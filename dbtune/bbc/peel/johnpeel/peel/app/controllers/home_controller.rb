class HomeController < ApplicationController

	# Home page
	def index
		@artist_count = Artist.count
		@festive_fifty_track_count = FestiveFifty.find(:all,
			:group => 'year')
		@session_count = Session.count
	end
end