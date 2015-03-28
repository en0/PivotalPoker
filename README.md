#### To Run Server
```bash
cd src/
gunicorn -k gevent -b IP:PORT run:app
```

## REST Api

* Session
  * PUT /api/v0.1/session: Start user session.
  * GET /api/v0.1/session: Retrieve user session.
* Job
  * GET /api/v0.1/jobs/: List currently queued items.
  * GET /api/v0.1/jobs/{jobid}: Retrieve queued item _jobid_.
* Game
  * POST /api/v0.1/game/: Create a new game.
  * GET /api/v0.1/game/: List open games.
  * GET /api/v0.1/game/{gameid}: List the game _gameid_
  * DELETE /api/v0.1/game/{gameid}: Destroy the game _gameid_
* Hand
  * PUT /api/v0.1/hand/{gameid}: Deal the hand for game _gameid_.
  * DELETE /api/v0.1/hand/{gameid}: Destroy hand for game _gameid_.
* Player
  * POST /api/v0.1/player/{gameid}/: Join the game _gameid_.
  * GET /api/v0.1/player/{gameid}/: List players in a game _gameid_.
  * GET /api/v0.1/player/{gameid}/{playerid}: Retrieve player _playerid_ from game _gameid_.
  * DELETE /api/v0.1/player/{gameid}/{playerid}: Remove a player _playerid_ from game _gameid_
* Vote
  * PUT /api/v0.1/vote/{gameid}: Submit the vote for the current hand on game _gameid_.
* Result
  * PUT /api/v0.1/result/{gameid}: Accept or reject the result of the vote on the current hand for game _gameid_.

## Session
### POST /api/v0.1/session
Start user session.

The full JSON format of a user resource.

```json
{
    "name": "Player Name"
}
```

name

The name that will be showed to other players in the game.

#### Example
##### Request:
```http
PUT /api/v0.1/session HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Content-Type: application/json
Content-Length: 23

{"name": "Player Name"}

```

##### Response:
```http
HTTP/1.1 201 CREATED
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 16:32:03 GMT
Connection: keep-alive
Location: http://localhost:5000/api/v0.1/session
Content-Type: text/html; charset=utf-8
Content-Length: 0
Added cookie session="9626aa1a-3902-44ed-915c-b3e48f8d7a21" for domain localhost, path /, expire 0
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

```

### GET /api/v0.1/session

Retrieve user session.

#### Example
##### Request:
```http
GET /api/v0.1/session HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json

```

##### Response:
```http
HTTP/1.1 200 OK
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 16:37:22 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 27
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

{
  "name": "Player Name"
}

```

## Job
### GET /api/v0.1/jobs/
List currently queued items.

The full JSON format of a job resource.

```json
{
  "job_id": "07149d5d-0397-4057-bb7f-784d7023199d", 
  "status": 202
}
```

job_id

The unique id of referring to a queued item.

status

The last known status of the queued item.

#### Example
##### Request:
```http
GET /api/v0.1/jobs/ HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json

```

##### Response:
```http
HTTP/1.1 200 OK
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 18:35:10 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 108
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

{
  "jobs": [
    {
      "job_id": "07149d5d-0397-4057-bb7f-784d7023199d", 
      "status": 202
    }
  ]
}

```

### GET /api/v0.1/jobs/{jobid}
Retrieve queued item _jobid_.

#### Example
##### Request:
```http
GET /api/v0.1/jobs/07149d5d-0397-4057-bb7f-784d7023199d HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json

```

##### Response:
```http
HTTP/1.1 200 OK
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 18:37:12 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 72
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

{
  "job_id": "07149d5d-0397-4057-bb7f-784d7023199d", 
  "status": 202
}

```

## Game
### POST /api/v0.1/game/
Create a new game

The full JSON format of a game resource.

```json
{
  "current_hand": null, 
  "desc": "This is a test game", 
  "game_id": "7920c443-256c-4c67-a96f-df39d2c1b330", 
  "hands": [], 
  "owner_id": "34c4a38d-51dc-4fd8-a5c7-d2ccb9ff004e", 
  "owner_name": "Player Name", 
  "password": null, 
  "players": {}, 
  "pts_scale": [ 1,  2,  3,  5,  8 ], 
  "state": "Open", 
  "title": "Game", 
  "total_pts": 0
}
```

current_hand

Initially NULL, this field will hold a hand entity. The current hand is the hand that all votes will be applied.

desc

The details provided by the owner.

game_id

The system assigned game id used to interact with the game.

hands

Initially empty, the hands that have already been completed for this game.

owner_id

The player id of the person that created the game.

owner_name

The player name of the person that created the game.

password

The optional password to secure access to this game.

players

Initially empty, the currently enrolled players in the game.

pts_scale

The point scale used for casting votes on any hands for this game.

state

Initially _Open_, the current state of the game.
 - Open: No hands are currently in play and new users can join at any time.
 - Playing: The game is currently in voting on a hand. No players can join at this time.
 - Reviewing: The game has finished a hand and is waiting on the owner to accept or reject the of the vote. No players can join at this time.
 
title

The publicly visible title of the game.

total_pts

The accumulated points for this game. This value is dirived by adding accepted votes from each hand together.


#### Example
##### Request:
```http
POST /api/v0.1/game/ HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json
Content-Length: 88

{
    "title": "Game",
    "desc": "This is a test game",
    "pts_scale": [1, 2, 3, 5, 8]
}

```

##### Response:
```http
HTTP/1.1 200 OK
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 17:38:05 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 376
Location: http://localhost:5000/api/v0.1/game/7920c443-256c-4c67-a96f-df39d2c1b330
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

{
  "current_hand": null, 
  "desc": "This is a test game", 
  "game_id": "7920c443-256c-4c67-a96f-df39d2c1b330", 
  "hands": [], 
  "owner_id": "34c4a38d-51dc-4fd8-a5c7-d2ccb9ff004e", 
  "owner_name": "Player Name", 
  "password": null, 
  "players": {}, 
  "pts_scale": [
    1, 
    2, 
    3, 
    5, 
    8
  ], 
  "state": "Open", 
  "title": "Game", 
  "total_pts": 0
}
```

### GET /api/v0.1/game/
List open games.

#### Example
##### Request:
```http
GET /api/v0.1/game/ HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json

```

##### Response:
```http
HTTP/1.1 200 OK
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 17:56:39 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 178
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

{
  "games": [
    {
      "game_id": "7920c443-256c-4c67-a96f-df39d2c1b330", 
      "has_password": false, 
      "owner_name": "Player Name", 
      "title": "Game"
    }
  ]
}

```

### GET /api/v0.1/game/{gameid}
List the game _gameid_

#### Example
##### Request:
```http
GET /api/v0.1/game/7920c443-256c-4c67-a96f-df39d2c1b330 HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json

```

##### Response:
```http
HTTP/1.1 200 OK
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 18:03:39 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 300
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

{
  "current_hand": null, 
  "desc": "This is a test game", 
  "game_id": "7920c443-256c-4c67-a96f-df39d2c1b330", 
  "hands": [], 
  "owner_name": "Player Name", 
  "players": {}, 
  "pts_scale": [
    1, 
    2, 
    3, 
    5, 
    8
  ], 
  "state": "Open", 
  "title": "Game", 
  "total_pts": 0
}
```

### DELETE /api/v0.1/game/{gameid}
Destroy the game _gameid_

#### Example
##### Request:
```http
DELETE /api/v0.1/game/7920c443-256c-4c67-a96f-df39d2c1b330 HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21
Content-Type: application/json

```

##### Response:
```http
HTTP/1.1 204 NO CONTENT
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 18:20:33 GMT
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Content-Length: 0
Set-Cookie: session=9626aa1a-3902-44ed-915c-b3e48f8d7a21; HttpOnly; Path=/

```

## Hand
### PUT /api/v0.1/hand/{gameid}
Deal the hand for game _gameid_.

The full JSON format of a hand resource.

```json
{
    "body": "As a/an [actor], I should be able to [feature] so that i can [benefit]"
}
```

#### Example
##### Request:
```http
PUT /api/v0.1/hand/69d44d20-ea8a-4779-8d1f-e16e3e9b6de5 HTTP/1.1
User-Agent: curl/7.41.0
Host: localhost:5000
Accept: */*
Cookie: session=f30d43c5-cc20-4900-a1a1-f12f135d2fdf
Content-Type: application/json
Content-Length: 87

{
    "body": "As a/an [actor], I should be able to [feature] so that I can [benefit]."
}

```

##### Response:
```http
HTTP/1.1 202 ACCEPTED
Server: gunicorn/19.2.1
Date: Sat, 28 Mar 2015 21:45:14 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 72
Set-Cookie: session=f30d43c5-cc20-4900-a1a1-f12f135d2fdf; HttpOnly; Path=/

{
  "job_id": "0302b029-2f8d-481e-b51a-b62066cbb943", 
  "status": 202
}

```

### DELETE /api/v0.1/hand/{gameid}
Destroy hand for game _gameid_.

__TO DO__
