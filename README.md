# FIRST-MLWorkshop - Neil Deshmukh
This is the workshop github for the 'Using Machine Learning to Build an Image Classification App' by Neil Deshmukh at FIRST Detroit on April 26th at 1:30 - 3:30 pm.

In this workshop, we will first train a ML algorithm to classify between any image classes that we give it, and then secondly integrate it into an application. 

The app integration is optional, but it's a pretty cool direct visualization of the Neural Network in action.

All that you need is: 
 * an internet connection (to download the needed materials)
 * (optional) the development environment for your respective phone:
   * Xcode for IOS (only on Mac)
   * Android Studio for Android 
   * Cord to connect the phone and computer

______________________________________________________________________________________________________________________________


## Step #0: Setup 

Download Python (if you don't already have it)

ONLY Mac Users Developing for IOS: 

python2: `sudo pip install --upgrade \
 https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.4.0-py-none-any.whl`

python 3: `sudo pip3 install --upgrade \
 https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.4.0-py3-none-any.whl`
 
Download tensorflow following the instructions at https://www.tensorflow.org/install/ (the CPU version will be sufficient for this workshop)

Download google_images_download, if you would like to train the model on the classes that you want it to detect:

`pip install google_images_download`

______________________________________________________________________________________________________________________________


# Part 1: Developing ML Classification Algorithm:

## 1. Clone this directory onto your computer: 

`git clone https://github.com/QuantumTCode/FIRST-MLWorkshop`



## 2. cd into the directory, where all of the code will be run:

`cd FIRST-MLWorkshop`



## 3. Download the classes of images that you would like the algorithm to detect:

`googleimagesdownload -f jpg -k "[Class 1], [Class 2], [Class 3], [Class 4], [Class 5]" `

So an example would be:

`googleimagesdownload -f jpg -k "train, car, bus, racecar, motorcycle"`

While only 5 classes are downloaded above, you can add more (might decrease accuracy of classification)

Check the images: 

`python scripts/check_images.py`



## 4. Set up variables for training:

`ARCHITECTURE="mobilenet_0.50_224"`

`tensorboard --logdir tf_files/training_summaries &`

If you receive an error stating: `TensorBoard attempted to bind to port 6006, but it was already in use` kill the existing TensorBoard instance using `pkill -f "tensorboard"`


## 5. Time to Initiate Machine Learning!

Start the training of the model using:

```python
python -m scripts.retrain \
  --bottleneck_dir=tf_files/bottlenecks \
  --how_many_training_steps=1000 \
  --model_dir=tf_files/models/ \
  --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}" \
  --output_graph=tf_files/retrained_graph.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=downloads
  
  ```
  
If you have time, and want to increase the accuracy of you model, change `--how_many_training_steps=X` to a higher number (4000 is probably the highest you need to go).


## 6. Watch Machine Learning in Action:

To see the real time learning behind the algorithm, go to http://0.0.0.0:6006/ on your computer!

## 7. Test the Accuracy of Your Algorithm:
```python
python -m scripts.label_image \
    --graph=tf_files/retrained_graph.pb  \
    --image=(path_to_image) 
   ```
    
For example:

`python -m scripts.label_image \
    --graph=tf_files/retrained_graph.pb  \
    --image=downloads/car/car.png`
  
______________________________________________________________________________________________________________________________

# Part 2: Implementing ML Algorithm on Phone:

## 1. Setup:

`pip install PILLOW`

If IOS: `sudo gem install cocoapods`

## 2: Optimize model using TensorFlow Lite Optimizing Converter (TOCO):
```python
toco \
  --input_file=tf_files/retrained_graph.pb \
  --output_file=tf_files/optimized_graph.pb \
  --input_format=TENSORFLOW_GRAPHDEF \
  --output_format=TENSORFLOW_GRAPHDEF \
  --input_shape=1,224,224,3 \
  --input_array=input \
  --output_array=final_result \
  --mean_value=128 \
  --std_value=128 \
  --default_range_min=0  \
  --default_ranges_max=6
  ```

## 3: Convert Model to TFLite Format:

```python 
toco \
  --input_file=tf_files/retrained_graph.pb \
  --output_file=tf_files/optimized_graph.lite \
  --input_format=TENSORFLOW_GRAPHDEF \
  --output_format=TFLITE \
  --input_shape=1,224,224,3 \
  --input_array=input \
  --output_array=final_result \
  --inference_type=FLOAT \
  --input_type=FLOAT \
  --mean_value=128 \
  --std_value=128 \
  --default_range_min=0  \
  --default_ranges_max=6
  ```
___________________________
## 4.1: For IOS:
`cd ios/camera`

Update Pods:
`pod update`

Copy the trained models into the app:
`cd ../..`
`cp tf_files/retrained_graph.pb ios/camera/data/retrained_graph.pb`

Copy the labels into the app:
`cp tf_files/retrained_labels.txt ios/camera/data/retrained_labels.txt`
Open the app:
`open ios/camera/tf_camera_example.xcworkspace`

Make sure to go to Xcode>Preferences and sign in to be able to connect your phone and test the application.

  *  Click on the tflite_photos_example file on the left, and name your Bundle Identifier something unique, for example: com.[your name]
  * Click on automatically manage signing
  
Finally, you should be able to run your app!

___________________________
## 4.2: For Android:
Set up Device: https://developer.android.com/studio/debug/dev-options#enable

Copy the labels and models into the app:
`cp tf_files/optimized_graph.lite android/tflite/app/src/main/assets/graph.lite`
`cp tf_files/retrained_labels.txt android/tflite/app/src/main/assets/labels.txt`

Open Android Studio>Open an existing Android Studio project, open FIRST-MLWorkshop/android/tflite, and click 'OK' for Gradle Sync.

Then run the app!
