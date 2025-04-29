![Web App CI/CD](https://github.com/software-students-spring2025/5-final-dockstars2-0/actions/workflows/web-app.yml/badge.svg?branch=main)  ![Mongo CI/CD](https://github.com/software-students-spring2025/5-final-dockstars2-0/actions/workflows/mongo.yml/badge.svg?branch=main)

# Yonder

## Overview
Yonder is an event discovery platform where users can browse, save, and organize events into boards.

## Features
- Explore page with event grid and integrated search
- User authentication (sign up, login)
- Save events to custom boards 
- Create new events
- Comment on events
- Profile page showing upcoming saved events and personal boards
- View events saved into each board

## Access the Deployed App
You can access the live Yonder web app [here](http://159.89.38.231/).

## Container Images
You can pull and run the images from Docker Hub:  

Web App: [ariangn/yonder:web-app](https://hub.docker.com/r/ariangn/yonder/tags?page=1&name=web-app) 
MongoDB Image: [ariangn/yonder:mongo](https://hub.docker.com/r/ariangn/yonder/tags?page=1&name=mongo) </code></pre>
## How to Run 

### With Docker
#### Prerequisites

Install the following software on your machine:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.8+](https://www.python.org/downloads/)

##### Installing Docker

1. Go to the [Docker website](https://www.docker.com/products/docker-desktop) and download Docker Desktop for your operating system.
2. Follow the installation instructions and make sure Docker Desktop is running.  

#### Steps:
1. **Clone the repository:**

```bash
git clone https://github.com/software-students-spring2025/5-final-dockstars2-0.git
cd 5-final-dockstars2-0
```

2. **Build and start the app using Docker Compose:**

```bash
docker-compose up --build
```

This will:

- Start the Flask app 
- Start a MongoDB container

3. **Access the app:**

Open your browser and go to [http://localhost:5000](http://localhost:5000) to access.

---

### Locally (Without Docker)

If you want to run it manually:

1. Install Python dependencies:

```bash
cd web-app
pipenv install
```

2. Start MongoDB separately (e.g., local MongoDB service, or Atlas connection).

3. Create a .env file following the `env.example`:

```bash
MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
MONGO_DBNAME="example_db"
FLASK_PORT=5000
```

4. Run the Flask app:

```bash
python app.py
```



## Team
* [Ajok Thon](https://github.com/ajokt123)
* [Aria Nguyen](https://github.com/ariangn)
* [Kahmeeah Obey](https://github.com/kahmeeah)
* [Nyjur Majok](https://github.com/nyjur1)
