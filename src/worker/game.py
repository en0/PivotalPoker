__author__ = 'en0'

import pickle
import models
from redis import Redis
from time import time, sleep


class Game(object):

    @classmethod
    def get_games(cls, db):
        for _game_key in db.hkeys("PokerGame"):
            yield _game_key

    def __init__(self, game_id, db):
        assert isinstance(db, Redis)
        self._db = db
        self._game_id = game_id
        self._queue = "PokerGame:{0}:queue".format(self._game_id)
        self._heart_beat_key = "PokerGameHeartBeat:{0}".format(self._game_id)

    def is_game_orphaned(self):
        # verify game is orphaned
        return self._db.get(self._heart_beat_key) is None

    def decode_item(self, serial_string):
        d = None
        try:
            # Try to unpack the queue item. if the queue data is not formatted correctly,
            # it will though a KeyError.
            d = pickle.loads(serial_string)
            return models.QueueItem(document=d, db=self._db)
        except KeyError as e:
            # If we where able to load some of it, try to get the job_id out
            # so we can set the error code.
            if type(d) is dict and d.get('job_id') is not None:
                _job = models.BackgroundJob.load(d.get('job_id'), db=self._db)
                if _job is not None:
                    _job.status = 500
                    _job.message = e.message
                    _job.save()

        # Failed. item is not valid
        return None

    def keep_alive(self):
        # Key expires in 20 seconds. this must be called
        # on every loop of the worker to keep the key alive.
        self._db.setex(self._heart_beat_key, time(), 20)

    def reload(self):
        return models.Game.load(self._game_id, db=self._db)

    def __call__(self, event):

        _game_ids = self._db.hkeys('PokerGame')
        print("waiting on queue: {0}".format(self._queue))

        # Load the game model
        _model = self.reload()

        # Loop while the game exists.
        while self._game_id in _game_ids and not event.is_set():

            # Verify owner exists
            if len(self._db.keys("session:{0}".format(_model.owner_id))) == 0:
                print("NOTICE: Owner's session expired for game {0}. Close game.".format(self._game_id))
                _model.delete()
                break

            # Heart Beat
            self.keep_alive()

            # Get next item from game queue.
            _val = self._db.blpop(self._queue, timeout=10)

            if _val:
                # Unpack the queued item
                _, v = _val
                _item = self.decode_item(v)

                if _item is None:
                    # Failed to understand request, Skip it.
                    continue

                # Process the request.
                # noinspection PyBroadException
                try:
                    self.process(_model, _item)
                except:
                    _item.set_job_status(500, message="The job encountered an unknown error.")

            # re-pull game ids so we can verify our game is still in play
            _game_ids = self._db.hkeys('PokerGame')

        print("Exiting: {0}".format(self._queue))

    def process(self, game_model, item):
        # [ 'Open', 'Playing', 'Reviewing' ]
        result = False
        if item.doc_type == models.WorkerRequest.__document_namespace__:
            result = self.process_worker_request(game_model, item)
        elif item.doc_type == models.Player.__document_namespace__:
            result = self.porcess_add_player(game_model, item)
        elif item.doc_type == models.Hand.__document_namespace__:
            result = self.process_deal_hand(game_model, item)
        elif item.doc_type == models.Vote.__document_namespace__:
            result = self.process_cast_vote(game_model, item)
        elif item.doc_type == models.Result.__document_namespace__:
            result = self.process_accept_vote(game_model, item)

        print "Process success: {0}".format(result)

        if not result:
            item.set_job_status(503, message="Failed to process job")

        return result

    def process_worker_request(self, game_model, item):
        _request = models.WorkerRequest(document=item.data)
        if _request.action == 'remove_player':
            return self.process_remove_player(game_model, item)
        elif _request.action == 'abort_hand':
            return self.process_abort_hand(game_model, item)
        elif _request.action == 'close_game':
            return self.process_close_game(game_model, item)
        return item.set_job_status(400, message="Unknown action request.")

    def porcess_add_player(self, game_model, item):
        if game_model.state == 'Open':
            _player = models.Player(document=item.data)

            # Verify password (even null passwords)
            if game_model.password != _player.password:
                return item.set_job_status(401, message="Wrong password.")

            elif _player.player_id in game_model.players:
                # Player already joined, Just fake a join and move on.
                return item.set_job_status(200, message="Rejoining the game.")

            # Add player to the game
            game_model.add_player(player=_player)
            _ret = game_model.save()

            if _ret:
                return item.set_job_status(200, message="Joining the game.")

            return False

        return item.set_job_status(409, message="The game is not open.")

    def process_remove_player(self, game_model, item):
        _request = models.WorkerRequest(document=item.data)

        # Only the user can remove anyone. otherwise users can only remove themselves.
        if _request.params == _request.request_by or _request.request_by == game_model.owner_id:
            game_model.remove_player(player_id=_request.params)
            _ret = game_model.save()
            if _ret:
                return item.set_job_status(200, message="Player removed.")

            return False

        return item.set_job_status(403, message="Request Forbidden")

    def process_deal_hand(self, game_model, item):
        if game_model.state != 'Open':
            return item.set_job_status(409, message="The game is not open.")

        # Add the hand to the game and set the state to playing.
        _hand = models.Hand(document=item.data)
        game_model.current_hand = _hand.private_entity
        game_model.state = 'Playing'

        _ret = game_model.save()
        if _ret:
            return item.set_job_status(200, message="Hand dealt.")

        return False

    def process_abort_hand(self, game_model, item):
        _request = models.WorkerRequest(document=item.data)

        if game_model.state != 'Playing':
            return item.set_job_status(409, message="No hand in play.")

        if _request.request_by != game_model.owner_id:
            return item.set_job_status(403, message="Request Forbidden")

        game_model.current_hand = None
        game_model.state = 'Open'
        _ret = game_model.save()

        if _ret:
            return item.set_job_status(200, message="Hand canceled.")

        return False

    def process_close_game(self, game_model, item):
        _request = models.WorkerRequest(document=item.data)
        if game_model.owner_id != _request.request_by:
            return item.set_job_status(403, message="Request Forbidden")

        game_model.delete()
        return item.set_job_status(200, message="Game has ended")

    def process_cast_vote(self, game_model, item):
        if game_model.state != 'Playing':
            return item.set_job_status(409, message="No hand in play.")

        _vote = models.Vote(document=item.data)
        _player_name = game_model.players.get(_vote.player_id)

        # verify player_id is playing
        if not _player_name:
            return item.set_job_status(401, message="You are not in this game.")

        # Cast vote and possibly close hand
        game_model.cast_vote(_vote)
        _ret = game_model.save()

        if _ret:
            return item.set_job_status(200, message="Vote accepted.")

        return False

    def process_accept_vote(self, game_model, item):
        if game_model.state != 'Reviewing':
            return item.set_job_status(409, message="The hand is not ready.")

        _result = models.Result(document=item.data)

        if 'Accept' == _result.result:
            try:
                _p = int(_result.points)
                if _p not in game_model.pts_scale:
                    return item.set_job_status(400, message="{0} is not a valid value for this game.".format(_p))
            except ValueError:
                return item.set_job_status(500, message="{0} is not a valid result.".format(_result.points))
            game_model.complete_hand(_p)
            _ret = game_model.save()
            if _ret:
                return item.set_job_status(200, message="Hand complete.")
            return False

        elif 'Revote' == _result.result:
            game_model.resetVote()
            _ret = game_model.save()
            if _ret:
                return item.set_job_status(200, message="Reset hand complete.")
            return False

        elif 'Cancel' == _result.result:
            game_model.current_hand = None
            game_model.state = 'Open'
            _ret = game_model.save()
            if _ret:
                return item.set_job_status(200, message="Hand canceled.")
            return False

        return item.set_job_status(400, message="Unknown result action.")
