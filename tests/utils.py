from unittest.mock import MagicMock


def create_blob_model_mock(
    id=1,
    first_name='Test',
    last_name='Blob',
    strength=1.0,
    speed=1.0,
    learning=1.0,
    integrity=100,
    born=0,
    terminated=None,
    debut=0,
    contract=0,
    money=0,
    points=0,
    bronze_medals=0,
    silver_medals=0,
    gold_medals=0,
    season_victories=0,
    bronze_trophies=0,
    silver_trophies=0,
    gold_trophies=0,
    championships=0,
    grandmasters=0,
    league_id=None,
    parent_id=None,
    color="#888888",
    current_activity=None
):
    blob = MagicMock()
    blob.id = id
    blob.first_name = first_name
    blob.last_name = last_name
    blob.strength = strength
    blob.speed = speed
    blob.learning = learning
    blob.integrity = integrity
    blob.born = born
    blob.terminated = terminated
    blob.debut = debut
    blob.contract = contract
    blob.money = money
    blob.points = points
    blob.bronze_medals = bronze_medals
    blob.silver_medals = silver_medals
    blob.gold_medals = gold_medals
    blob.season_victories = season_victories
    blob.bronze_trophies = bronze_trophies
    blob.silver_trophies = silver_trophies
    blob.gold_trophies = gold_trophies
    blob.championships = championships
    blob.grandmasters = grandmasters
    blob.league_id = league_id
    blob.parent_id = parent_id
    blob.color = color
    blob.current_activity = current_activity
    return blob


def create_mock_result(position, blob, points, event_id, blob_id):
    result = MagicMock()
    result.position = position
    result.blob = blob
    result.points = points
    result.event_id = event_id
    result.blob_id = blob_id
    return result


def create_mock_blob_competitor(id, points, gold_trophies, name):
    blob = MagicMock()
    blob.id = id
    blob.points = points
    blob.gold_trophies = gold_trophies
    blob.name = name
    return blob
