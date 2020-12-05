import ML.data_prep as data_prep
import ML.train_model as train_model


data_prep.save_encoder()
(train_images, train_labels, test_images, test_labels) = data_prep.prepare_data()
model = train_model.train_model(train_images, train_labels, test_images, test_labels)
train_model.save_model(model, "model/")