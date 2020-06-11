# Load sub-modules
im = __import__('image_preprocessing')
pred = __import__('model_inference')
score = __import__('generate_scores')

# Load Oak core
import tensorflow as tf
core = tf.keras.models.load_model("professor_oak_cnn.h5")

# Set input variables
image_path = 'test_images/tentacruel.png'
target_species = 'Tentacruel'

# Perform image pre-processing
im.image_preprocess(image_path)

# Perform model inference
predictions = pred.model_prediction(core)

# Generate final scores
output = score.oak_score(target_species, predictions)
print(output)
