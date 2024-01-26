import pandas as pd
import numpy as np
import tensorflow as tf

from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Import files and merge into one df
# The df holds the original data and predict_df holds the predicted values.
df_scores = pd.read_csv('df_scores.csv')
ky_spending_df = pd.read_csv('preprocessed_df.csv').loc[:,['End Year Code', 'School Code', 'Level Code', 'Reported Spending per student', 'Money Difference per school',]]
df = pd.merge(df_scores, ky_spending_df, on=['End Year Code', 'School Code', 'Level Code'], how='left').sort_values(by=['End Year', 'District Code', 'School Code']).reset_index(drop=True)
predict_df = df.copy()

## Predict Classification: a NN Model
unscaled_df = predict_df.loc[:,['End Year Code', 'District Code', 'Level Code',
                                'Reported Spending per student', 'Money Difference per school',
                                'Proficiency Score', 'Classification Code', ]].dropna(axis =0).reset_index(drop=True)

#Shuffle df and separate into input and targets
unscaled_df = unscaled_df.sample(frac=1, random_state=15)
unscaled_inputs = unscaled_df.values[:,:-1]
targets = unscaled_df.values[:,-1]

# Split into training, validation, and test sets
unscaled_X_train, unscaled_X_set, y_train, y_set = train_test_split(unscaled_inputs, targets,
                                                                    test_size=0.2, random_state=15,
                                                                    stratify = targets)
unscaled_X_valid, unscaled_X_test, y_valid, y_test = train_test_split(unscaled_X_set, y_set,
                                                                      test_size=0.5, random_state=13,
                                                                      stratify = y_set)

# Scale data
epsb_scaler = StandardScaler()

# Calculate and store the mean and sd
epsb_scaler.fit(unscaled_X_train)

# Apply the scaler
scaled_X_train = epsb_scaler.transform(unscaled_X_train)
scaled_X_valid = epsb_scaler.transform(unscaled_X_valid)
scaled_X_test = epsb_scaler.transform(unscaled_X_test)

# ## Model
# Create the model
# Ran different rounds of the below model.  Some of the options I put in comments to the right.
input_size = 6 # Ran rounds using a multi-index of School Code & End Year.  But didn't get above a 78% validation accuracy
output_size = 3
hidden_layer_size = 15 # for this problem, optimal results were between 10-20 layers

model = tf.keras.Sequential([
    tf.keras.layers.Dense(hidden_layer_size, activation='tanh'),  # attempted to make this linear, and it only came to 77% valid accuracy or less
    tf.keras.layers.Dense(hidden_layer_size, activation='tanh'),
    tf.keras.layers.Dense(output_size, activation='softmax')
    ])
model.compile(optimizer=tf.keras.optimizers.legacy.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Fit the model
batch_size = 50  # started with batch size 25
max_epochs = 100 # started with 20 epochs
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

model.fit(scaled_X_train,
          y_train,
          batch_size=batch_size,
          epochs = max_epochs,
          callbacks = [early_stopping],
          validation_data = (scaled_X_valid, y_valid),
          verbose =0) # verbose=2 until final product. 

# Test the Classification model and print test accuracy
test_loss, test_accuracy = model.evaluate(scaled_X_test, y_test)
print('\nClassification Test loss: {0:.2f}. Classification Test accuracy: {1:.2f}%'.format(test_loss, test_accuracy*100.))

# Save model
# Test accuracy for the saved model is 97%
tf.keras.models.save_model(model, 'classification_model', include_optimizer=True)

## Fill in Classification predictions using model
# Grab the data that we want to predict
inputs = predict_df.loc[:, ['End Year Code', 'District Code', 'Level Code',
                            'Reported Spending per student', 'Money Difference per school', 'Proficiency Score', ]]

# Convert to np array and scale data
inputs = epsb_scaler.transform(inputs.values)

# Predict classification and convert to one column
pred_classification = model.predict(inputs).argmax(axis=1)

# Update the predict_df with the missing values in the Classification columns
predict_df['Classification Code'] = predict_df['Classification Code'].fillna(pd.Series(pred_classification))
predict_df['Classification'] = predict_df['Classification'].fillna(pd.Series(pred_classification)).replace([0, 1, 2], ['Needs Improvement', 'Proficient', 'Distinguished'])

## Predict Rating: a NN Model
# Shuffle, Split, Scale
nested_df = predict_df.loc[:,['End Year Code', 'Level Code',
                              'Reported Spending per student', 'Money Difference per school',
                              'Proficiency Score', 'Classification Code', 'Rating Code']].dropna()

#Shuffle data
nested_df = nested_df.sample(frac=1, random_state=7)
nested_df.reset_index(drop=True, inplace=True)

nested_inputs = nested_df.values[:,:-1]
nested_targets = nested_df.values[:,-1]

x_train, x_set, y_train, y_set = train_test_split(nested_inputs, nested_targets,
                                                  test_size=0.2, random_state=3, stratify = nested_targets)

x_valid, x_test, y_valid, y_test = train_test_split(x_set, y_set,
                                                    test_size=0.5, random_state=16, stratify = y_set)

# Scale data
nested_model_scaler = StandardScaler()

# Calculate and store the mean and sd
nested_model_scaler.fit(x_train)

# Apply the scaler
x_train_scaled = nested_model_scaler.transform(x_train)
x_valid_scaled = nested_model_scaler.transform(x_valid)
x_test_scaled = nested_model_scaler.transform(x_test)

nested_df = predict_df.loc[:,['End Year Code', #'District Code',
                              'Level Code',
                              'Reported Spending per student', 'Money Difference per school',
                              'Proficiency Score', 'Classification Code', 'Rating Code']].dropna()

#Shuffle data
nested_df = nested_df.sample(frac=1, random_state=7)
nested_df.reset_index(drop=True, inplace=True)

## Create the Rating model
# Ran different rounds of the below model.  Some of the options I put in comments to the right.
input_size = 6
output_size = 5
hidden_layer_size = 10 # also tried 20, 5, 15, 30
nested_model = tf.keras.Sequential([
    tf.keras.layers.Dense(hidden_layer_size, activation='PReLU'), # relu, elu, PReLU, LeakyReLU, swish     runnerup: swish, PReLU
    tf.keras.layers.Dense(hidden_layer_size, activation='elu'), # relu, elu, swish, PReLU, gelu, tanh      runnerup: elu, PReLU
    tf.keras.layers.Dense(output_size, activation='softmax')
    ])
# Create a custom learning rate
custom_learning_rate = 0.005 # 0.01, 0.005, 0.001

# Compile the model
nested_model.compile(optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=custom_learning_rate),
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])

# Fit the model
batch_size = 20  # 20, 50, 100, 30
max_epochs = 100
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
nested_model.fit(x_train_scaled, y_train,
          batch_size=batch_size,
          epochs = max_epochs,
          callbacks = [early_stopping],
          validation_data = (x_valid_scaled, y_valid),
          verbose = 0) # verbose=2 until final product. 

# Test the Nested Model and print test accuracy
nested_test_loss, nested_test_accuracy = nested_model.evaluate(x_test_scaled, y_test)
print('\nRating Test loss: {0:.2f}. Rating Test accuracy: {1:.2f}%'.format(nested_test_loss, nested_test_accuracy*100.))

# Save model. The test data accuracy for the saved model is 96%
tf.keras.models.save_model(nested_model, 'rating_model', include_optimizer=True)

# ## Nested Predict
nested_inputs = predict_df.loc[:,['End Year Code', 'Level Code',
                              'Reported Spending per student', 'Money Difference per school',
                              'Proficiency Score', 'Classification Code', ]]

# Apply the scaler
nested_inputs = nested_model_scaler.transform(nested_inputs.values)

# Predict Rating and convert to one column
predict_rating = nested_model.predict(nested_inputs).argmax(axis=1)

# Update the predict_df with the missing values in the Classification columns
predict_df['Rating Code'] = predict_df['Rating Code'].fillna(pd.Series(predict_rating))
predict_df['Rating'] = predict_df['Rating'].fillna(pd.Series(predict_rating)).replace([0,1,2,3,4], ['Very Low', 'Low', 'Medium', 'High', 'Very High'])

# # Export and Finish
predict_df.info()
predict_df.to_csv('predict_df.csv', index = False)
print("File4 Finished: predict_df.csv updated")