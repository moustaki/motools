class FestiveFifty < ActiveRecord::Base
	belongs_to :artist
	
	# Year of festive 50 to display
	def display_year
		if year == 0
			'Millenium'
		else
			year
		end
	end
end
