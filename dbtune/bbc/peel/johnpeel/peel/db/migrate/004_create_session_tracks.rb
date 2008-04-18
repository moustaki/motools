class CreateSessionTracks < ActiveRecord::Migration
  def self.up
    create_table :session_tracks do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :session_tracks
  end
end
