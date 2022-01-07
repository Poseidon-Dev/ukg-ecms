from ecmsapi import SQLQuery
from ecmsapi.tables import HRTEMP

select = SQLQuery(HRTEMP).select()

class Lookup:

    divisions = {
        'TUC': 1,
        'PHX': 2,
        'HDS': 3,
        'COR': 4, 
        'VGS': 5,
        'PPL': 6,
        'NNV': 7,
        'CCT': 8,
        'PAC': 9,
        'BHC': 10,
        'IEM': 11,
    }
    departments = {
        '01': 1,
        '02': 2,
        '03': 3,
        '04': 4,
        '05': 5,
        '06': 6,
        '07': 7,
        '08': 8,
        '09': 9,
    }

    def __init__(self, lookup=None, change=None, record=None):
        self._lookup = lookup
        self.change = change
        if change:
            self.val = change['new']
        self.record = record


    @property
    def lookup(self):
        table = {
            'company_name' : [],
            'first_name' : self.parse_name(),
            'middle_name' : self.parse_name(),
            'last_name' : self.parse_name(),
            'is_active' : self.inactive_lookup(),
            'org_level_1' : self.parse_dept(),
            'org_level_2' : self.parse_dept(),
            'employee_status' : self.inactive_lookup(),
            'employee_number' : ['EMPLOYEENO'],
            'hire_date' : ['REHIREDATE'],
            'date_of_last_hire' : ['REHIREDATE'],
            'org_level_3' : [],
            'org_level_4' : [],
            'employee_status_start_date' : [],
            'termination_date' : [],
            'preferred_name' : [],
            'email_address' : [],
            'work_phone' : [],
            'country_code' : [],
            'language_code' : [],
            'employee_id' : [],
            'person_id' : [],
            'user_integrated_key' : [],
            'company_id' : [],
            'salary_or_hourly' : [],
            'supervisor_id' : [],
            'fulltime_or_parttime' : [],
            'work_location_code' : [],
            'job_code' : [],
            'project_code' : [],
            'home_phone' : [],
            'employee_address_1' : [],
            'employee_address_2' : [],
            'city' : [],
            'state' : [],
            'zip_code' : [],
            'supervisor_name' : [],
            'suffix' : [],
            'prefix' : [],
            'alternative_email_address' : [],
            'gender' : [],
            'employe_type' : [],
            'date_in_job' : [],
            'job_group' : [],
            'alternative_job_title' : [],
        }
        return table[self._lookup]

    
    def inactive_lookup(self):
        """
        Compares eCMS active/inactive codes with UKGs
        """
        if self._lookup == 'is_active' or self._lookup == 'employee_status':
            sublookup = {
                False: 'I',
                'T': 'I',
                'L': 'I',
                True: 'A',
                'A': 'A'

            }
            return [{'col' : 'STATUSCODE', 'result': sublookup[self.val]}]
        

    def parse_phone(self, number):
        pass

    def parse_name(self):
        """
        Parses the UKG Split name system back into the 
        singlur column system of eCMS while retaining 
        the suplimental split columns 
        """
        if self._lookup == 'first_name':
            employee = self.lookup_employee()

            new_first = self.val.upper()

            old_name = employee['EMPLNAME'].item().strip()
            new_name = old_name.replace(self.change['old'].upper(), new_first)

            old_abbrv = employee['ABBRV'].item().strip()
            new_abbrv = old_abbrv[:len(old_abbrv)-1] + new_name[0]

            results = [
                {'col': 'FIRSTNAME25', 'result': new_first},
                {'col': 'EMPLNAME', 'result': new_name},
                {'col': 'ABBRV', 'result': new_abbrv}
            ]
            return results
        if self._lookup == 'last_name':
            employee = self.lookup_employee()

            new_last = self.val.upper()
            if len(new_last) > 9:
                last_abbrv = new_last.split()[0][:8] + ' '
            else:
                last_abbrv = new_last

            old_name = employee['EMPLNAME'].item().strip()
            new_name = old_name.replace(self.change['old'].upper(), new_last)

            old_abbrv = employee['ABBRV'].item().strip()
            new_abbrv = last_abbrv + old_abbrv[-1]

            results = [
                {'col': 'LASTNAME25', 'result': new_last},
                {'col': 'EMPLNAME', 'result': new_name},
                {'col': 'ABBRV', 'result': new_abbrv}
            ]
            return results
        
    def parse_dept(self):
        """
        Converts the UKG department level back into ecms 
        department level
        """
        if self._lookup[:9] == 'org_level':
            employee = self.lookup_employee()
            level = int(self._lookup[-1])
            old_dept = str(int(employee['DEPTNO'].item()))
            dept = {}
            if level == 1:
                new_dept = str(self.divisions[self.val])
                dept = f'{new_dept}{old_dept[-1]}'
            if level == 2:
                old_dept = old_dept[:len(old_dept)-1]
                new_dept = str(self.departments[self.val])
                dept = f'{old_dept}{new_dept}'
            return [{'col': 'DEPTNO', 'result': dept}]

    def lookup_employee(self):
        """
        Looks up the record within ecms and returns a dataframe object
        """
        select = SQLQuery(HRTEMP).select()
        select.filters(employeeno=self.record['employee'].employee_number, companyno=1)
        return select.to_df()

    def company_lookup(self):
        company_lookup = {
            'Z9DZY': 1,
            'Z9EDD': 30,
            'Z9EG4': 40,
        }
        record = self.record['employee'].company_id
        return company_lookup[record]


        
        