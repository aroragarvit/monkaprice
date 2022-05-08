import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("saved_model\my_model")

tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)