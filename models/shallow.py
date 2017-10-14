from keras.layers import Input, Dense, Dropout, Flatten, merge, Reshape
from keras.layers import Convolution2D, MaxPooling2D
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from util import categorical_accuracy_per_sequence
from keras import backend as K
K.set_image_dim_ordering('th')


def build_shallow(channels, width, height, nb_classes):
	# input
	inputs = Input(shape=(channels, height, width))
	# 1 conv
	conv1_1 = Convolution2D(48, 5, 5, border_mode='same', activation='relu')(inputs)
	bn1 = BatchNormalization(mode=0, axis=1)(conv1_1)
	pool1 = MaxPooling2D(pool_size=(2,2), strides=(2,2))(bn1)
	drop1 = Dropout(0.5)(pool1)
	# 2 conv
	conv2_1 = Convolution2D(64, 5, 5, border_mode='same', activation='relu')(drop1)
	bn2 = BatchNormalization(mode=0, axis=1)(conv2_1)
	pool2 = MaxPooling2D(pool_size=(2,2), strides=(2,2))(bn2)
	drop2 = Dropout(0.5)(pool2)
	# 3 conv
	conv3_1 = Convolution2D(128, 5, 5, border_mode='same', activation='relu')(drop2)
	bn3 = BatchNormalization(mode=0, axis=1)(conv3_1)
	pool3 = MaxPooling2D(pool_size=(2,2), strides=(2,2))(bn3)
	drop3 = Dropout(0.5)(pool3)
	# 4 conv
	conv4_1 = Convolution2D(160, 5, 5, border_mode='same', activation='relu')(drop3)
	bn4 = BatchNormalization(mode=0, axis=1)(conv4_1)
	pool4 = MaxPooling2D(pool_size=(2,2), strides=(2,2))(bn4)
	drop4 = Dropout(0.5)(pool4)
	# 5 conv
	conv5_1 = Convolution2D(192, 5, 5, border_mode='same', activation='relu')(drop4)
	bn5 = BatchNormalization(mode=0, axis=1)(conv5_1)
	pool5 = MaxPooling2D(pool_size=(2,2), strides=(2,2))(bn5)
	drop5 = Dropout(0.5)(pool5)
	# flaten
	flat = Flatten()(drop5)
	# 1 dense
	dense1 = Dense(2048, activation='relu')(flat)
	bn6 = BatchNormalization(mode=0, axis=1)(dense1)
	drop6 = Dropout(0.5)(bn6)
	# output
	out = []
	out.append(Dense(nb_classes, activation='softmax')(drop6))

	sample_weight_mode = None
	metrics = ['accuracy']
	model = Model(input=[inputs], output=out)
	model.summary()#print model 
	model.compile(loss='categorical_crossentropy',
				  optimizer='adam',
				  metrics=metrics,
				  sample_weight_mode = sample_weight_mode
				  )

	return model