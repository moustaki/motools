ActionController::Routing::Routes.draw do |map|
  # The priority is based upon order of creation: first created -> highest priority.
  
  # Sample of regular route:
  # map.connect 'products/:id', :controller => 'catalog', :action => 'view'
  # Keep in mind you can assign values other than :controller and :action

  # Sample of named route:
  # map.purchase 'products/:id/purchase', :controller => 'catalog', :action => 'purchase'
  # This route can be invoked with purchase_url(:id => product.id)

  # You can have the root of your site routed by hooking up '' 
  # -- just remember to delete public/index.html.
  map.connect '',
		:controller => 'home'

  # Allow downloading Web Service WSDL as a file with an extension
  # instead of a file named 'wsdl'
  map.connect ':controller/service.wsdl', :action => 'wsdl'
	
	# Artist stuff
	map.list_artist 'artist',
		:controller => 'artist',
		:action => 'index'
	map.show_artist 'artist/:url_key',
		:controller => 'artist',
		:action => 'show'
	
	# Festive 50 stuff
	map.list_festive_fifties 'festive50',
		:controller => 'festive50',
		:action => 'index'
	map.show_festive_fifty 'festive50/:year',
		:controller => 'festive50',
		:action => 'show'
	
	# Session stuff
	map.list_session_years 'session',
		:controller => 'session',
		:action => 'index'
	map.session_date 'session/:year/:month',
		:controller => 'session',
		:action => 'show_date',
		:requirements => {
			:year => /(19|20)\d\d/,
			:month => /[01]?\d/,
		},
		:month => nil
	map.list_sessions_with_unknown_tx_dates 'session/unknown_tx_date',
		:controller => 'session',
		:action => 'list_sessions_with_unknown_tx_date'		
	map.show_session 'session/:url_key',
		:controller => 'session',
		:action => 'show'

  # Install the default route as the lowest priority.
  map.connect ':controller/:action/:id'
end
