"""Create the development user (id 1) if it does not exist yet.

Run from backend/:  python -m app.seed
Safe to run any number of times (idempotent).
Until authentication exists (Phase 13), every saved result belongs to user 1.
"""

from sqlalchemy.orm import Session

from app.database import IS_SQLITE, SessionLocal
from app.models import User

DEV_USER_ID = 1


def seed_dev_user(db: Session) -> bool:
    """Create the dev user if missing. Returns True if it was created."""
    if db.get(User, DEV_USER_ID) is not None:
        return False

    db.add(
        User(
            id=DEV_USER_ID,
            email="dev@cortex-athlete.local",
            display_name="Dev Athlete",
        )
    )
    db.commit()
    return True


def main() -> None:
    if not IS_SQLITE:
        raise SystemExit("Refusing to seed: the dev user is only for the local SQLite database.")

    with SessionLocal() as db:
        created = seed_dev_user(db)

    if created:
        print("Created dev user (id 1).")
    else:
        print("Dev user (id 1) already exists. Nothing to do.")


if __name__ == "__main__":
    main()