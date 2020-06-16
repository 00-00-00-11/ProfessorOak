# ProfessorOak
Keras-based convolutional neural network to predict Gen1 pokemon from terrible paint drawings

Initial version of Professor Oak, translated into Python.

Requires modules tensorflow, PIL and numpy.

To do list
-------

GUI with Tkinter

Update and test removing white borders on images during preprocessing (i.e, just rescaling to 86x86 and feeding that straight in)


professor_oak.py
------------------------------

Central script. Calls the three peripheral modules and handles I/O.

INPUT VARIABLES

image_path = path to input image: any size, white background, no alpha

target_species = What you've attempted to draw - spelling and capitalisation crucial.

For test images, specify a species name with correct capitalisation. Script will automatically load the right image from the test_images director

OUTPUT VARIABLES

JSON format containing: % accuracy of Oak's guess, Species and score for his top 3 guesses, and adjusted score out of 100


image_preprocessing.py
------------------------------
Takes the input image, crops, rescales, etc.

Returns as PIL image object that, with some reshaping, can be read by Keras.

model_inference.py
------------------------------
Runs the image in the above temp directory through the Professor Oak Convolutional Neural Network (CNN). Returns an array of length 151 of confidence that the image belongs to each pokemon (in pokedex order). Sums to 1.


generate_scores.py
------------------------------

Takes the target and the predictions, and generates scores as a JSON according to a somewhat complex process described in the manual.


professor_oak_cnn.h5
------------------------------
Architecture and weights of the Professor Oak core CNN. Was trained in R - really can't be arsed to port that code over to Python. Will update this if I have any major training breakthroughs...


pokedex.json
------------------------------

Handy reference file of all species, their metadata (type, family, body shape), as well as how well Oak tends to score that species on average, and this same power expressed as a percentage
