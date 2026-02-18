from datetime import datetime, timezone
from models import User, Event, RSVP

def test_check_user_password():
    # arrange: create user
    user = User(username="Eric")
    user.set_password("securepassword123")

    # act & : check password
    assert user.password_hash != "securepassword123"
    assert user.check_password("securepassword123") is True
    assert user.check_password("wrongpassword") is False


def test_user_to_dict_returns_expected_fields():
    user = User(username="eric", is_admin=True)
    user.id = 1
    user.created_at = datetime(2026, 2, 18, 12, 0, tzinfo=timezone.utc)

    data = user.to_dict()

    assert data["id"] == 1
    assert data["username"] == "eric"
    assert data["is_admin"] is True
    assert data["created_at"] == user.created_at.isoformat()


def test_user_to_dict_returns_expected_fields():
    user = User(username="eric", is_admin=True)
    user.id = 1
    user.created_at = datetime(2026, 2, 18, 12, 0, tzinfo=timezone.utc)

    data = user.to_dict()

    assert data["id"] == 1
    assert data["username"] == "eric"
    assert data["is_admin"] is True
    assert data["created_at"] == user.created_at.isoformat()


def test_event_to_dict_includes_attendees():
    event = Event(
        title="Python Meetup",
        date=datetime(2026, 3, 10, 18, 0),
        created_by=1
    )
    r1 = RSVP(event_id=1, user_id=10, attending=True)
    r2 = RSVP(event_id=1, user_id=11, attending=False)
    event.rsvps = [r1, r2]

    data = event.to_dict()

    assert data["title"] == "Python Meetup"
    assert data["rsvp_count"] == 2
    assert data["attendees"] == [10]


def test_rsvp_to_dict_returns_expected_fields():
    rsvp = RSVP(event_id=10, user_id=2, attending=True)
    rsvp.id = 99
    rsvp.created_at = datetime(2026, 2, 18, 14, 0, tzinfo=timezone.utc)

    data = rsvp.to_dict()

    assert data["id"] == 99
    assert data["event_id"] == 10
    assert data["user_id"] == 2
    assert data["attending"] is True
    assert data["created_at"] == rsvp.created_at.isoformat()
