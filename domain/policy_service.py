from sqlalchemy.orm import Session
from data.model.policy_type import PolicyType
from data.persistence.policy_repository import upsert_policy
from domain.sim_data_service import get_sim_time
from domain.utils.policy_utils import get_policy_effect_duration
from data.persistence.policy_repository import get_active_policies
from data.db.db_engine import transactional
from domain.dtos.policy_dto import PolicyDto, PolicyTypeDto
from domain.utils.sim_time_utils import convert_to_sim_time


def create_or_update_policy(session: Session, policy_type: PolicyType, level: int):
    """Create a new policy or update an existing active one.

    Parameters:
        session: DB session
        policy_type: PolicyType enum
        level: grandmaster level to apply
    """

    current_time = get_sim_time(session)
    duration = get_policy_effect_duration(level)
    effect_until = current_time + duration

    return upsert_policy(session, policy_type, effect_until, level)


@transactional
def fetch_active_policies(session: Session) -> list[PolicyDto]:
    current_time = get_sim_time(session)
    active = get_active_policies(session, current_time)

    result: list[PolicyDto] = []
    for p in active:
        try:
            ptype = PolicyTypeDto(p.policy_type)
        except Exception:
            # skip unknown types
            continue
        result.append(PolicyDto(type=ptype, effect_until=convert_to_sim_time(p.effect_until)))

    return result
