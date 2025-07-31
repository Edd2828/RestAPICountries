# RestAPICountries
Simple API to get country information from restcountries: https://restcountries.com/

Requirements:
- local postgres
- python
- Power BI

Python dependancies:
- psycopg2
- pandas
- pydantic

Instructions:
1. Create Countries Database in local postgres
2. Create login group/role in postgres
3. Grant admin privileges to user
4. In utils file `connection_details.py` to utils folder add function with group/role username and password
```
# Copy to connection_details.py
def get_connection_details():
    return {
        'host': 'localhost',
        'database': 'Countries',
        'user': '<created_group_role>',
        'password': '<group_role_password>'
    }
```
5. Run `py main.py`


   
