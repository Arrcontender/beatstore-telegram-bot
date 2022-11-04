from sqlalchemy.exc import IntegrityError
from .db_engine import session
from details.beats_list import beats_for_db
from .db_map import Beats


def init_beats():
    """ Beats initialization via database access  """
    db_list = []
    for x in session.query(Beats.name).all():
        db_list.append(x[0])
    for i in beats_for_db:
        if i.get('name', 'NotAllowed') not in db_list:
            beat = Beats(name=i['name'], url=i['url'], genre=i['genre'],
                         leasing=i['leasing'], exclusive=i['exclusive'])
            session.add(beat)
            try:
                session.commit()
                db_list.append(i['name'])
            except IntegrityError:
                session.rollback()
                return False
    return True


