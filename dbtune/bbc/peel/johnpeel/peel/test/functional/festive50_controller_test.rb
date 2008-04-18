require File.dirname(__FILE__) + '/../test_helper'
require 'festive50_controller'

# Re-raise errors caught by the controller.
class Festive50Controller; def rescue_action(e) raise e end; end

class Festive50ControllerTest < Test::Unit::TestCase
  def setup
    @controller = Festive50Controller.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  # Replace this with your real tests.
  def test_truth
    assert true
  end
end
