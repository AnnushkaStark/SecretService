from datetime import date
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from models import Secret


class SecretFilter(Filter):
    created_at__gte: Optional[date] = None
    created_at__lte: Optional[date] = None

    class Constants(Filter.Constants):
        model = Secret
