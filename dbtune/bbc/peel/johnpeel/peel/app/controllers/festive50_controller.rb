class Festive50Controller < ApplicationController

	# List years
	def index
		@years = FestiveFifty.find(:all,
			:group => 'year',
			:order => 'year desc')
	end
	
	# Show festive 50 for given year
	def show
		@tracks = FestiveFifty.find(:all,
			:conditions => ['year = ?', params[:year]],
			:order => 'chart_position')
	end
end
