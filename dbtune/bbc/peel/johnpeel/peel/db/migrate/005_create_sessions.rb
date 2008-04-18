class CreateSessions < ActiveRecord::Migration
  def self.up
    create_table :sessions do |t|
      # t.column :name, :string
    end
  end

  def self.down
    drop_table :sessions
  end
end
