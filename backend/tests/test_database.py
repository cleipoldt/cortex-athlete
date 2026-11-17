import pytest
from sqlalchemy.exc import IntegrityError

from app.models import CognitiveSession, User


def test_dev_user_is_seeded(db_session):
    user = db_session.get(User, 1)

    assert user is not None
    assert user.email == "test@example.com"


def test_foreign_keys_are_enforced(db_session):
    db_session.add(CognitiveSession(user_id=999, test_type="simple_reaction"))

    with pytest.raises(IntegrityError):
        db_session.commit()