#To rrun the node

ros2 run your_package text_to_speech_node

#To publish the  string

ros2 topic pub /speech_text std_msgs/String "{data: 'AGV is going from one to Eleven'}"

#To  set the language and file name parameter

ros2 param set /text_to_speech_node language 'es'  # For Spanish
ros2 param set /text_to_speech_node audio_filename 'new_audio.mp3'



