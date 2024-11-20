import os

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

import utils

sequences, labels = [], []
# WLASL dataset
# for gloss in os.listdir(os.path.join('images')):
#     for id in os.listdir(os.path.join('images', gloss)):
#         window = []
#         for frame_num in range(no_of_frames):
#             res = np.load(os.path.join('images', gloss, str(id), f'{frame_num}.npy'))
#             window.append(res)
#         if len(window) == no_of_frames:
#             sequences.append(window)
#             labels.append(label_map[gloss])

# custom dataset
for gloss in os.listdir(os.path.join('custom_images_data')):
    for id in os.listdir(os.path.join('custom_images_data', gloss)):
        window = []
        for frame_num in range(utils.no_of_frames):
            print(os.path.join('custom_images_data', gloss, str(id), f'{frame_num}.npy'))
            res = np.load(os.path.join('custom_images_data', gloss, str(id), f'{frame_num}.npy'))
            window.append(res)
        if len(window) == utils.no_of_frames:
            sequences.append(window)
            labels.append(utils.label_map[gloss])

X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

np_gloss = np.array(list(utils.label_map.keys()))

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(utils.no_of_frames, X.shape[2])))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(np_gloss.shape[0], activation='softmax'))

model.compile(optimizer="Adam", loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs=250, callbacks=[tb_callback])

model.save(f'{input("Enter the name of your model")}.h5')
