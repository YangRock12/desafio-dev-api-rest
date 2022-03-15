# About Project
- Python (framework: fastApi)
- MySql (python package: mysql-connector-python)
- Built in a DDD approach
- To validate if transactions were possible it was implemented the ChainOfResponsibilities Pattern
- To make the code easier to implement and maintain new kind of transactions it was implemented the StrategyPattern
- To minimize concurrency access to the rows being manipulated by a transaction it was used a 'Select For Update'
---
# How to start the project
Using docker you can run the following command on project root folder:
> docker compose up -d

Docker compose will start 2 pods:
- One Pod containing the DigitalAccountApi
- One Pod containing the MySql DB
---
# Running tests
Run the following commands
> pip install coverage
>
> coverage run -m unittest
> 
> coverage html - this command creates a folder, open the index.html on your browser to see the result
---
# Documentation
On 'docs' folder exist two folder:
- One called "database", containing a .sql file with a script creating the database,
  tables and inserting some dummy records. This file run the first time the database is created with the docker compose 
  command mentioned before.
- One called 'digital_account_api_flux', with a draw.io containing all fluxes that are above.
> On the endpoint '/docs' of the API has more descriptive information about the endpoints.