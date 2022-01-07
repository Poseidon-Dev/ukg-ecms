import json
import requests
import os
from datetime import datetime as dt

from src.conn import UKGApi
from src.models import Employee

from core.defaults import TESTING

__all__ = ['EmployeeChanges',]

class EmployeeChanges(UKGApi):

    module = 'personnel'
    method = 'employee-changes'

    def __init__(self):
        self.tracker = []
        super().__init__()


    def fetch(self):
        """
        A method for fetching all employee records from the API, storing the json locally
        and returns the changes between the two most recently fetched datasets
        """
        if not TESTING:
            self._post_request()
        return self.logged_changes()


    def _post_request(self, version='v1'):
        """
        Get request from the employee changes API
        grabs all records until no records are returned from API
        and returns all results
        """
        url = f'{self.base_url}{self.module}/{version}/{self.method}'
        page = 1
        record_check = 1
        results = []
        while record_check >= 1:
            params = {'page': page, 'per_page': 100}
            result = requests.get(url=url, auth=self.auth, headers=self.headers, params=params).json()
            results.extend(result)
            record_check = len(result)
            page += 1

        self._dump(results)
        return results


    def _dump(self, results, filetype='json', dir='dumps/'):
        """
        Saves results as a json file in the /dumps directory
        with the YearMonthDay_HourMinute of the current fetch
        """
        dt_format = '%Y%m%d_%H%M'
        filename = f'{dir}{dt.now().strftime(dt_format)}.{filetype}'

        with open(filename, 'w') as out:
            json.dump(results, out)
    

    def load_records(self):
        """
        Converted the two most recent files into list of Employees
        Returns a tuple containing the results
        """
        records = self.current_files()
        data1 = json.load(open(records[0]))
        data2 = json.load(open(records[1]))

        records1 = [Employee(e) for e in data1]
        records2 = [Employee(e) for e in data2]

        return (records1, records2)


    def changes(self, instance, other):
        """
        Checks to see if the employees match and if they do
        logs the changes differences and appends the Instance as a key
        """
        if not isinstance(other, Employee) and not isinstance(instance, Employee):
            return NotImplemented
        if instance == other:
            diffs = {}
            changes = {
                k: {
                    'new': other.__dict__[k],
                    'old': instance.__dict__[k]
                    }
                for k in instance.__dict__
                if other.__dict__[k] != instance.__dict__[k]
            }
            if changes:
                diffs['employee'] = instance
                diffs['changes'] = changes
                self.tracker.append(diffs)
            else:
                return False


    def logged_changes(self):
        """
        Looks at the two most recently fetched records and 
        appends the dictionary to the class list to store
        any differences found between files
        """
        records = self.load_records()
        for record in records[0]:
            for new_record in records[1]:
                self.changes(record, new_record)

        return self.tracker


    @staticmethod
    def current_files():
        """
        Checks the dump directory for store json files
        and returns the two most recent dumps
        """
        path = os.getenv('DUMP_PATH')
        paths = sorted([
            os.path.abspath(os.path.join(dirpath, f))
            for dirpath,_,file_names in os.walk(path)
            for f in file_names
            if f.split('.')[1] == 'json'
        ], reverse=True)
        return sorted(paths[:2])


    @staticmethod
    def deletions(instance, other):
        pass


    @staticmethod
    def additions(instance, other):
        pass
