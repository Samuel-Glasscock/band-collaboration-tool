from django.core import signing
from django.utils import timezone
from datetime import timedelta

def make_invite_token(band_id, ttl_minutes=60):
    payload = {"band_id": band_id, "exp": (timezone.now() + timedelta(minutes=ttl_minutes)).timestamp()}
    return signing.dumps(payload, salt="band-invite")

def parse_invite_token(token):
    payload = signing.loads(token, salt="band-invite", max_age=60*60*24)  # defense-in-depth
    if timezone.now().timestamp() > payload["exp"]:
        raise signing.BadSignature("Invite expired")
    return payload["band_id"]
