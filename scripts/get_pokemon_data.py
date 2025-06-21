import asyncio
import aiopoke
import math 
import os 


def get_previous_evolution(evolution_chain, target_name):
    if evolution_chain.species.name == target_name:
        return None  # No previous evolution
    def find_in_chain(current_evolution):
        # Check current node 
        if current_evolution.species.name == target_name:
            return True
        else:
            # Iterate to children 
            for next_evolution in current_evolution.evolves_to:
                next_matches = get_previous_evolution(next_evolution, target_name)
                if next_matches:
                    return current_evolution.species.name

    return find_in_chain(evolution_chain)


def get_next_evolution(evolution_chain, target_name):
    def find_in_chain(current_evolution):
        # Check current node 
        if current_evolution.species.name == target_name:
            if len(current_evolution.evolves_to) == 0:
                return None
            return current_evolution.evolves_to[0].species.name
        else:
            # Iterate to children 
            for next_evolution in current_evolution.evolves_to:
                next_matches = find_in_chain(next_evolution)
                if next_matches:
                    return next_matches
    return find_in_chain(evolution_chain)


def get_stage(evolution_chain, target_name):
    def find_in_chain(current_evolution, stage):
        # Check current node 
        if current_evolution.species.name == target_name:
            if current_evolution.is_baby:
                return 0
            return stage
        else:
            # Iterate to children 
            for next_evolution in current_evolution.evolves_to:
                next_stage = find_in_chain(next_evolution, stage + 1)
                if next_stage:
                    return next_stage
    return find_in_chain(evolution_chain, 1 if not evolution_chain.is_baby else 0)


async def collect_more_data():
    # Create a CSV file with the following columns:
    # id, name, type1, type2, weight, height
    async with aiopoke.AiopokeClient() as client:
        rows = []
        for i in range(1, 251+1):
            print("Collecting '%d'..." % i)
            # Base information 
            pkm = await client.get_pokemon(i)
            print("Collecting %s..." % pkm.name)
            pkm_spec = await client.get_pokemon_species(i)

            inches = math.ceil(pkm.height * (39/10))
            height = "{}'{:02d}\"".format(math.floor(inches / 12), inches % 12)
            weight = "{:.1f}".format(pkm.weight * (199.5/905))

            def get_flavor_text():
                for entry in pkm_spec.flavor_text_entries:
                    if entry.language.name == 'en' and entry.version.name == 'firered':
                        ft = entry.flavor_text.replace('\n', ' ')
                        ft = ft.replace('\u000c', ' ')
                        ft = ft.replace('\x0c', '')
                        return "\"\"\"" + ft + "\"\"\""
                return ""
            flavor_text = get_flavor_text()

            def get_genus():
                for entry in pkm_spec.genera:
                    if entry.language.name == 'en':
                        return entry.genus
                return ""
            genus = get_genus()

            # Evolution 
            evolution_chain = await client.get_evolution_chain(str(pkm_spec.evolution_chain).split('/')[-2]) 
            stage = get_stage(evolution_chain.chain, pkm.name)
            prev_evolution_name = pkm_spec.evolves_from_species.name if pkm_spec.evolves_from_species else None
            next_evolution_name = get_next_evolution(evolution_chain.chain, pkm.name)

            # Calculate a level 
            bst = sum([s.base_stat for s in pkm.stats])
            hst = max([s.base_stat for s in pkm.stats])
            if stage == 0:
                level = 5
            elif stage == 1:
                level = min(5 + int((bst - 200) / 10) + int(hst / 12), 99)
            elif stage == 2:
                level = min(8 + int((bst - 200) / 10) + int(hst / 12), 99)
            elif stage == 3:
                level = min(10 + int((bst - 200) / 10) + int(hst / 12), 99)

            # Calculate a rarity
            if stage == 3 or pkm_spec.is_legendary or pkm_spec.is_mythical or bst > 520:
                rarity = 3
            elif stage == 2 or bst > 420:
                rarity = 2
            elif stage == 1:
                rarity = 1

            # Save to rows 
            rows.append((
                pkm.id, pkm.name, pkm.types[0].type.name, pkm.types[1].type.name if len(pkm.types) > 1 else None, weight, height, 
                genus, stage, prev_evolution_name, next_evolution_name, level, rarity,
                flavor_text,
            ))
            print(rows[-1])

    print("Writing CSV...")
    HEADERS = [
        'id', 
        'name',
        'type1',
        'type2',
        'weight',
        'height',
        'genus',
        'stage',
        'prev_evolution_name',
        'next_evolution_name',
        'level',
        'rarity',
        'flavor_text',
    ]

    csv_file = os.path.join(os.path.dirname(__file__), 'general_data.csv')
    print("Writing to {}...".format(os.path.abspath(csv_file)))
    with open(csv_file, 'w') as f:
        # Write header
        f.write(','.join(HEADERS))
        f.write('\n') 
        # Write each row 
        for row in rows:
            f.write(','.join(map(str, row))) 
            f.write('\n')     



print('Start.')
asyncio.run(collect_more_data())
print('Done.')
