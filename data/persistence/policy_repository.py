from sqlalchemy.orm import Session
from sqlalchemy import and_

from data.model.policy import Policy
from data.model.policy_type import PolicyType


def create_policy(session: Session, policy_type: PolicyType, effect_until: int, applied_level: int) -> Policy:
    """Create and persist a new policy."""
    policy = Policy(policy_type=policy_type.value, effect_until=effect_until, applied_level=applied_level)
    session.add(policy)
    session.commit()
    session.refresh(policy)
    return policy


def get_active_policies(session: Session, current_time: int) -> list[Policy]:
    return session.query(Policy).filter(Policy.effect_until >= current_time).all()


def get_active_policy_by_type(session: Session, policy_type: PolicyType, current_time: int) -> Policy | None:
    """Return the active policy of the given PolicyType, or None if none is active."""
    return session.query(Policy).filter(and_(Policy.policy_type == policy_type.value, Policy.effect_until >= current_time)).first()


def get_policy_by_type(session: Session, policy_type: PolicyType) -> Policy | None:
    """Return any policy of the given PolicyType (active or expired), or None if none exists."""
    return session.query(Policy).filter(Policy.policy_type == policy_type.value).first()


def upsert_policy(session: Session, policy_type: PolicyType, effect_until: int, applied_level: int) -> Policy:
    """Create a new policy or update an existing one (active or expired) by type."""
    existing = get_policy_by_type(session, policy_type)
    if existing:
        existing.applied_level = applied_level
        existing.effect_until = effect_until
        session.commit()
        session.refresh(existing)
        return existing

    return create_policy(session, policy_type, effect_until, applied_level)
