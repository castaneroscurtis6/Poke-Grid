# Pokemon Grid Game

A 9-box grid game similar to Hoop Grid, where players find Pokemon that match row and column categories. The scoring system rewards rarer picks with fewer points, making lower scores better!

## How It Works

- **3x3 Grid**: 3 categories on the left (rows) and 3 categories on top (columns)
- **Goal**: Find a Pokemon that matches BOTH the row and column category for each cell
- **Scoring**: Rarer picks = fewer points = better! Lower total score wins
- **Rarity Calculation**: Based on how many times a Pokemon has been picked by all players

## Features

- Random daily grid generation
- Multiple category types (Type, Region, Generation, Legendary status, Evolution stage)
- Rarity-based scoring system
- Grid statistics viewer
- Command-line interface

## Installation
```bash
git clone 
cd pokemon-grid-game
python pokemon_grid_game.py
```

## How to Play

1. Run the game: `python pokemon_grid_game.py`
2. Type `play` to start
3. Enter the row (0-2) and column (0-2) for the cell you want to fill
4. Enter a Pokemon name that matches both categories
5. Repeat until all 9 cells are filled
6. Try to get the lowest score possible!

## Commands

- `play` - Start playing the grid
- `stats` - View all valid Pokemon for each cell
- `score` - View your current score
- `quit` - Exit the game

## Scoring System

- **1 point**: First person to pick this Pokemon (extremely rare!)
- **5 points**: Picked less than 10 times (very rare)
- **25 points**: Picked 10-49 times (uncommon)
- **50 points**: Picked 50-99 times (common)
- **100 points**: Picked 100+ times (very common)

**Lower score = better!** Challenge yourself to find the most obscure Pokemon that fit each category combination.

## Example Grid
```
                     | Type: Fire          | Type: Dragon        | Region: Kanto
--------------------------------------------------------------------------------
Type: Flying         | Charizard (100pts) | Dragonite (50pts)   | [ ? ]
Legendary            | [ ? ]               | Rayquaza (5pts)     | Mewtwo (25pts)
Generation 3         | Blaziken (50pts)    | [ ? ]               | [ ? ]
```

## Expanding the Game

### Adding More Pokemon

Edit the `load_pokemon_data()` method to add more Pokemon:
```python
"PokemonName": {
    "types": ["Type1", "Type2"],
    "generation": 1,
    "evolution_stage": 1,
    "legendary": False,
    "region": "RegionName"
}
```

### Adding New Categories

You can add new category types in the `generate_daily_grid()` method:
```python
new_categories = [
    ("Category Name", lambda p: p["attribute"] == value),
]
```

### Database Integration

For a production version, you would want to:
- Store Pokemon data in a database
- Track pick counts across all players in a database
- Store daily grids and player scores
- Add user authentication

## Future Enhancements

- [ ] Load Pokemon data from PokeAPI
- [ ] Web interface with Flask/Django
- [ ] Daily challenge mode with leaderboards
- [ ] Persistent storage with SQLite/PostgreSQL
- [ ] Share results with friends
- [ ] Hint system
- [ ] Timed mode

## Contributing

Feel free to fork and add more features!

## License

MIT License

