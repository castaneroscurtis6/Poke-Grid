"""
Pokemon 9-Box Grid Game
Similar to Hoop Grid - find Pokemon that match row and column categories
Lower score is better (rarer picks = fewer points)
"""

import json
import random
from typing import Dict, List, Set, Tuple


class PokemonGridGame:
    def __init__(self):
        self.pokemon_data = self.load_pokemon_data()
        self.row_categories = []
        self.col_categories = []
        self.grid_answers = {}  # (row, col) -> set of valid pokemon
        self.user_picks = {}  # (row, col) -> pokemon name
        self.pick_counts = {}  # pokemon name -> how many times picked across all players
        
    def load_pokemon_data(self) -> Dict:
        """Load Pokemon data with their attributes"""
        # Sample data structure - you can expand this significantly
        return {
            "Charizard": {
                "types": ["Fire", "Flying"],
                "generation": 1,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Kanto"
            },
            "Pikachu": {
                "types": ["Electric"],
                "generation": 1,
                "evolution_stage": 1,
                "legendary": False,
                "region": "Kanto"
            },
            "Mewtwo": {
                "types": ["Psychic"],
                "generation": 1,
                "evolution_stage": 1,
                "legendary": True,
                "region": "Kanto"
            },
            "Greninja": {
                "types": ["Water", "Dark"],
                "generation": 6,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Kalos"
            },
            "Lucario": {
                "types": ["Fighting", "Steel"],
                "generation": 4,
                "evolution_stage": 2,
                "legendary": False,
                "region": "Sinnoh"
            },
            "Garchomp": {
                "types": ["Dragon", "Ground"],
                "generation": 4,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Sinnoh"
            },
            "Rayquaza": {
                "types": ["Dragon", "Flying"],
                "generation": 3,
                "evolution_stage": 1,
                "legendary": True,
                "region": "Hoenn"
            },
            "Blaziken": {
                "types": ["Fire", "Fighting"],
                "generation": 3,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Hoenn"
            },
            "Gyarados": {
                "types": ["Water", "Flying"],
                "generation": 1,
                "evolution_stage": 2,
                "legendary": False,
                "region": "Kanto"
            },
            "Dragonite": {
                "types": ["Dragon", "Flying"],
                "generation": 1,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Kanto"
            },
            "Salamence": {
                "types": ["Dragon", "Flying"],
                "generation": 3,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Hoenn"
            },
            "Metagross": {
                "types": ["Steel", "Psychic"],
                "generation": 3,
                "evolution_stage": 3,
                "legendary": False,
                "region": "Hoenn"
            },
        }
    
    def generate_daily_grid(self, seed: int = None):
        """Generate a new grid with random categories"""
        if seed:
            random.seed(seed)
        
        # Define possible categories
        type_categories = [
            ("Type: Fire", lambda p: "Fire" in p["types"]),
            ("Type: Water", lambda p: "Water" in p["types"]),
            ("Type: Dragon", lambda p: "Dragon" in p["types"]),
            ("Type: Flying", lambda p: "Flying" in p["types"]),
            ("Type: Steel", lambda p: "Steel" in p["types"]),
            ("Type: Psychic", lambda p: "Psychic" in p["types"]),
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
        
        # Randomly select categories
        all_categories = type_categories + region_categories + other_categories
        selected = random.sample(all_categories, 6)
        
        self.row_categories = [selected[i] for i in range(3)]
        self.col_categories = [selected[i] for i in range(3, 6)]
        
        # Calculate valid answers for each grid cell
        self.grid_answers = {}
        for row in range(3):
            for col in range(3):
                row_name, row_func = self.row_categories[row]
                col_name, col_func = self.col_categories[col]
                
                valid_pokemon = set()
                for poke_name, poke_data in self.pokemon_data.items():
                    if row_func(poke_data) and col_func(poke_data):
                        valid_pokemon.add(poke_name)
                
                self.grid_answers[(row, col)] = valid_pokemon
    
    def is_valid_answer(self, row: int, col: int, pokemon_name: str) -> bool:
        """Check if a Pokemon is valid for a given grid cell"""
        return pokemon_name in self.grid_answers.get((row, col), set())
    
    def submit_answer(self, row: int, col: int, pokemon_name: str) -> bool:
        """Submit an answer for a grid cell"""
        if self.is_valid_answer(row, col, pokemon_name):
            self.user_picks[(row, col)] = pokemon_name
            # Track pick count (in real implementation, this would be stored in database)
            self.pick_counts[pokemon_name] = self.pick_counts.get(pokemon_name, 0) + 1
            return True
        return False
    
    def calculate_rarity_score(self, pokemon_name: str) -> int:
        """
        Calculate score based on rarity
        Lower score = rarer pick = better
        Score is based on how many times this Pokemon has been picked
        """
        pick_count = self.pick_counts.get(pokemon_name, 0)
        
        # In a real implementation with many players:
        # - Most common picks might have 1000+ selections = 100 points
        # - Rare picks might have <10 selections = 1-10 points
        # For demo purposes, we'll simulate this
        
        if pick_count == 0:
            return 1  # Extremely rare, first picker!
        elif pick_count < 10:
            return 5
        elif pick_count < 50:
            return 25
        elif pick_count < 100:
            return 50
        else:
            return 100
    
    def calculate_total_score(self) -> int:
        """Calculate total score for all picks (lower is better)"""
        total = 0
        for pokemon_name in self.user_picks.values():
            total += self.calculate_rarity_score(pokemon_name)
        return total
    
    def display_grid(self):
        """Display the current game grid"""
        print("\n" + "="*80)
        print("POKEMON GRID GAME")
        print("="*80)
        print("\nFind a Pokemon that matches both the row and column categories!")
        print("Lower score is better (rarer picks = fewer points)\n")
        
        # Header
        print(f"{'':20} | {self.col_categories[0][0]:20} | {self.col_categories[1][0]:20} | {self.col_categories[2][0]:20}")
        print("-" * 88)
        
        # Rows
        for row in range(3):
            row_name = self.row_categories[row][0]
            cells = []
            for col in range(3):
                if (row, col) in self.user_picks:
                    pokemon = self.user_picks[(row, col)]
                    score = self.calculate_rarity_score(pokemon)
                    cells.append(f"{pokemon} ({score}pts)")
                else:
                    cells.append("[ ? ]")
            
            print(f"{row_name:20} | {cells[0]:20} | {cells[1]:20} | {cells[2]:20}")
        
        if self.user_picks:
            print(f"\nCurrent Score: {self.calculate_total_score()} points")
            print("(Lower is better!)")
    
    def get_grid_stats(self):
        """Display statistics about valid answers per cell"""
        print("\n" + "="*80)
        print("GRID STATISTICS")
        print("="*80)
        
        for row in range(3):
            for col in range(3):
                valid_pokemon = self.grid_answers[(row, col)]
                print(f"\nCell ({row}, {col}): {len(valid_pokemon)} valid Pokemon")
                print(f"Row: {self.row_categories[row][0]}")
                print(f"Col: {self.col_categories[col][0]}")
                print(f"Valid: {', '.join(sorted(valid_pokemon))}")


def main():
    """Main game loop"""
    game = PokemonGridGame()
    game.generate_daily_grid(seed=42)  # Use seed for reproducible grid
    
    print("Welcome to Pokemon Grid Game!")
    print("\nCommands:")
    print("  play - Start playing the grid")
    print("  stats - View grid statistics")
    print("  score - View current score")
    print("  quit - Exit game")
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command == "quit":
            break
        elif command == "stats":
            game.get_grid_stats()
        elif command == "score":
            print(f"\nCurrent Score: {game.calculate_total_score()} points")
            print("Picks made: {}/9".format(len(game.user_picks)))
        elif command == "play":
            game.display_grid()
            
            if len(game.user_picks) >= 9:
                print("\nGrid complete! Final score: {} points".format(game.calculate_total_score()))
                continue
            
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))
                
                if (row, col) in game.user_picks:
                    print("You've already filled this cell!")
                    continue
                
                pokemon = input("Enter Pokemon name: ").strip()
                
                if game.submit_answer(row, col, pokemon):
                    score = game.calculate_rarity_score(pokemon)
                    print(f"✓ Correct! {pokemon} is worth {score} points")
                else:
                    valid = game.grid_answers.get((row, col), set())
                    print(f"✗ Incorrect. {pokemon} doesn't match both categories.")
                    print(f"Valid options: {', '.join(sorted(valid))}")
            
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
        else:
            print("Unknown command. Try: play, stats, score, or quit")


if __name__ == "__main__":
    main()