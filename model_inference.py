def model_prediction(model):
    # Load modules
    import tensorflow

    # Prepare prediction image
    test_datagen = tensorflow.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
    test_image_array_gen = test_datagen.flow_from_directory("_temp",
                                                            target_size=(86, 86),
                                                            class_mode="categorical")

    # Predict
    predictions = model.predict(test_image_array_gen)
    return(predictions)
