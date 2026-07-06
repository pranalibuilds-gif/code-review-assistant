from .enterprise import enterprise_profile
from .medium import medium_profile
from .six_year_history import six_year_history_profile
from .small import small_profile

PROFILES = {
    profile["name"]: profile
    for profile in [small_profile, medium_profile, enterprise_profile, six_year_history_profile]
}


def get_profile(name: str) -> dict:
    profile = PROFILES.get(name)
    if not profile:
        raise ValueError(f"Unknown profile '{name}'. Available profiles: {', '.join(PROFILES)}")
    return profile
