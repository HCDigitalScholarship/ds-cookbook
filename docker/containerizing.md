# Containerizing Projects With Docker

Docker achieves three main things for DS projects:

1. Prepares the project for deployment to a live website.
2. Makes the project ready for others to collaborate on.
3. Preserves the project long-term by freezing it in time, so it can run many years later.

To get started with Docker, you need to add a few files to your project.

## 1. Adding files for Docker

Create the following text files in the root folder of your project:

- `Dockerfile`
- `compose-dev.yaml`

### 1.1 `Dockerfile`

This file tells Docker how to build the container for your app.

Edit this file, and the delete all the `FIXME` comments when you are done.

```dockerfile
# The Docker image our image will be based on.
# Django projects should base off the python image.
FROM python:3.11
# FIXME^: This version is outdated! Get the latest stable version from here: https://hub.docker.com/_/python

# Project folder path in the image.
WORKDIR /app

# Install requirements first. This makes rebuilding the image faster.
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the project files in. Compile CSS, etc.
COPY . /app
RUN SECRET_KEY=1 python mysite/manage.py collectstatic --noinput --clear
# FIXME^: Change `mysite` to your project name.

# Run the project on port 5000.
EXPOSE 5000
CMD python mysite/manage.py migrate; python mysite/manage.py runserver 0.0.0.0:5000
# FIXME^: Change `mysite`(2) to your project name.
```

### 1.2 `compose-dev.yaml`

This file is used by Docker Desktop to spin up your container.

```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
    ports:
      - "5000:5000"
```

After this, **commit your changes!**

### 1.3 Running with Docker

The easiest way to use Docker is with [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Once installed, add your project folder to it and start it up. If it worked, your project will now be running at http://localhost:5000! If it didn't, don't be discouraged. Scroll down to the "Troubleshooting" section below.

If you are using a database, you will need changes to both the `Dockerfile` and `compose-dev.yaml`. Please review other DS projects on GitHub for inspiration.

Once this is working, you are done with the first section. Submit a pull request for your Docker changes and take a break. ☕

## 2. Deploying the project

Now that Docker is working, it's time to deploy. You will need a server provisioned by the IT department. You should provide your SSH public key, and receive a git remote URL, looking something like this:

```
dokku@pennstreaty-2023.haverford.edu:pennstreaty
```

Add it to your project:

```
git remote add dokku dokku@pennstreaty-2023.haverford.edu:pennstreaty
```

Finally, deploy the project:

```
git push dokku main
```

If all is well, your project will be built with Docker and running on a public URL! If so, you can skip the rest of this section. Otherwise, read on.

### 2.1 Configuring your app

To set environment variables on your project, use the SSH command:

```
ssh dokku@pmyapp.haverford.edu:myapp config:set ENV_1="testing123"
```

Most projects will need at least some configuration, such as a `SECRET_KEY` for the app to start. This is a common reason why a deployment may fail.

### 2.2 Using a database

An IT administrator can add a database to your project, such as Postgres, Redis, and more. When they do, the credentials will be available in a single `DATABASE_URL` environment variable. For Django projects, it is recommended to use the [dj-database-url](https://pypi.org/project/dj-database-url/) package.

For now projects, it is **highly recommended** to use SQLite as the database due to its simplicity.

## 3. Troubleshooting

Please try the following methods:

- Search the web. Docker is widely discussed technology.
- Ask an AI chatbot. AI is capable of writing Dockerfiles and helping to debug errors.
- Look at other DS projects on GitHub. Many are set up and working with Docker.
- Ask another student, especially those working on DS projects.
- If you are trying to deploy and have exhausted all other options, feel free to reach out to the IT department. Server misconfigurations can happen.

## 4. Advanced tips

DS servers use [Dokku](https://dokku.com/) for deployment. Anything Dokku supports can be done.
