import tensorflow as tf
from data_prep import prepare_data

(train_images, train_labels, test_images, test_labels) = prepare_data()

model = tf.keras.models.load_model('./model/')

test_loss, test_acc = model.evaluate(test_images, test_labels)
print('\nTest accuracy: ', test_acc)
print('\nTest loss: ', test_loss)
