class CreateArtists < ActiveRecord::Migration
  def self.up
    create_table :artists do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :artists
  end
end
