from src import EmployeeChanges
from src.lookup import Lookup
import time

from ecmsapi import SQLQuery
from ecmsapi.tables import HRTEMP

start = time.perf_counter()

service = EmployeeChanges()
records = service.fetch()

print(records)
 
for record in records:
    for col, change in record['changes'].items():
        value = Lookup(col, change, record).lookup
        if value:
            for val in value:
                update = SQLQuery(HRTEMP).update()
                update.set(val['col'], val['result'])
                employeeno = record['employee'].employee_number
                companyno = Lookup(record=record).company_lookup()
                update.filters(employeeno=employeeno, companyno=companyno)
                update.query()

print(time.perf_counter() - start)

