"""
Pokemon Grid Game - Flask Web Version
"""

from flask import Flask, render_template, request, jsonify, session
import json
import random
from datetime import date
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management


class PokemonGridGame:
    def __init__(self):
        self.pokemon_data = self.load_pokemon_data()
        
    def load_pokemon_data(self):
        """Load Pokemon data with their attributes"""
        return {
            "Charizard": {"types": ["Fire", "Flying"], "generation": 1, "evolution_stage": 3, "legendary": False, "region": "Kanto"},
            "Pikachu": {"types": ["Electric"], "generation": 1, "evolution_stage": 1, "legendary": False, "region": "Kanto"},
            "Mewtwo": {"types": ["Psychic"], "generation": 1, "evolution_stage": 1, "legendary": True, "region": "Kanto"},
            "Greninja": {"types": ["Water", "Dark"], "generation": 6, "evolution_stage": 3, "legendary": False, "region": "Kalos"},
            "Lucario": {"types": ["Fighting", "Steel"], "generation": 4, "evolution_stage": 2, "legendary": False, "region": "Sinnoh"},
            "Garchomp": {"types": ["Dragon", "Ground"], "generation": 4, "evolution_stage": 3, "legendary": False, "region": "Sinnoh"},
            "Rayquaza": {"types": ["Dragon", "Flying"], "generation": 3, "evolution_stage": 1, "legendary": True, "region": "Hoenn"},
            "Blaziken": {"types": ["Fire", "Fighting"], "generation": 3, "evolution_stage": 3, "legendary": False, "region": "Hoenn"},
            "Gyarados": {"types": ["Water", "Flying"], "generation": 1, "evolution_stage": 2, "legendary": False, "region": "Kanto"},
            "Dragonite": {"types": ["Dragon", "Flying"], "generation": 1, "evolution_stage": 3, "legendary": False, "region": "Kanto"},
            "Salamence": {"types": ["Dragon", "Flying"], "generation": 3, "evolution_stage": 3, "legendary": False, "region": "Hoenn"},
            "Metagross": {"types": ["Steel", "Psychic"], "generation": 3, "evolution_stage": 3, "legendary": False, "region": "Hoenn"},
            "Tyranitar": {"types": ["Rock", "Dark"], "generation": 2, "evolution_stage": 3, "legendary": False, "region": "Johto"},
            "Alakazam": {"types": ["Psychic"], "generation": 1, "evolution_stage": 3, "legendary": False, "region": "Kanto"},
            "Gengar": {"types": ["Ghost", "Poison"], "generation": 1, "evolution_stage": 3, "legendary": False, "region": "Kanto"},
            "Snorlax": {"types": ["Normal"], "generation": 1, "evolution_stage": 2, "legendary": False, "region": "Kanto"},
            "Lapras": {"types": ["Water", "Ice"], "generation": 1, "evolution_stage": 1, "legendary": False, "region": "Kanto"},
            "Articuno": {"types": ["Ice", "Flying"], "generation": 1, "evolution_stage": 1, "legendary": True, "region": "Kanto"},
            "Zapdos": {"types": ["Electric", "Flying"], "generation": 1, "evolution_stage": 1, "legendary": True, "region": "Kanto"},
            "Moltres": {"types": ["Fire", "Flying"], "generation": 1, "evolution_stage": 1, "legendary": True, "region": "Kanto"},
        }
    
    def generate_daily_grid(self, seed=None):
        """Generate a new grid with random categories"""
        if seed:
            random.seed(seed)
        
        type_categories = [
            ("Type: Fire", lambda p: "Fire" in p["types"]),
            ("Type: Water", lambda p: "Water" in p["types"]),
            ("Type: Dragon", lambda p: "Dragon" in p["types"]),
            ("Type: Flying", lambda p: "Flying" in p["types"]),
            ("Type: Steel", lambda p: "Steel" in p["types"]),
            ("Type: Psychic", lambda p: "Psychic" in p["types"]),
            ("Type: Electric", lambda p: "Electric" in p["types"]),
            ("Type: Ice", lambda p: "Ice" in p["types"]),
        ]
        
        region_categories = [
            ("Region: Kanto", lambda p: p["region"] == "Kanto"),
            ("Region: Hoenn", lambda p: p["region"] == "Hoenn"),
            ("Region: Sinnoh", lambda p: p["region"] == "Sinnoh"),
        ]
        
        other_categories = [
            ("Legendary", lambda p: p["legendary"] == True),
            ("Generation 1", lambda p: p["generation"] == 1),
            ("Generation 3", lambda p: p["generation"] == 3),
            ("Fully Evolved", lambda p: p["evolution_stage"] == 3),
        ]
        
        all_categories = type_categories + region_categories + other_categories
        selected = random.sample(all_categories, 6)
        
        row_categories = [selected[i] for i in range(3)]
        col_categories = [selected[i] for i in range(3, 6)]
        
        # Calculate valid answers for each grid cell
        grid_answers = {}
        for row in range(3):
            for col in range(3):
                row_name, row_func = row_categories[row]
                col_name, col_func = col_categories[col]
                
                valid_pokemon = []
                for poke_name, poke_data in self.pokemon_data.items():
                    if row_func(poke_data) and col_func(poke_data):
                        valid_pokemon.append(poke_name)
                
                grid_answers[f"{row},{col}"] = valid_pokemon
        
        return {
            'row_categories': [cat[0] for cat in row_categories],
            'col_categories': [cat[0] for cat in col_categories],
            'grid_answers': grid_answers
        }
    
    def calculate_rarity_score(self, pokemon_name, pick_counts):
        """Calculate score based on rarity"""
        pick_count = pick_counts.get(pokemon_name, 0)
        
        if pick_count == 0:
            return 1
        elif pick_count < 10:
            return 5
        elif pick_count < 50:
            return 25
        elif pick_count < 100:
            return 50
        else:
            return 100


# Initialize game
game = PokemonGridGame()


@app.route('/')
def index():
    """Main game page"""
    # Initialize session if needed
    if 'grid_data' not in session:
        today = str(date.today())
        seed = int(today.replace("-", ""))
        grid_data = game.generate_daily_grid(seed)
        session['grid_data'] = grid_data
        session['user_picks'] = {}
        session['pick_counts'] = {}
    
    return render_template('index.html')


@app.route('/api/grid')
def get_grid():
    """Get current grid data"""
    return jsonify({
        'row_categories': session.get('grid_data', {}).get('row_categories', []),
        'col_categories': session.get('grid_data', {}).get('col_categories', []),
        'user_picks': session.get('user_picks', {})
    })


@app.route('/api/submit', methods=['POST'])
def submit_answer():
    """Submit a Pokemon answer for a cell"""
    data = request.json
    row = data.get('row')
    col = data.get('col')
    pokemon = data.get('pokemon', '').strip()
    
    cell_key = f"{row},{col}"
    grid_answers = session.get('grid_data', {}).get('grid_answers', {})
    valid_pokemon = grid_answers.get(cell_key, [])
    
    # Check if answer is valid
    if pokemon in valid_pokemon:
        # Update session
        user_picks = session.get('user_picks', {})
        user_picks[cell_key] = pokemon
        session['user_picks'] = user_picks
        
        # Update pick counts
        pick_counts = session.get('pick_counts', {})
        pick_counts[pokemon] = pick_counts.get(pokemon, 0) + 1
        session['pick_counts'] = pick_counts
        session.modified = True
        
        # Calculate score
        score = game.calculate_rarity_score(pokemon, pick_counts)
        
        return jsonify({
            'success': True,
            'pokemon': pokemon,
            'score': score,
            'pick_count': pick_counts[pokemon]
        })
    else:
        return jsonify({
            'success': False,
            'message': f'{pokemon} does not match both categories',
            'valid_options': valid_pokemon
        })


@app.route('/api/score')
def get_score():
    """Get current total score"""
    user_picks = session.get('user_picks', {})
    pick_counts = session.get('pick_counts', {})
    
    total_score = 0
    for pokemon in user_picks.values():
        total_score += game.calculate_rarity_score(pokemon, pick_counts)
    
    return jsonify({
        'total_score': total_score,
        'cells_filled': len(user_picks),
        'total_cells': 9
    })


@app.route('/api/reset')
def reset_game():
    """Reset the game"""
    session.clear()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)