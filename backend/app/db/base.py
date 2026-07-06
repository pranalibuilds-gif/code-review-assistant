# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.project import Project  # noqa
from app.models.submission import Submission  # noqa
from app.models.review import Review  # noqa
from app.models.finding import Finding  # noqa
from app.models.metric import Metric  # noqa
from app.models.artifact import Artifact  # noqa
