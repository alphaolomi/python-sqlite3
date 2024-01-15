import sqlite3
import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from sqlite3 import IntegrityError
from module.sqlite3_crud import insert, retrieve, update, delete, disp_rows, main

class TestSQLiteCRUD(unittest.TestCase):

    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row
        self.db.execute('create table test ( t1 text, i1 int )')

    def tearDown(self):
        self.db.close()

    def test_insert_retrieve(self):
        insert(self.db, dict(t1='test_insert', i1=42))
        result = dict(retrieve(self.db, 'test_insert'))
        self.assertEqual(result, {'t1': 'test_insert', 'i1': 42})

    def test_update(self):
        insert(self.db, dict(t1='test_update', i1=42))
        update(self.db, dict(t1='test_update', i1=99))
        result = dict(retrieve(self.db, 'test_update'))
        self.assertEqual(result, {'t1': 'test_update', 'i1': 99})

    def test_delete(self):
        insert(self.db, dict(t1='test_delete', i1=42))
        delete(self.db, 'test_delete')
        result = retrieve(self.db, 'test_delete')
        self.assertIsNone(result)

    def test_disp_rows(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            insert(self.db, dict(t1='disp_row_test', i1=42))
            disp_rows(self.db)
            output = mock_stdout.getvalue().strip()
            self.assertIn('disp_row_test', output)
            self.assertIn('42', output)

    def test_main_integration(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main_output = StringIO()
            with redirect_stdout(main_output):
                main()
            main_output = main_output.getvalue().strip()

        self.assertIn('Create table test', main_output)
        self.assertIn('Create rows', main_output)
        self.assertIn('Retrieve rows', main_output)
        self.assertIn('Update rows', main_output)
        self.assertIn('Delete rows', main_output)

if __name__ == '__main__':
    unittest.main()