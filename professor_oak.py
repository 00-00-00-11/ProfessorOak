# Load sub-modules
im = __import__('image_preprocessing')
pred = __import__('model_inference')
score = __import__('generate_scores')

# Load Oak core
import tensorflow as tf

core = tf.keras.models.load_model("professor_oak_cnn.h5")

# Set input variables
target_species = 'Slowbro'
image_path = 'test_images/' + target_species.lower() + '.png'

# Perform image pre-processing
input_image = im.image_preprocess(image_path)

# Perform model inference
predictions = pred.model_prediction(input_image, core)

# Generate final scores
output = score.oak_score(target_species, predictions)

# Print human-readable output
import json
import numpy as np

results = json.loads(output)

if results['TARGET_PERCENT'][0] == 100:
    print('I correctly guessed ' + target_species + ' with 100% confidence. 100 points!')
else:
    # Print target score
    print('I guessed ' + target_species + ' with ' + str(results['TARGET_PERCENT'][0]) +
          '% confidence. ' + str(round(results['TARGET_PERCENT'][0] / 10)) + ' points!')

    # Extract results to array
    guesses_array = np.array([[results['1S'][0], results['1C'][0], results['1P'][0], results['1M'][0]],
                              [results['2S'][0], results['2C'][0], results['2P'][0], results['2M'][0]],
                              [results['3S'][0], results['3C'][0], results['3P'][0], results['3M'][0]]])

    # Determine number of guesses made
    nguesses = (results['1S'][0] is not None,
                results['2S'][0] is not None,
                results['3S'][0] is not None)
    nguesses = sum(nguesses)

    # Create verbal vectors for text output
    verbal_vector_numbers = ("first", 'second', 'third')
    verbal_vector_matches = ['Same type. ', 'Same family. ', 'Same body shape.']

    for G in range(nguesses):
        # Determine matching criteria
        if guesses_array[G, 3] == '000':
            # Output nothing if this is the target
            VV = 'Same species'
        else:
            # Extract match criteria code
            matches = list(guesses_array[G, 3])

            # Extract any non-x elements
            VV = ''
            for j in range(len(matches)):
                if matches[j] != 'X':
                    VV = VV + verbal_vector_matches[j]

        # Print concatenated output
        print(
            'My ' + verbal_vector_numbers[G] + ' guess was ' + guesses_array[G, 0] +
            ' (' + str(guesses_array[G, 1]) + '%). ' +
            str(guesses_array[G, 2]) + ' points! (' + VV + ')'
        )
    print('Scaled to my own skill, my final score is', str(results['FINAL'][0]) +
          ' out of 100!')