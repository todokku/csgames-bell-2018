# CSGames Bell 2018 Web Competition

This competition was part of the 2018 edition of the [CS Games](http://csgames.org), a collegiate competition that includes challenges from all aspects of computing.

## Competition Description
You are an extraterrestrial life form on Earth without any tools to properly integrate yourself. What's better than news shows and TV shows to open a conversation with humans?

The goal:
Your task is to create a streaming platform (HTTP REST backend and web frontend) to provide easy access to human content for extraterrestrial life form. You have been given a set of stories with business points for each story. The more business points you complete, the better extraterrestrials will be able to integrate on Earth.

## Home Page

![Screenshot](screenshot.png)

## Filters

<img src="filters.png" height="400" width="400">

## Features
* Video Gallery
* Video Filters
* Video Search
* User Profiles

## Setup
In order for the frontend app to connect to the APIs, add a `client.env` file in the root folder of the project with the following variables:
```
NODE_ENV=development
REACT_APP_BELL_SERVICE_URL=http://localhost:8932
REACT_APP_YOUTUBE_DATA_API_URL=https://www.googleapis.com/youtube/v3
REACT_APP_YOUTUBE_DATA_API_KEY=[YOUR_YOUTUBE_DATA_API_KEY]
```

## Start the server and the client
`./start.sh`

The client should be acessible at [http://localhost:3007/](http://localhost:3007/).

I used JWT for authentication because the default Flask session is not persisted in the browser.

## Common Commands

Build the images:

`docker-compose -f docker-compose-dev.yml build`

Run the containers:

`docker-compose -f docker-compose-dev.yml up`

Create the database:

`docker-compose -f docker-compose-dev.yml exec server python manage.py recreate_db`

Seed the database:

`docker-compose -f docker-compose-dev.yml exec server python manage.py seed_db`

## Other Commands

To stop the containers:

`docker-compose -f docker-compose-dev.yml stop`

Remove images:

`docker rmi $(docker images -q)`

## Postgres
Want to access the database via psql?

`docker-compose -f docker-compose-dev.yml exec database psql -U postgres`

## Client
Connect to the client

`docker-compose -f docker-compose-dev.yml exec client /bin/sh`

### Frontend Setup

If you copied the repository, this step can be skipped as it is already done.
To create the frontend app from scratch locally:

Install [nvm](https://github.com/nvm-sh/nvm), then run the following commands.

```shell
# Install Node.js
nvm install node
# Install Create React App
npm install create-react-app --global
# Create the boilerplate
cd client
create-react-app .
```

## Completed User Stories
* [BP:3] As an operator, I can run a bash script that starts both the client and the server
* [BP:8] As an extraterrestrial user, I can navigate through available assets
* [BP:2] As an extraterrestrial user, I am able to search content
* [BP:3] As a user, I can authenticate (log in)
* [BP:5] As an operator, I can create accounts for users (register)
* As a user, I can log out
* [BP:1] As an extraterrestrial user, I can watch a video
* [BP:3] As an extraterrestrial user, I can play an asset that is available
* [BP:?] As an extraterrestrial user, I should not be able to stream a video that does not fit my profile
* As an extraterrestrial user, I can add a filter to the stream (blur, inverse, convolve, convoblur, black and white, noir, displacement)
* As an operator, I can create or update an asset (requires YouTube API key)

## TODO
* [BP:21] As a 3D Enthusiast, I can add a filter to make my stream appear in 3D
* [BP:13] As an extraterrestrial user, I can add an ASCII Art filter to the stream and toggle it
* [BP:?] As an extraterrestrial user, I can add a Vaporwave filter to the stream and toggle it
* [BP:5] As a extraterrestrial user, my background color changes depending on the dominant color shade in the video
* [BP:3] As a content provider, I want the rights to be refreshed every X seconds (where X is defined by the content provider)
* [BP:1] As an operator, I can change content provider refresh rate
* [BP:?] The client must refresh its session in case of profiles changes
* [BP:1] As a streaming platform, I am legally obligated to provide alerts in case of emergencies

## Completed Required API Routes
* **PUT** `/bell/authentication`
* **GET** `/bell/assets?profiles=X&profiles=Y`
* **GET** `/bell/alerts`
* **PUT** `/bell/hidden/provider/{:id}/refreshRate`
* **POST** `/bell/hidden/account`
* **GET** `/bell/search?query=<query>`

**POST** `/bell/authentication`

Logs in the user.

Request
```json
{
  "username": "YoungProudBandicoot",
  "password": "Password_4"
}
```

Response
```json
{
  "accountId": "cf44bf5c-0cca-45f1-a47a-a13b6c859054",
  "hashedCredentials": "YoungProudBandicoot:973faaff5f9859cd1c8145cf1f4b1aa0833be900da1916ecf168853e95362054",
  "profiles": [
    "Vaporwave Lover"
  ],
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTQyNDQyMjAsImlhdCI6MTU1MTY1MjIyMCwic3ViIjoiY2Y0NGJmNWMtMGNjYS00NWYxLWE0N2EtYTEzYjZjODU5MDU0In0.cAkWQE9bVYeRXcgNH9MFIas0VYqaLPVTcec5IYpBtsk"
}
```

## Completed Additional API Routes

**GET** `/bell/asset/<:id>`

Returns the asset which corresponds to the media id parameter, only if the current date is within the licensing window.

Response
```json
{
  "licensingWindow": {
    "start": "2018-01-01T06:00:00",
    "end": "2019-12-31T10:00:00",
  },
  "media": {
    "durationInSeconds": 97,
    "mediaId": "UYrkQL1bX4A"
  },
  "profileIds": ["4", "6", "7"],
  "providerId": "CTV",
  "provider": 2345,
  "refreshRateInSeconds": 3,
  "title": "LazyTown song - Cooking By The Book"
}
```
200 | when the asset is valid

400 | when the media id, licensing window or profiles are invalid

---

**POST** `/bell/logout/`

Logs out the currently logged in user.

Response
```json
{
  "message": "Logout successful"
}
```
200 | Logout successful

---

**POST** `/bell/hidden/asset/{:id}`

Create an asset.

**PUT** `/bell/hidden/asset/{:id}`

Update an asset.

## Profiles
| profile_id | name |
|:----------:|:----:|
| 1 | Pirate |
| 2 | Mac User |
| 3 | Vaporwave Lover |
| 4 | Deaf |
| 5 | Hipster |
| 6 | Robot |
| 7 | Uniped |
| 8 | 3D Enthusiast |
| 9 | Simpsons Enthusiast |

## References
* [CSGames Bell 2018 - User stories (final - EN version)](https://trello.com/b/pT20udUF/csgames-bell-2018-user-stories-final-en-version)
* [Microservices with Docker, Flask, and React](https://github.com/testdrivenio/testdriven-app-2.4)
* [React + Redux - User Registration and Login Tutorial & Example](http://jasonwatmore.com/post/2017/09/16/react-redux-user-registration-and-login-tutorial-example)
* [JSON Web Tokens](https://jwt.io/)
* [https://www.paulirish.com/work/videooo.xhtml](https://www.paulirish.com/work/videooo.xhtml)
