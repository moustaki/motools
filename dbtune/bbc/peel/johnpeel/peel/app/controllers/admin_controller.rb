class AdminController < ApplicationController

	# Add url_key to artists table
	def add_url_key_to_artists
		@artists = Artist.find(:all)
		@artists.each do |a|
			a.url_key = UrlKey.get_next
			a.save
		end
	end

	# Add url_key to sessions table
	def add_url_key_to_sessions
		@sessions = Session.find(:all)
		@sessions.each do |s|
			s.url_key = UrlKey.get_next
			s.save
		end
	end

	# Add url_key to festive fifties table
	# Turns out this is unused - use year instead
	def add_url_key_to_festive_fifties
		@festive_fifties = FestiveFifty.find(:all)
		@festive_fifties.each do |ff|
			ff.url_key = UrlKey.get_next
			ff.save
		end
	end
end
