class SessionController < ApplicationController

	# Shows years with sessions
	def index
		@years = Session.find(:all,
			:select => 'substring(tx_date, 1, 4) as year',
			:conditions => 'substring(tx_date, 1, 4) != 0000',
			:group => 'year',
			:order => 'year desc')
		@sessions_with_unknown_tx_date = Session.find(:all,
			:conditions => 'tx_date is null')
	end
	
	# Show date
	def show_date
		if params[:month]
			show_month
		else
			show_year
		end
	end
	
	# Show year
	def show_year
		@months = Session.find(:all,
			:select => 'substring(tx_date, 6, 2) as month',
			:conditions => ["substring(tx_date, 1, 4) = :year", params],
			:group => 'month',
			:order => 'month')
			
		render :action => 'show_year'
	end
	
	# Show month
	def show_month
		@peel_sessions = Session.find(:all,
			:conditions => ["substring(tx_date, 1, 4) = :year and substring(tx_date, 6, 2) = :month", params])
			
		render :action => 'show_month'
	end
	
	# List sessions with unknown transmission dates
	def list_sessions_with_unknown_tx_date
		@sessions = Session.find(:all,
			:conditions => 'tx_date is null')
	end
	
	# Show session
	def show
		@peel_session = Session.find_by_url_key(params[:url_key])
		puts @session.inspect
	end
end
