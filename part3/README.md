# PART 3

## TECH STACK

1. Python & Django
2. Postgresql
3. Vite + React
4. Docker & Docker Compose

## API Documentation

### Add New Leads

- Method: POST

- Endpoint: /leads/

- Headers: -

- Query Params: -

- Body:

```
{
    name: str (required),
    email: str (required),
    phone_number: str (required),
    loan_type: "kpr" | "kpa" | "personal" (required)
}
```

- Response:

```
  {
    id: UUID (required)
    name: str (required),
    email: str (required),
    phone_number: str (required),
    loan_type: "kpr" | "kpa" | "personal" (required)
  }
```

### List All Leads

- Method: GET

- Endpoint: /leads/

- Headers:

```
{
    Authorization: Bearer <jwt>
}
```

- Query Params:

```
{
    page: int (optional),
    limit: int (optional) (default=10)
}
```

- Body: -

- Response:

```
{
    count_items: int,
    previous_page: int,
    next_page: int,
    data: List[{
        id: UUID (required)
        name: str (required),
        email: str (required),
        phone_number: str (required),
        loan_type: "kpr" | "kpa" | "personal" (required)
    }]
}
```

### SWAGGER ACCESS

To make it easier for API testing and see the documentation, please access it at

- Live Version

```
http://16.78.198.190:8003/swagger
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

### Run flin-web

assume you are using pnpm (you also can use npm/yarn)

```
cd flin-web
```

```
pnpm install
```

```
pnpm run dev
```

## Deployed Version

Please try the deployed version in here
Frontend:
http://16.78.198.190:8004/
Backend:
http://16.78.198.190:8003/
