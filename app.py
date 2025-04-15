# app.py
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from extensions import db, ma
from models import Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)

@app.route('/')
def home():
    return "Welcome to the Superheroes API!"

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify({
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [
            {
                "hero_id": hp.hero_id,
                "id": hp.id,
                "power": {"id": hp.power.id, "name": hp.power.name, "description": hp.power.description},
                "power_id": hp.power_id,
                "strength": hp.strength
            } for hp in hero.hero_powers
        ]
    })

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description} for p in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({"id": power.id, "name": power.name, "description": power.description})

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.json
    if "description" not in data or len(data["description"]) < 20:
        return jsonify({"errors": ["description must be at least 20 characters long"]}), 400

    power.description = data["description"]
    db.session.commit()
    return jsonify({"id": power.id, "name": power.name, "description": power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json

    if data["strength"] not in ["Strong", "Weak", "Average"]:
        return jsonify({"errors": ["Invalid strength value"]}), 400

    hero_power = HeroPower(strength=data["strength"], hero_id=data["hero_id"], power_id=data["power_id"])
    db.session.add(hero_power)
    db.session.commit()

    return jsonify({
        "id": hero_power.id,
        "hero_id": hero_power.hero_id,
        "power_id": hero_power.power_id,
        "strength": hero_power.strength,
        "hero": {"id": hero_power.hero.id, "name": hero_power.hero.name, "super_name": hero_power.hero.super_name},
        "power": {"id": hero_power.power.id, "name": hero_power.power.name, "description": hero_power.power.description}
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
