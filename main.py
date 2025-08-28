from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load your JSON data
with open("kanto_data (1).json", "r", encoding="utf-8") as f:
    pokemon_data = json.load(f)

# Route to get all Pokémon
@app.route("/pokemon", methods=["GET"])
def get_all_pokemon():
    return jsonify(pokemon_data)

# Route to get specific Pokémon by name
@app.route("/pokemon/<name>", methods=["GET"])
def get_pokemon(name):
    name = name.capitalize()  # Ensure first letter uppercase
    if name in pokemon_data:
        return jsonify(pokemon_data[name])
    else:
        return jsonify({"error": "Pokémon not found"}), 404

# Route to search by National Id
@app.route("/pokemon/id/<int:national_id>", methods=["GET"])
def get_pokemon_by_id(national_id):
    for poke in pokemon_data.values():
        if poke["Basic_Info"]["National_Id"] == national_id:
            return jsonify(poke)
    return jsonify({"error": "Pokémon not found"}), 404

# Optional: Route to filter by type
@app.route("/pokemon/type/<poke_type>", methods=["GET"])
def get_pokemon_by_type(poke_type):
    poke_type = poke_type.capitalize()
    result = {}
    for name, poke in pokemon_data.items():
        types = [t.strip() for t in poke["Basic_Info"]["Type"].split()]
        if poke_type in types:
            result[name] = poke
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No Pokémon found with this type"}), 404

if __name__ == "__main__":
    app.run(debug=True)
