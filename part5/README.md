# PART 3

## TECH STACK

1. Python & Django
2. Postgresql
3. Docker & Docker Compose

## API Documentation

### Login

- Method: POST

- Endpoint: /identities/login/

- Headers: -

- Query Params: -

- Body:

```
{
    email: str (required),
    password: str (required)
}
```

- Response:

```
{
    user:   {
        id: UUID (required)
        full_name: str (optional),
        email: str (required),
        phone_number: str (optional),
        photo_profile: str (optional),
        username: str (optional),
        provider: 'basic' | 'google',
        is_email_verified: boolean,
    },
    token: {
        refresh: str (required),
        access: str (required)
    }
}
```

### Register

- Method: POST

- Endpoint: /identities/register/

- Headers: -

- Query Params: -

- Body:

```
{
    email: str (required),
    password: str (required)
}
```

- Response:

```
{
    user:   {
        id: UUID (required)
        full_name: str (optional),
        email: str (required),
        phone_number: str (optional),
        photo_profile: str (optional),
        username: str (optional),
        provider: 'basic' | 'google',
        is_email_verified: boolean,
    },
    token: {
        refresh: str (required),
        access: str (required)
    }
}
```

### Profile

- Method: GET

- Endpoint: /identities/profile/

- Headers:

```
{
    Authorization: Bearer <jwt>
}
```

- Query Params: -

- Body: -

- Response:

```
{
    email: str (required),
    full_name: str (optional),
    phone_number: str (optional)
}
```

### SWAGGER ACCESS

To make it easier for API testing and see the documentation, please access it at

- Live Version

```
http://16.78.198.190:8006/swagger
```

please use this credentials

```
username: test@test.com
password: test12345
```

## HOW TO RUN

### BEFORE RUN THE PROJECT

please make sure to create `.env` file like shown in `.env.example`

### With Docker

1. make sure to install docker first, you can check how to install if not yet installed at your machine in here https://docs.docker.com/get-started/get-docker/
2. also make sure you already insall docker-compose https://docs.docker.com/compose/install/linux/
3. after that, simply just run this on the root project dir (cd ../part3)

```
docker-compose up part3-nginx --build
```

### Without Docker

#### Run flin-api

- please check [README](./flin-api/README.md)

## Deployed Version

Please try the deployed version in here
Backend:
http://16.78.198.190:8006/
