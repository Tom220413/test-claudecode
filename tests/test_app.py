import pytest
import os
import tempfile
from app import app


class TestApp:
    
    def setup_method(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        
    def teardown_method(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_index_page_shows_todo_list(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'Todo List' in response.data
    
    def test_add_new_todo_item(self):
        response = self.client.post('/add', data={'task': 'Test task'})
        assert response.status_code == 302  # Redirect after POST
        
        response = self.client.get('/')
        assert b'Test task' in response.data
    
    def test_toggle_todo_completion(self):
        self.client.post('/add', data={'task': 'Test task'})
        
        # Toggle completion
        response = self.client.post('/toggle/1')
        assert response.status_code == 302  # Redirect after POST
        
        response = self.client.get('/')
        assert b'checked' in response.data
    
    def test_empty_todo_list_initially(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'No todos yet' in response.data or b'Todo List' in response.data
    
    def test_add_multiple_todos(self):
        self.client.post('/add', data={'task': 'Task 1'})
        self.client.post('/add', data={'task': 'Task 2'})
        
        response = self.client.get('/')
        assert b'Task 1' in response.data
        assert b'Task 2' in response.data