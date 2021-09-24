import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten, Concatenate
from tensorflow.keras.layers import BatchNormalization, Conv2DTranspose, add, Activation, Dropout
#from tensorflow.keras.layers import add, Input
import visualkeras
#from visualkeras_.layered import layered_view
from PIL import ImageFont
font = ImageFont.truetype("arial.ttf", 24*2)  # using comic sans is strictly prohibited!

from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, ZeroPadding2D, UpSampling2D, InputLayer, BatchNormalization, ReLU, DepthwiseConv2D, Add, Activation, Conv2DTranspose, Concatenate, Input
from collections import defaultdict

color_map = defaultdict(dict)
color_map[Conv2D]['fill'] = 'lightskyblue'
color_map[ZeroPadding2D]['fill'] = 'gray'
color_map[Dropout]['fill'] = 'lightgray'
color_map[MaxPooling2D]['fill'] = 'darkred'
color_map[Dense]['fill'] = 'coral'
color_map[Flatten]['fill'] = 'darkorange'
color_map[UpSampling2D]['fill'] = 'olive'
color_map[InputLayer]['fill'] = 'black'
color_map[BatchNormalization]['fill'] = 'teal'
color_map[ReLU]['fill'] = 'green'
color_map[DepthwiseConv2D]['fill'] = 'darkseagreen'
color_map[Add]['fill'] = 'crimson'
color_map[Activation]['fill'] = 'navy'
color_map[Conv2DTranspose]['fill'] = 'indigo'
color_map[Concatenate]['fill'] = 'cornsik'


model_type = "advanced_decoder2" # "vgg", mobilenetv2", "resnet", "simple_decoder", "unet", "advanced_decoder"

if model_type == "vgg":
    encoder = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet', input_shape=(256,256,3), classifier_activation=None)
    model = Model(inputs=encoder.inputs, outputs=encoder.output)
    font = ImageFont.truetype("arial.ttf", 24*2)  # using comic sans is strictly prohibited!
    visualkeras.layered_view(model, legend=True, font=font, scale_xy=3, to_file="plots/models/mobilenet_v2.png", scale_z=0.0001, max_z=0.1).show()
    visualkeras.layered_view(model, legend=True, font=font, scale_xy=3, to_file="plots/models/mobilenet_v2.png", scale_z=0.0001, max_z=0.1, color_map=color_map).show()
elif model_type == "resnet":
    encoder = tf.keras.applications.ResNet50V2(include_top=False, weights="imagenet", input_tensor=None, input_shape=(256,256,3), pooling=None, classifier_activation= None)
    model = Model(inputs=encoder.inputs, outputs=encoder.output)
    font = ImageFont.truetype("arial.ttf", 24*2)  # using comic sans is strictly prohibited
    visualkeras.layered_view(model, legend=True, font=font, scale_xy=3, to_file="plots/models/resnet.png", scale_z=0.0001, max_z=0.1).show()
    visualkeras.layered_view(model, legend=True, font=font, scale_xy=3, to_file="plots/models/resnet.png", scale_z=0.0001, max_z=0.1, color_map=color_map).show()
elif model_type == "simple_decoder":
    x = Input((256,256,3))
    d1 = UpSampling2D(size=(2, 2))(x)
    c1 = Conv2D(8, kernel_size=(3, 3), activation='selu', padding='same')(d1)
    d2 = UpSampling2D(size=(2, 2))(c1)
    c2 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d2)
    d3 = UpSampling2D(size=(2, 2))(c2)
    c3 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d3)
    d4 = UpSampling2D(size=(2, 2))(c3)
    c4 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d4)
    d5 = UpSampling2D(size=(2, 2))(c4)
    c5 = Conv2D(1, kernel_size=(1, 1), activation='sigmoid', padding='same')(d5)
    output = c5
    model = Model(inputs=x, outputs=output)
    font = ImageFont.truetype("arial.ttf", 24*3)  # using comic sans is strictly prohibited!
    visualkeras.layered_view(model, legend=True, font=font, scale_xy = 0.1, to_file="plots/models/simple_decoder.png", scale_z = 10, index_ignore=[0]).show()
    visualkeras.layered_view(model, legend=True, font=font, scale_xy = 0.1, to_file="plots/models/simple_decoder.png", scale_z = 10, index_ignore=[0], color_map=color_map).show()
elif model_type == "unet":
    model = tf.keras.models.load_model("results/julian/unet_4/model.tf")
    font = ImageFont.truetype("arial.ttf", 24)  # using comic sans is strictly prohibited!
    visualkeras.layered_view(model, legend=True, scale_xy = 1, font=font, to_file="plots/models/unet.png").show()
    visualkeras.layered_view(model, legend=True, scale_xy = 1, font=font, to_file="plots/models/unet.png", color_map=color_map).show()
elif model_type == "advanced_decoder":
    x = Input((256,256,3))
    
    base = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(x)
    t1 = Conv2DTranspose(16, (3, 3), activation="selu", padding="same")(base)
    b12 = BatchNormalization()(t1)
    act11 = Activation("selu")(b12)
    dUp1 = UpSampling2D(size=(2, 2))(act11)
    d1 = UpSampling2D(size=(2, 2))(act11)
    c1 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d1)
    plus1 = add([c1,dUp1])
    b12 = BatchNormalization()(plus1)
    act12 = Activation("selu")(b12)
    drop1 = Dropout(0.3)(act12)

    t2 = Conv2DTranspose(16,(3, 3),activation="selu", padding="same")(drop1)
    b22 = BatchNormalization()(t2)
    act21 = Activation("selu")(b22)
    dUp2 = UpSampling2D(size=(2, 2))(act21)
    d2 = UpSampling2D(size=(2, 2))(act21)
    c2 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d2)
    plus2 = add([c2,dUp2])
    b22 = BatchNormalization()(plus2)
    act22 = Activation("selu")(b22)
    drop2 = Dropout(0.3)(act22)

    t3 = Conv2DTranspose(16, (3, 3), activation="selu", padding="same")(drop2)
    b32 = BatchNormalization()(t3)
    act31 = Activation("selu")(b32)
    dUp3 = UpSampling2D(size=(2, 2))(act31)
    d3 = UpSampling2D(size=(2, 2))(act31)
    c3 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d3)
    plus3 = add([c3,dUp3])
    b32 = BatchNormalization()(plus3)
    act32 = Activation("selu")(b32)
    drop3 = Dropout(0.3)(act32)
   
    t4 = Conv2DTranspose(16, (3, 3), activation="selu", padding="same")(drop3)
    b42 = BatchNormalization()(t4)
    act41 = Activation("selu")(b42)
    dUp4 = UpSampling2D(size=(2, 2))(act41)
    d4 = UpSampling2D(size=(2, 2))(act41)
    c4 = Conv2D(16, kernel_size=(3, 3), activation='selu', padding='same')(d4)
    plus4 = add([c4,dUp4])
    b42 = BatchNormalization()(plus4)
    act42 = Activation("selu")(b42)
    drop4 = Dropout(0.3)(act42)

    d5 = Conv2DTranspose(256, (3, 3), strides=2, activation="selu", padding="same")(drop4)
    #c5 = Conv2D(1, kernel_size=(1, 1), activation='sigmoid', padding='same')(d5)
    c5 = Conv2D(3, kernel_size=(1, 1), activation='softmax', padding='same')(d5)
    output = c5
    model = Model(inputs=x, outputs=output)
    font = ImageFont.truetype("arial.ttf", 24)  # using comic sans is strictly prohibited!
    visualkeras.layered_view(model, legend=True, font=font, scale_xy = 0.1, to_file="plots/models/advanced_decoder.png", scale_z=0.0001, max_z=0.1, index_ignore=[0]).show()
    visualkeras.layered_view(model, legend=True, font=font, scale_xy = 0.07, to_file="plots/models/advanced_decoder.png", scale_z=0.01, max_z=0.1, index_ignore=[0], color_map=color_map).show()
elif model_type == "segnet":
    x = Input((256,256,3))
    conv_1 = Conv2D(32, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(x)
    conv_1 = BatchNormalization()(conv_1)
    conv_1 = Activation("relu")(conv_1)
    pool_1 = MaxPooling2D()(conv_1)
    conv_2 = Conv2D(64, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(pool_1)
    conv_2 = BatchNormalization()(conv_2)
    conv_2 = Activation("relu")(conv_2)
    pool_2 = MaxPooling2D()(conv_2)
    conv_3 = Conv2D(64, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(pool_2)
    conv_3 = BatchNormalization()(conv_3)
    conv_3 = Activation("relu")(conv_3)
    pool_3 = MaxPooling2D()(conv_3)
    conv_4 = Conv2D(128, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(pool_3)
    conv_4 = BatchNormalization()(conv_4)
    conv_4 = Activation("relu")(conv_4)
    pool_4 = MaxPooling2D()(conv_4)
    unpool_1 = Conv2DTranspose(64,kernel_size=(2, 2), strides=(2,2))(pool_4)
    conv_5 = Conv2D(64, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(unpool_1)
    conv_5 = BatchNormalization()(conv_5)
    conv_5 = Activation("relu")(conv_5)
    unpool_2 = Conv2DTranspose(64, kernel_size=(2, 2), strides=(2,2))(conv_5)
    conv_6 = Conv2D(64, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(unpool_2)
    conv_6 = BatchNormalization()(conv_6)
    conv_6 = Activation("relu")(conv_6)
    unpool_3 = Conv2DTranspose(32, kernel_size=(2, 2), strides=(2,2))(conv_6)
    conv_7 = Conv2D(32, kernel_size=(3, 3), padding="same", kernel_initializer='he_normal')(unpool_3)
    conv_7 = BatchNormalization()(conv_7)
    conv_7 = Activation("relu")(conv_7)
    unpool_4 = Conv2DTranspose(3, kernel_size=(2, 2), strides=(2,2))(conv_7)
    conv_8 = Conv2D(3, kernel_size=(1, 1), padding="same", kernel_initializer='he_normal')(unpool_4)
    conv_8 = BatchNormalization()(conv_8)
    outputs = Activation("softmax")(conv_8)
    model = Model(inputs=x, outputs=outputs)
    font = ImageFont.truetype("arial.ttf", 24)  # using comic sans is strictly prohibited!

    layered_view(model, legend=True, font=font, scale_xy = 1, to_file="plots/models/segnet.png", scale_z = 0.01).show()
    layered_view(model, legend=True, font=font, scale_xy = 1, to_file="plots/models/segnet.png", scale_z = 0.01, color_map=color_map).show()
elif model_type == "advanced_decoder2":
    inp = Input((256,256,3))
    x = inp
    f = [16,32,64,128,256]
    d = [16,16,32,48,64]
    ####### Layer i #######
    for i in range(len(f)):
        dUp = UpSampling2D(size=(2, 2))(x)
        dUp = Conv2D(d[-i], kernel_size=(3, 3),activation='selu',padding='same')(dUp)
        dUp = BatchNormalization()(dUp)
        dUp = Activation("selu")(dUp)

        x = Conv2DTranspose(f[i], (3, 3), strides=2, activation="selu", padding="same")(x)
        x = Conv2D(d[-i], kernel_size=(3, 3),activation='selu',padding='same')(x)
        x = Conv2D(d[-i], kernel_size=(3, 3),activation='selu',padding='same')(x)
        x = BatchNormalization()(x)

        x = add([x,dUp])
        x = Activation("selu")(x)
        x = Dropout(0.3)(x)
        
    
    c5 = Conv2D(3, kernel_size=(1, 1), activation='softmax', padding='same')(x)
    output =c5
    model = Model(inputs=inp, outputs=output)
    font = ImageFont.truetype("arial.ttf", 24)  # using comic sans is strictly prohibited!
    visualkeras.layered_view(model, legend=True, font=font, scale_xy = 0.1, to_file="plots/models/advanced_decoder2.png", scale_z=0.0001, max_z=0.1, index_ignore=[0]).show()
    visualkeras.layered_view(model, legend=True, font=font, scale_xy = 0.07, to_file="plots/models/advanced_decoder2.png", scale_z=0.01, max_z=0.1, index_ignore=[0], color_map=color_map).show()