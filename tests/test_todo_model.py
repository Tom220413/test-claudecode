import pytest
import sqlite3
import os
from todo_model import TodoModel


class TestTodoModel:
    
    def setup_method(self):
        self.db_path = 'test_todo.db'
        self.todo_model = TodoModel(self.db_path)
    
    def teardown_method(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_add_todo_item(self):
        item_id = self.todo_model.add_item("Test task")
        assert item_id is not None
        assert isinstance(item_id, int)
    
    def test_get_all_items(self):
        self.todo_model.add_item("Task 1")
        self.todo_model.add_item("Task 2")
        items = self.todo_model.get_all_items()
        assert len(items) == 2
        assert items[0]['text'] == "Task 1"
        assert items[1]['text'] == "Task 2"
        assert items[0]['completed'] is False
        assert items[1]['completed'] is False
    
    def test_toggle_completion(self):
        item_id = self.todo_model.add_item("Test task")
        self.todo_model.toggle_completion(item_id)
        items = self.todo_model.get_all_items()
        assert items[0]['completed'] is True
        
        self.todo_model.toggle_completion(item_id)
        items = self.todo_model.get_all_items()
        assert items[0]['completed'] is False
    
    def test_empty_list_initially(self):
        items = self.todo_model.get_all_items()
        assert len(items) == 0
    
    def test_persistence_across_instances(self):
        self.todo_model.add_item("Persistent task")
        
        new_model = TodoModel(self.db_path)
        items = new_model.get_all_items()
        assert len(items) == 1
        assert items[0]['text'] == "Persistent task"
    
    def test_add_item_empty_text_raises_error(self):
        with pytest.raises(ValueError, match="Todo text cannot be empty"):
            self.todo_model.add_item("")
        
        with pytest.raises(ValueError, match="Todo text cannot be empty"):
            self.todo_model.add_item("   ")
        
        with pytest.raises(ValueError, match="Todo text cannot be empty"):
            self.todo_model.add_item(None)
    
    def test_add_item_too_long_text_raises_error(self):
        long_text = "a" * 201
        with pytest.raises(ValueError, match="Todo text cannot exceed 200 characters"):
            self.todo_model.add_item(long_text)
    
    def test_add_item_exactly_200_chars_works(self):
        exactly_200_chars = "a" * 200
        item_id = self.todo_model.add_item(exactly_200_chars)
        assert item_id is not None
        items = self.todo_model.get_all_items()
        assert len(items) == 1
        assert items[0]['text'] == exactly_200_chars
    
    def test_toggle_completion_invalid_id_raises_error(self):
        with pytest.raises(ValueError, match="Todo item with ID 999 not found"):
            self.todo_model.toggle_completion(999)