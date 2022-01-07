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
            for v in value:
                if v:
                    update = SQLQuery(HRTEMP).update()
                    update.set(v['col'], v['result'])
                    employeeno = record['employee'].employee_number
                    companyno = Lookup(record=record).company_lookup()
                    update.filters(employeeno=employeeno, companyno=companyno)
                    print(update.command) 
                    # update.query()

print(time.perf_counter() - start)

