from sqlalchemy import func, select

from app.models import User
from app.seed import seed_dev_user


def test_seed_creates_dev_user_exactly_once(db_session):
    # conftest already created user 1, so remove it to start from an empty table.
    db_session.delete(db_session.get(User, 1))
    db_session.commit()

    assert seed_dev_user(db_session) is True
    assert seed_dev_user(db_session) is False
    assert db_session.scalar(select(func.count()).select_from(User)) == 1