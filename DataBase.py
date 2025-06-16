import json
import os
from collections import defaultdict


class Database:

    def __init__(self, filename='database.json'):
        self.filename = filename
        self.tables = {}
        self.indexes = defaultdict(dict)
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tables = data.get('tables', {})
                self.indexes = defaultdict(dict, data.get('indexes', {}))

    def save(self):
        data = {
            'tables': self.tables,
            'indexes': dict(self.indexes)
        }

        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def create_table(self, table_name):
        if table_name not in self.tables:
            self.tables[table_name] = {}
            self.save()

    def insert(self, table, record_id, record):
        if table not in self.tables:
            self.tables[table] = {}
        self.tables[table][record_id] = record
        self._update_indexes(table, record_id, record)
        self.save()

    def _update_indexes(self, table, record_id, record):
        if table in self.indexes:
            for i in self.indexes[table]:
                if i in record:
                    field_value = record[i]
                    if field_value not in self.indexes[table][i]:
                        self.indexes[table][i][field_value] = []
                    if record_id not in self.indexes[table][i][field_value]:
                        self.indexes[table][i][field_value].append(record_id)

    def create_index(self, table, field):
        if table not in self.tables:
            return False

        self.indexes[table][field] = {}

        for record_id, record in self.tables[table].items():
            if field in record:
                value = record[field]
                if value not in self.indexes[table][field]:
                    self.indexes[table][field][value] = []
                self.indexes[table][field][value].append(record_id)

        self.save()
        return True

    def query(self, table, field, value):
        if table in self.indexes and field in self.indexes[table]:
            return[
                self.tables[table][record_id]
                for record_id in self.indexes[table][field].get(value, [])
            ]

        return []

    def get(self, table, record_id):
        table_data = self.tables.get(table, {})
        return table_data.get(record_id)

    def get_all(self, table):
        return self.tables.get(table, {})

    def update(self, table, record_id, new_values):
        if table not in self.tables or record_id not in self.tables[table]:
            return False

        self.tables[table][record_id].update(new_values)
        self._update_indexes(table, record_id, self.tables[table][record_id])

    def delete(self, table, record_id):
        if table not in self.tables or record_id not in self.tables[table]:
            return False

        if table in self.indexes:
            for field in self.indexes[table]:
                field_value = self.tables[table][record_id].get(field)
                if field_value in self.tables[table][field]:
                    self.indexes[table][field][field_value].remove(record_id)
                    if not self.indexes[table][field][field_value]:
                        del self.indexes[table][field][field_value]

        del self.tables[table][record_id]

        self.save()
        return True