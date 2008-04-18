require File.dirname(__FILE__) + '/../test_helper'
require 'artist_controller'

# Re-raise errors caught by the controller.
class ArtistController; def rescue_action(e) raise e end; end

class ArtistControllerTest < Test::Unit::TestCase
  def setup
    @controller = ArtistController.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  # Replace this with your real tests.
  def test_truth
    assert true
  end
end
