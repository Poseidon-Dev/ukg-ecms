# UKG - ECMS Employee Record Integration

UKG - ECMS Employee Record Integration is an application that maintains the changes that took place at a given interval in the UKG system and updates the corresponding records that are found in eCMS

## Authors

**[Johnny Whitworth (@Poseidon-dev)](https://github.com/poseidon-dev)** 

## Requirements
requests
ecms-api - https://github.com/Poseidon-Dev/ecms-api

## How to use Examples

The primary class for gathering data is the EmployeeChanges class
The fetch method will compile all api requests and post them in the dumps container. 
The file name will be the request date and time. 

Records are a list of dictionaries
And the employee record is of class Employee, not an integer. 

```python
service = EmployeeChanges()
records = service.fetch()
```

Will return
```python
{'employee': 12345, 'changes': {'org_level_1': {'new': 'NEW', 'old': 'OLD'}}}, 
{'employee': 23456, 'changes': {
				'job_code': {'new': 'SAWCUT', 'old': 'LABORER'}, 
                'date_in_job': {'new': '12/27/2021 12:00:00 AM', 'old': '12/1/2021 12:00:00 AM'}}}, 
```


By pairing with the ecms-api
Records can be updated based on changes found in UKG

The following can be responsibile for pushing changes found into the ecms system
Any values in the lookup table that are an empty list will be ignored

```python
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
```

This will generate and execute the following query. Queries are also based on the records that are currently found within
ecms so values will be pulled and compared prior to execution.

```sql
UPDATE
FROM CMSFIL.HRTEMP
SET DEPTNO = 'NEW' WHERE EMPLOYEENO = '12345' AND COMPANYNO = '1'
```

## Future update
- [ ] Task Async at 2 hour intervals


## Support

If you need some help for something, please reach out to me directly or submit an issue and I'll get to it as soon as I can

## Site

https://poseidon-dev.github.io/ecms-api/
