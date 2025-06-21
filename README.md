# Pokemon Trading Card Evolutions Generator

This repository contains a couple of Python scripts for generating Pokemon cards in the style of the Evolutions set.

## How To Use

1. Design cards 
- Add Pokemon art to `resource/pokemon_art`
- Add backgrounds for main card art to `resource/pokemon_backgrounds`
- Update the card details in `cards.csv` 

2. Set up Python and install packages

3. Generate card art.
```bash
python scripts/build_art.py
```

4. Generate finished cards.
```bash
python scripts/build_cards.py
```
