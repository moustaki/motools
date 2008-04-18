class Session < ActiveRecord::Base
	belongs_to :artist
	has_many :session_band_members
	has_many :session_tracks
	
	# Transmission date of session to display
	def display_tx_date
		if tx_date == nil
			'Unknown'
		else
			tx_date.strftime('%B %d, %Y')
		end
	end
	
	# Record date of session to display
	def display_record_date
		if record_date == nil
			'Unknown'
		else
			record_date.strftime('%B %d, %Y')
		end
	end
	
	# Producer of session to display
	def display_producer
		if producer == nil or producer == ''
			'Unknown'
		else
			producer
		end
	end
	
	# Venue of session to display
	def display_studio
		if studio == nil or studio == ''
			'Unknown'
		else
			studio
		end
	end
end
