These instructions are for setting up a personal copy of a project in your home directory on the dev server.

The first thing you need to do is copy the code.

```shell
# Clone the repository from GitHub.
$ cd ~
$ git clone https://github.com/HCDigitalScholarship/<your-project-name>.git

# If your repository has a settings_secret file:
$ cp /srv/<your-project-name>/<project-dir>/settings_secret.py ~/<your-project-name>/<project-dir>
```

Next, configure git with your email and name.

```shell
$ git config user.email "jdoe@haverford.edu"
$ git config user.name "Jane Doe"
```

Replace the placeholders with your personal information. Make sure you use the email that is associated with your GitHub account.

You should now be able to run the server with:

```shell
$ ./manage.py runserver <dev-server-ip>:8000
```

For example, the IP address for the GAM dev server is 192.241.128.56, so you would run the server with `./manage.py runserver 192.241.128.56:8000`.

The website will be available at the same URL, but with the port suffixed to the domain name, i.e. `192.241.128.56:8000/about` instead of `192.241.128.56/about`.

If multiple people are working on the same site at the same time, you'll each have to choose a different port number, i.e. `8001` instead of `8000`.

Finally, the last step is to create a copy of the database. The exact commands depend on whether you're using MySQL or Postgres. For the database name, suffix the main database with your username. For example, if your username is `jdoe` and the main database is called `tichadb` (you can check in `settings_secret.py`), then your database should be named `tichadb_jdoe`. The database username should be the same as the main database (again, you can check in `settings_secret.py`).

MySQL:
```shell
$ mysql -u root -p
> CREATE DATABASE <database-name>;
> GRANT ALL PRIVILEGES ON * . * '<username>'@'localhost';
> FLUSH PRIVILEGES;
> \q
```

Postgres:
```shell
$ sudo -u postgres psql postgres
> CREATE DATABASE <database-name>;
> GRANT ALL PRIVILEGES ON DATABASE <database-name> TO <database-username>;
> \q
```

You'll then need to export your data from the old database and import it into the new database.

MySQL:
```shell
$ mysqldump -u root -p <main-database-name>  > dump.sql
# IMPORTANT: Edit dump.sql so that the first line is "USE <your-database-name>;" (with the semicolon but without the quotes).
$ mysql -u root -p < dump.sql
```

Postgres:
```shell
$ sudo -u postgres pg_dump <main-database-name>  > dump.sql
$ sudo -u postgres psql <your-database-name>  < dump.sql
```

Finally, run the Django migrations:
```shell
$ ./manage.py migrate
```
