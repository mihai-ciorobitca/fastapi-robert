from datetime import datetime, timezone

def check_user(user):
    if not user["verification"]:
        print(user)
        created_at = user["created_at"]
        created_at_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        print(created_at_dt)
        now = datetime.now(timezone.utc)
        difference = (now - created_at_dt).days
        print(difference)
        if difference > 3:
            return True
    return False