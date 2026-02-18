import datetime
from models import User, Event, RSVP

def test_check_user_password():


    # arrange: create user
    user = User(username="Eric")
    user.set_password("securepassword123")

    # act & : check password
    assert user.password_hash != "securepassword123"
    assert user.check_password("securepassword123") is True
    assert user.check_password("wrongpassword") is False

def test_event_to_dict_includes_attendees():
    event = Event(
        title="Python Meetup",
        date=datetime.datetime(2026, 3, 10, 18, 0),
        created_by=1
    )
    r1 = RSVP(event_id=1, user_id=10, attending=True)
    r2 = RSVP(event_id=1, user_id=11, attending=False)
    event.rsvps = [r1, r2]

    data = event.to_dict()

    assert data["title"] == "Python Meetup"
    assert data["rsvp_count"] == 2
    assert data["attendees"] == [10]