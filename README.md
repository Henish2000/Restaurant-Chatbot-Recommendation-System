
# Dining-Concierge-Chat-App

This is a serverless, micro service-driven web application created completely using AWS cloud services. The main application of this chatbot is to provide restaurant suggestions to its users based on the preferences provided to it through conversations.

We have support for Yelp-API with suggestions and real time chat.




## Technologies Used

- Amazon S3 - To host the frontend
- Amazon Lex - To create the bot
- API Gateway - To set up the API
- Amazon SQS - to store user requests on a first-come bases
- ElasticSearch Service - To quickly get restaurant ids based on the user preferences of cuisine collected from SQS
- DynamoDB - To store the restaurant data collected using Yelp API
- Amazon SNS - to send restaurant suggestions to users through SMS
- Lambda - To send data from the frontend to API and API to Lex, validation, collecting restaurant data, sending suggestions using SNS.
- Yelp API - To get suggestions for food
- AWS Congito - For authentication


## Architecture

![Architecture](https://github.com/Henish2000/Restaurant-Chatbot-Recommendation-System/blob/main/Screenshots/architecture_diagram.png)

