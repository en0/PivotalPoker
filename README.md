#### To Run Server
```bash
cd src/
gunicorn -k gevent -b IP:PORT run:app
```

## REST Api

* Session
  * PUT /api/v0.1/session: Start user session.
  * GET /api/v0.1/session: Retrieve user session.
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
