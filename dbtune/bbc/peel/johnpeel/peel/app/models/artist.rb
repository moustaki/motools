class Artist < ActiveRecord::Base
	has_many :sessions,
		:order => 'tx_date'
	has_many :festive_fifties,
		:order => 'chart_position, year desc'
end
