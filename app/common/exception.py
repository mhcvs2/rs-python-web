import re
import logging
from app.common.base_exception import OpenstackException, DatabaseMigrationError

LOG = logging.getLogger(__name__)


DatabaseMigrationError = DatabaseMigrationError


def safe_fmt_string(text):
    return re.sub(r'%([0-9]+)', r'\1', text)


class CWError(OpenstackException):
    """Base exception that all custom app exceptions inherit from."""
    internal_message = None

    def __init__(self, message=None, **kwargs):
        if message is not None:
            self.message = message
        if self.internal_message is not None:
            try:
                LOG.error(safe_fmt_string(self.internal_message), kwargs)
            except Exception:
                LOG.error(self.internal_message)
        self.message = safe_fmt_string(self.message)
        super(CWError, self).__init__(**kwargs)


class NotFound(CWError):

    message = "Resource %(uuid)s cannot be found."


class InvalidModelError(CWError):

    message = "The following values are invalid: %(errors)s."


class ModelNotFoundError(NotFound):

    message = "Not Found."


class DBConstraintError(CWError):

    message = "Failed to save %(model_name)s because: %(error)s."
