def model_prediction(input_image, model):
    # Load modules
    import tensorflow
    import numpy as np

    # Prepare prediction image - OLD METHOD USING TEMP DIRECTORY
    # test_datagen = tensorflow.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
    # test_image_array_gen = test_datagen.flow_from_directory("_temp",
    #                                                        target_size=(86, 86),
    #                                                        class_mode="categorical")
    # Predict
    # predictions_old = model.predict(test_image_array_gen)

    # Prepare image directly
    input_image_array = tensorflow.keras.preprocessing.image.img_to_array(input_image)
    input_image_array_expanded = np.expand_dims(input_image_array, 3) * (1/255)

    # Predict
    predictions = model.predict(input_image_array_expanded.reshape(1, 86, 86, 3))

    return (predictions)
