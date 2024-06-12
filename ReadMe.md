This is a simple FastAPI application.

You can test the app by:

    Creating a .env file in the same directory as docker-compose-prod.yml.
    Running the command: docker-compose -f .\docker-compose-prod.yml up --build.
    Opening your browser and navigating to: localhost:80.
    To see Swagger documentation, open: localhost:80/docs.

Exemple of .env file:

- DATABASE_HOSTNAME=postgres
- DATABASE_PORT=5432
- DATABASE_PASSWORD=""
- DATABASE_NAME=""
- DATABASE_USERNAME=""
- SECRET_KEY=hellofastapi
- ALGORITHM=HS256
- ACCESS_TOKEN_EXPIRE_MINUTES=15

test à faire
