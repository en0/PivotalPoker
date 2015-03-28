#### To Run Server
```bash
cd src/
gunicorn -k gevent -b IP:PORT run:app
```
