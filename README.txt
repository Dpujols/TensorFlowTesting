How to begin?

Install Dependencies:
  TensorFlow (PLEASE DO THIS FIRST):
    - Follow this guide, it includes steps in installing Python, PIP, and the various versions of tensorflow:
      https://www.tensorflow.org/install/pip
    - The version ive tested on is the CPU install, but the GPU version will provide faster detection and better performance.
  FLASK - pip install flask
  OpenCV - pip install OpenCV


Configure IP:
  1. By default the server assumes it will use port 8000. Find your machines local IP and adjust line 10 in main.py to it. If you
  do not know your local IP run the server and check the Flask Logs, it will give you the IP the server is running on, once youve   
  adjusted it flask will automatically rerun.


Optionally Customize Models:
  
  1. You can find new models here: https://tfhub.dev/tensorflow/collections/object_detection/1
  
  2. Simply copy the url and replace the url for the model in ImageProcessor.py (line 7 for video and line 11 for image), for image 
    detection you can use any model youd like - for video detection take note that slower models may be more accurate but they will 
    introduce video latency.
  
  3. After choosing a model please take note of the resolution for the model and adjust the resolution adjustment lines in        
    ImageHandler.py. For video models adjust line 15 for the RGB_RESIZE variable, for images adjust line 46 for the IMG_RESIZE
    variable 
  
  4. Some models may have different structures for their outputs, this was built around the CENTERNET system - any models under 
    there should be functional
