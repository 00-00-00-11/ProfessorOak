def oak_score(target_species, predictions):
    # Load modules
    import math
    import numpy as np
    import json

    # target_species = 'Vaporeon'

    # Load pokedex
    json_file_path = "pokedex.json"
    with open(json_file_path, 'r') as j:
        pokedex = json.loads(j.read())

    # Sort predictions and match
    sort_index = np.argsort(predictions, axis=1)[:, ::-1]
    sort_scores = predictions[:, sort_index]
    sort_species = np.asarray(pokedex['Name'])[sort_index]

    # Extract score for target
    target_score = sort_scores[:, sort_species == target_species][0, 0]

    # Create "remaining" arrays with target removed
    remaining_species = sort_species.reshape(1, 151)[sort_species != target_species]
    remaining_index = sort_index[sort_species != target_species]
    remaining_scores = sort_scores[0, 0, 0:151].reshape(1, 151)[sort_species != target_species]

    # Generate top 3
    top3_scores = sort_scores[0, 0, (0, 1, 2)]
    top3_species = sort_species[0, (0, 1, 2)]
    top3n = top3_scores[top3_scores > 0.001]

    # OUTPUT FORMAT
    # % of actual target (TARGET_PERCENT)
    # First guess species (1S)
    # First guess confidence (1C)
    # First guess points (1P)
    # First guess matching criteria (1M)
    # Second guess species (2S)
    # Second guess confidence (2C)
    # Second guess points (2P)
    # Second guess matching criteria (2M)
    # Third guess species (3S)
    # Third guess confidence (3C)
    # Third guess points (3P)
    # Third guess matching criteria (3M)
    # Total points scaled to skill (FINAL)

    # Output if 100% correct guess
    if round(target_score, 3) == 1 and top3_species[0] == target_species:
        output = {
            "TARGET_PERCENT": [100],
            "1S": [None], "1C": [None], "1P": [None], "1M": [None],
            "2S": [None], "2C": [None], "2P": [None], "2M": [None],
            "3S": [None], "3C": [None], "3P": [None], "3M": [None],
            "FINAL": [100]
        }
    else:
        # Output of top guesses
        target_percent = round(target_score * 100, 1)

        # Create empty array of size 3 * 3
        guesses_array = np.array([[None, None, None, None],
                                  [None, None, None, None],
                                  [None, None, None, None]])

        # Generate own metadata
        own_entry = pokedex['Name'].index(target_species)
        own_metadata = (pokedex["Type.1"][own_entry],
                        pokedex["Type.2"][own_entry],
                        pokedex["Family"][own_entry],
                        pokedex["Body.type"][own_entry])

        # Loop through possible predictions
        for G in range(len(top3n)):
            # Find species metadata
            entry = pokedex['Name'].index(top3_species[G])
            target_metadata = (pokedex["Type.1"][entry],
                               pokedex["Type.2"][entry],
                               pokedex["Family"][entry],
                               pokedex["Body.type"][entry])

            # Check if type1 in target type1 or type2
            if own_metadata[0] in (target_metadata[0], target_metadata[1]):
                type = 1
            else:
                type = 0

            # Check again if type2 exists
            if own_metadata[1] != 'NA':
                # Check if type2 in target type1 or type2
                if own_metadata[1] in (target_metadata[0], target_metadata[1]):
                    type = 1

            # Check family tree
            if own_metadata[2] == target_metadata[2]:
                tree = 1
            else:
                tree = 0

            # Check body shape
            if own_metadata[3] == target_metadata[3]:
                shape = 1
            else:
                shape = 0

            # Sum and weight points
            point_sum = type + tree + shape
            point_weight = point_sum * (3, 2, 1)[G]

            # Assemble matching criteria
            # 3-char string, T = type, F = family, S = shape
            # X if no match, OOO if guess is the target species
            if top3_species[G] == target_species:
                match = '000'
            else:
                match_1 = 'T' if type == 1 else 'X'
                match_2 = 'F' if tree == 1 else 'X'
                match_3 = 'S' if shape == 1 else 'X'
                match = match_1 + match_2 + match_3

            # Add score to array
            guesses_array[G, 0] = top3_species[G]
            guesses_array[G, 1] = round(top3_scores[G] * 100, 1)
            guesses_array[G, 2] = point_weight
            guesses_array[G, 3] = match

        # Extract total
        total = sum(guesses_array[range(0, G + 1), 2]) + target_percent

        # Scale total to Oak's power
        oak_max = entry = pokedex['Power'][own_entry]
        scale_coefficient = 100 / oak_max
        final_score = math.ceil(((total * scale_coefficient) / 28) * 100)
        if final_score > 100:
            final_score = 100

        # Output to json
        output = {
            "TARGET_PERCENT": [target_percent],
            "1S": [guesses_array[0, 0]], "1C": [guesses_array[0, 1]],
            "1P": [guesses_array[0, 2]], "1M": [guesses_array[0, 3]],
            "2S": [guesses_array[1, 0]], "2C": [guesses_array[1, 1]],
            "2P": [guesses_array[1, 2]], "2M": [guesses_array[1, 3]],
            "3S": [guesses_array[2, 0]], "3C": [guesses_array[2, 1]],
            "3P": [guesses_array[2, 2]], "3M": [guesses_array[2, 3]],
            "FINAL": [final_score]
        }

    json_output = json.dumps(output)
    return (json_output)
