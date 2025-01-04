from data.db.db_engine import transactional
from data.model.sim_data import SimData


@transactional
def get_sim_data(session) -> SimData:
    query_result = session.query(SimData).first()

    if query_result:
        return query_result
    else:
        raise Exception('SimData not found')


@transactional
def save_sim_data(session, sim_data: SimData):
    session.add(sim_data)
    session.commit()
