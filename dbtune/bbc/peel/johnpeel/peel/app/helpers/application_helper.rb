# Methods added to this helper will be available to all templates in the application.
module ApplicationHelper
	
	# function to work out font size for tag cloud from DP
	def font_size_for_tag_cloud( item_total, min_max, options={} )
		# options
		max           = options.delete( :max_size )   || 400
		min           = options.delete( :min_size )   || 100
		max_color     = options.delete( :max_color )  || [ 170, 0, 0 ]
		min_color     = options.delete( :min_color )  || [ 230, 0, 0 ]
		show_sizes    = options.delete( :sizes )      || true
		show_colours  = options.delete( :colours )    || false

		# function to work out rgb values
		def s( a, b, i, x)
			if x == 1
				v = b
			else
				if a > b
					m = (a-b)/Math.log(x)
					v = a-(Math.log(i)*m).floor
				else
					m = (b-a)/Math.log(x)
					v = (Math.log(i)*m+a).floor
				end
			end
			return v
		end

		if item_total > 0
			# vars
			spread = min_max[:max] - min_max[:min] unless min_max.blank?
			spread = 100 if spread.blank? or spread <= 0
			fontspread = max - min
			
			# Had to add this to DPs script cos if the fontspread > spread get a divide by zero
			if (spread > fontspread)
				fontstep = spread / fontspread
			else
				fontstep = fontspread / spread
			end
			# End of added bit
			
			# work out colours
			c = []
			(0..2).each { |i| c[i] = s( min_color[i], max_color[i], item_total, min_max[:max] ) }
			
			# final size
			size = ( min + ( ( item_total - min_max[:min] ) * fontstep ) )
			size = max if size > max
			colors = "#{c[0]},#{c[1]},#{c[2]}"
		else
			size = min
			colors = "#{ min_color.join(',') }"
		end
		size_tag = "font-size:#{ size.to_s }%;" if show_sizes
		color_tag = "color:rgb(#{ colors });" if show_colours
		return "#{ size_tag }#{ color_tag }"
	end
end
