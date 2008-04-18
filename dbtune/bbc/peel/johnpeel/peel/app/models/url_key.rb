class UrlKey < ActiveRecord::Base

	CHARS = "gjfbw9d6xp3m2nq58v4crhz".split(//)
	BASE = CHARS.length
	
	def self.get_next
		i = self.get_counter
		urlkey = ""
		index = 0
		while urlkey.length < 5
			i, remainder = i.divmod(BASE)
			index = (index + urlkey.length + remainder) % BASE
			urlkey = urlkey + CHARS[index]
		end
		return urlkey
	end
	
private
	
	def self.get_counter
		counter = self.find(:first)
		if counter.nil?
			counter = UrlKey.create( :count => 0 )
		end
		counter.count += 1
		self.update_all [ "count = ?", counter.count ]
		return counter.count
	end
end