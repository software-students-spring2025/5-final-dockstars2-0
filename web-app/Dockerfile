services:
    web-app:
      build: ./web-app
      ports:
        - "8080:8080"
      container_name: web-app
      depends_on:
        - mongo
  
    mongo:
      image: mongo
      ports:
        - "27017:27017"
      volumes:
        - mongo-data:/data/db
  
  volumes:
    mongo-data:
  