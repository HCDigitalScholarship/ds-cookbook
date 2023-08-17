# Dokku Administrator's Guide

This document is aimed at the IT department. Students can feel free to read on about how DS apps are deployed.

## 1. Introduction

DS apps are deployed with [Dokku](https://dokku.com/). Dokku is a FOSS self-hosted deployment platform inspired by Heroku. Dokku acts as a git remote, and when code is pushed to it, it attempts to deploy the code using Docker.

Dokku has a command-line interface for managing many apps on a single machine. Dokku also has plugins for things like user-project access control (ACL) and more.

The apps run in Docker. Nginx is installed on the host. Dokku manages both Docker and Nginx.

## 2. Installing Dokku

Dokku should be installed on a dedicated machine or VM. Follow the steps on the Dokku homepage: https://dokku.com/

Finally, the following [plugins](https://dokku.com/docs/community/plugins/) may be added:

- `letsencrypt` - https://github.com/dokku/dokku-letsencrypt
- `require` - https://github.com/crisward/dokku-require
- `acl` - https://github.com/dokku-community/dokku-acl
- `postgres` - https://github.com/dokku/dokku-postgres

## 3. Setting up projects

To create an app, run `dokku apps:create <myapp>`

### 3.1 Setting the domain

```sh
dokku domains:set <myapp> myapp.haverford.edu
```

### 3.2 Setting the port

Projects will typically use port `5000` or `8000`. It may need to be manually configured before the app will work:

```sh
dokku proxy:ports-set <myapp> http:80:5000
```

### 3.3 Enabling SSL

The app needs to be already running (on port 80) before this will work:

```sh
dokku letsencrypt:enable <myapp>
```

The first time, it will throw an error. To fix:

```sh
dokku letsencrypt:set <myapp> email pguardiola@haverford.edu
```

### 3.4 Project configuration

Different projects have different needs, but it won't be surprising if something like this is needed:

```sh
dokku config:set <myapp> ALLOWED_HOSTS="myapp.haverford.edu"
dokku config:set <myapp> SECRET_KEY="12346789..."
```

TIP: generate a Django secret key with `openssl rand -base64 48`

### 3.5 Adding Postgres

If the project needs a database, ensure the postgres plugin is installed, then:

```sh
dokku postgres:create myapp
dokku postgres:link myapp myapp
```

Each postgres container has a name. Here we call it the same name as the app, and then link them.

This will add a `DATABASE_URL` variable to the app. It's up to students to make sure their app uses it.

### 3.6 Adding other databases

There are plugins for MySQL, MariaDB, Redis, and more. Check the README for the specific plugin that is needed. The command line interface is usually the same as the Postgres plugin, eg `create` and then `link`.

### 3.7 Mounting volumes

Sometimes files need to be mounted to the host, so they will survive across deployments. This is common for SQLite databases.

```sh
dokku storage:mount <myapp> /var/lib/dokku/data/storage/myapp:/app/data
```

The directory needs to exist on the host, and needs to give Dokku permission to read and write to it. The second path is the storage path inside the image, and may vary by project. Usually it will be at `/app/data`.

Note that Docker cannot mount individual files, only folders. So SQLite databases cannot be at the project root, and should instead be in a `data` subdirectory. The project will need to be modified if this is not the case.

## 4. Server maintenance

Sometimes servers need to be updated, or projects need to be moved.

If an app needs to be moved, it's recommended to create it from scratch on the new machine, configure it with the old config, and then copy any persistent data (such as a database) to the new server.

### 4.1 Dumping a Postgres database

From another computer (with SSH):

```sh
ssh dokku@example.haverford.edu postgres:export myapp > myapp.dump
```

### 4.2 Restoring a database

From another computer (with SSH):

```sh
cat myapp.dump | ssh dokku@example.haverford.edu postgres:import myapp
```

### 4.3 Upgrading Dokku

Dokku is a stable system and does not need to be updated unless there is a specific need. It is more likely that the operating system itself will become too outdated and the whole VM will need to be replaced.

That being said, Dokku installs an Ubuntu PPA for itself on the first run, so `sudo apt update && sudo apt upgrade` will sufficiently keep Dokku up-to-date. Updates to Dokku are intended to be backwards-compatible.
