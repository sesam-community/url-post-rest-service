# URL Post rest service

A simple service that translates get requests to post requests.


Example system config:
----------------------

```json
{
  "_id": "url-post-rest-system",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "apiKey": "my-api-key",
      "baseurl": "https://my.base.url.no/",
      "page_number": "1",
      "page_size": "1000",
      "protocol": "json"
    },
    "image": "sesamcommunity/url-post-rest-service:latest",
    "port": 5001
  }
}

```

Example pipe using the microservice above
----------------------------------------------

```json
{
  "_id": "url-post-rest-pipe",
  "type": "pipe",
  "source": {
    "is_chronological": false,
    "is_since_comparable": true,
    "supports_since": false,
    "system": "url-post-rest-system",
    "type": "json",
    "url": "my-url-post-rest-api/api"
  }
}

```