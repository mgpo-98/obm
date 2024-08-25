# # ai_utils.py

# import tensorflow as tf
# from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
# from tensorflow.keras.preprocessing import image
# import numpy as np

# # Load the pre-trained InceptionV3 model
# model = tf.keras.applications.InceptionV3(weights='imagenet')

# def generate_tags(image_path):
#     """Generate tags for the given image using a pre-trained AI model."""
#     img = image.load_img(image_path, target_size=(299, 299))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = preprocess_input(img_array)
    
#     preds = model.predict(img_array)
#     tags = decode_predictions(preds, top=5)[0]  # Get top 5 predictions
#     return [tag[1] for tag in tags]
