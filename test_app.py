import pytest
from app import app, db
from models import Hero, Power, HeroPower

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed some data for testing
            hero1 = Hero(name="Superman", super_name="Clark Kent")
            hero2 = Hero(name="Batman", super_name="Bruce Wayne")
            power1 = Power(name="Flight", description="Ability to fly")
            power2 = Power(name="Strength", description="Superhuman strength")
            db.session.add_all([hero1, hero2, power1, power2])
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_heroes(client):
    response = client.get('/heroes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(h['name'] == "Superman" for h in data)
    assert all('id' in h and 'name' in h and 'super_name' in h for h in data)

def test_get_hero_by_id(client):
    # Get hero with id 1
    response = client.get('/heroes/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == "Superman"
    assert data['super_name'] == "Clark Kent"
    # According to README, hero_powers is not required, so we check keys
    assert 'hero_powers' in data

def test_get_hero_not_found(client):
    response = client.get('/heroes/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_get_powers(client):
    response = client.get('/powers')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(p['name'] == "Flight" for p in data)
    assert all('id' in p and 'name' in p and 'description' in p for p in data)

def test_patch_power_description(client):
    # Valid update
    response = client.patch('/powers/1', json={"description": "Enhanced ability to fly"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['description'] == "Enhanced ability to fly"

def test_patch_power_description_invalid(client):
    # Description empty or too short should fail
    response = client.patch('/powers/1', json={"description": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data

def test_create_hero_power(client):
    # Valid creation
    response = client.post('/hero_powers', json={
        "strength": "Strong",
        "hero_id": 1,
        "power_id": 2
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['strength'] == "Strong"
    assert data['hero_id'] == 1
    assert data['power_id'] == 2

def test_create_hero_power_invalid_strength(client):
    response = client.post('/hero_powers', json={
        "strength": "Very Strong",
        "hero_id": 1,
        "power_id": 2
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data
