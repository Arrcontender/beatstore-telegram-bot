from sqlalchemy.exc import PendingRollbackError, IntegrityError
from .db_engine import session
from beats.beats_list import beats_for_db
from .db_map import Beats


def init_beats():
    for i in beats_for_db:
        beat = Beats(name=i['name'], url=i['url'], genre=i['genre'], leasing=i['leasing'], exclusive=i['exclusive'])
        session.add(beat)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        print('False')
        return False