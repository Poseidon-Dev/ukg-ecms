
class Employee:

    def __init__(self, record):
        self.first_name = record['firstName']
        self.last_name = record['lastName']
        self.preferred_name = record['preferredName']
        self.email_address = record['emailAddress']
        self.country_code = record['countryCode']
        self.language_code = record['languageCode']
        self.employee_number = record['employeeNumber']
        self.employee_id = record['employeeId']
        self.person_id = record['personId']
        self.user_integrated_key = record['userIntegrationKey']
        self.company_name = record['companyName']
        self.company_id = record['companyId']
        self.supervisor_id = record['supervisorId']
        self.salary_or_hourly = record['salaryOrHourly']
        self.fulltime_or_parttime = record['fullTimeOrPartTime']
        self.is_active = record['isActive']
        self.work_location_code = record['workLocationCode']
        self.job_code = record['jobCode']
        self.project_code = record['projectCode']
        self.org_level_1 = record['orgLevel1Code']
        self.org_level_2 = record['orgLevel2Code']
        self.org_level_3 = record['orgLevel3Code']
        self.org_level_4 = record['orgLevel4Code']
        self.middle_name = record['middleName']
        self.work_phone = record['workPhone']
        self.home_phone = record['homePhone']
        self.employee_address_1 = record['employeeAddress1']
        self.employee_address_2 = record['employeeAddress2']
        self.city = record['city']
        self.state = record['state']
        self.zip_code = record['zipCode']
        self.termination_date = record['terminationDate']
        self.hire_date = record['hireDate']
        self.supervisor_name = record['supervisorName']
        self.suffix = record['suffix']
        self.prefix = record['prefix']
        self.alternative_email_address = record['alternateEmailAddress']
        self.gender = record['gender']
        self.employee_status = record['employeeStatus']
        self.employe_type = record['employeeType']
        self.employee_status_start_date = record['emplStatusStartDate']
        self.date_in_job = record['dateInJob']
        self.date_of_last_hire = record['dateOfLastHire']
        self.job_group = record['jobGroupCode']
        self.alternative_job_title = record['alternateJobTitle']

    
    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return self.employee_number == other.employee_number

   
    def __str__(self):
        return f'{self.employee_number}: {self.first_name} {self.last_name}'

    
    def __repr__(self):
        return f'{self.employee_number}'

