class CreateSessionBandMembers < ActiveRecord::Migration
  def self.up
    create_table :session_band_members do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :session_band_members
  end
end
