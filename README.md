# FLIN Assignment

## Structure Of Project

- part1
  - this is answer for Part 1
    - `chatbot` (express)
  - Key Decision
    - gathering some QnA about flin from https://flin.co.id
    - use this data to become predefined knowledge for the Chatbot at (knowledge/knowledge.json)
    - those predefined data will be used as Context to feed into LLM (using Gemini API). Simple prompt used can be seen in `gemini.js`
- part2
  - this is answer for Part 2
    - `bad-performance`
      - sample of web need to be improved
    - `improve-performance`
      - proposed solution for `bad-performance` folder
  - Key Decision
    - Since it's not defined what website need to improve and i'm struggling to looking one, i decide to make one on my own
    - this bad website are at `bad-performance` project
    - then i try to propose best practice that we can apply on the bad-performance website at `improve-performance` project
    - for detail approach, please check [Part 2 README.md](./part2/README.md)
- part3
  - this is answer for Part 3
    - flin-api
      - all required API needed to answer this part
    - flin-web
      - Frontend code for implementing simple form for this part
- part4
  - this is answer for part 4
    - Proposed Infrastucture are Explained at [PDF](./part4/Flin%20Wordpress%20Infrastructure.pdf)
    - I decide to use terraform to configure the AWS infrastructure for easier maintenace and also consistent configuration
    - i tried to combine EC2 + Docker + Wordpress for easier deployment process
- part5
  - this is answer for part 5
    - flin-api
  - Key Decision
    - Implement 3 required API, such as login, register and profile
    - for profile, requires to use JWT on the header request

## HOW TO TEST APIs

- Please check video in here for how to use Postman
- For the endpoint, can check each part README file or check from the Swagger (please read README)
