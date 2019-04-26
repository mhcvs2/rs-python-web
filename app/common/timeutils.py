from datetime import datetime
from datetime import timedelta
from datetime import tzinfo


class zulutime(tzinfo):
    """A tzinfo class for zulu time"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "Z"

    def dst(self, dt):
        return timedelta(0)


def utcnow_aware():
    """An aware utcnow() that uses zulutime for the tzinfo."""
    return datetime.now(zulutime())


def utcnow():
    """A wrapper around datetime.datetime.utcnow(). We're doing this
       because it is mock'ed in some places.
    """
    return datetime.now()


def isotime(tm=None, subsecond=False):
    """Stringify a time and return it in an ISO 8601 format. Subsecond
       information is only provided if the subsecond parameter is set
       to True (default: False).

       If a time (tm) is provided, it will be stringified. If tm is
       not provided, the current UTC time is used instead.

       The timezone for UTC time will be provided as 'Z' and not
       [+-]00:00. Time zone differential for non UTC times will be
       provided as the full six character string format provided by
       datetime.datetime.isoformat() namely [+-]NN:NN.

       If an invalid time is provided such that tm.utcoffset() causes
       a ValueError, that exception will be propagated.
    """

    _dt = tm if tm else utcnow_aware()

    if not subsecond:
        _dt = _dt.replace(microsecond=0)

    # might cause an exception if _dt has a bad utcoffset.
    delta = _dt.utcoffset() if _dt.utcoffset() else timedelta(0)

    ts = None

    if delta == timedelta(0):
        # either we are provided a naive time (tm) or no tm, or an
        # aware UTC time. In any event, we want to use 'Z' for the
        # timezone rather than the full 6 character offset.
        _dt = _dt.replace(tzinfo=None)
        ts = _dt.isoformat()
        ts += 'Z'
    else:
        # an aware non-UTC time was provided
        ts = _dt.isoformat()

    return ts
