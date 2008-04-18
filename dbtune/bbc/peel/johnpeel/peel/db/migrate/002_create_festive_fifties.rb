class CreateFestiveFifties < ActiveRecord::Migration
  def self.up
    create_table :festive_fifties do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :festive_fifties
  end
end
