# How to setup postrges in Linux Ubuntu 
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-22-04

run: sudo apt install postgresql postgresql-contrib

# How to change password
    In Linux
        sudo -i -u postgres
        plsq
        ALTER USER postgres PASSWORD 'mynewpassword';


# Other tools / interfaces
install phppgAdmin
https://www.rosehosting.com/blog/how-to-install-phppgadmin-on-ubuntu-22-04/

phppgadmin then go via browser to http://localhost/phppgadmin/ 

# Install sample database 
A dataset containing details about employees, their departments, salaries, and more.

# Create the database and schema:

create schema 'emailcandidate' manually

  $ sudo -i -u postgres
  $ psql
    CREATE DATABASE emailcandidate;
    \c emailcandidate
    CREATE SCHEMA emailcandidate;

# TODO explain how to create the database and tables with the utils/db_utils.py



Here are more details about how to install postgres on Windows
https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/
