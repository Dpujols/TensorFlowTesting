import tensorflow as tf
import tensorflow_hub as hub


def LoadModel(UseVideo):  # MType Determines model used
    if UseVideo:
        AI = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
        print("Video Model Loaded")
        return AI
    else:
        AI = hub.load("https://tfhub.dev/tensorflow/faster_rcnn/resnet152_v1_1024x1024/1")
        print("Image Model Loaded")
        return AI


def PrepareImage(Image):
    Tensor = tf.expand_dims(tf.convert_to_tensor(Image, dtype=tf.uint8), 0)
    return Tensor


def IntializeDetection(Image, Model):
    Tensor = PrepareImage(Image)
    DetectedImages = Model(Tensor)

    return DetectedImages
