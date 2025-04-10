# PART 1

## TECH STACK

1. NodeJS
2. Express
3. Gemini API
4. Docker & Docker Compose

## HOW TO RUN

### BEFORE RUN THE PROJECT

please make sure to obtain your GEMINI API KEY first at https://aistudio.google.com/

then create `.env` file like this

```
GEMINI_API_KEY=<your key>
```

and put it inside /chatbot directory

### With Docker

1. make sure to install docker first, you can check how to install if not yet installed at your machine in here https://docs.docker.com/get-started/get-docker/
2. also make sure you already insall docker-compose https://docs.docker.com/compose/install/linux/
3. after that, simply just run this on the root project dir (cd ../part1)

```
docker-compose up part1-chatbot --build
```

### Without Docker

assume you are using pnpm (you also can use npm/yarn)

```
pnpm install
```

```
pnpm run dev
```

then you can access it on your browser via http://localhost:3000

## Deployed Version

Please try the deployed version in here
http://16.78.198.190:8001/
