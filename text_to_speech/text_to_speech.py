#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gtts import gTTS
import os
from std_msgs.msg import String

class TextToSpeechNode(Node):
    def __init__(self):
        super().__init__('text_to_speech_node')
        self.get_logger().info("Text to Speech node has started.")
        
        # Subscriber for receiving text messages
        self.subscription = self.create_subscription(
            String,            # Message type (std_msgs/String)
            'speech_text',     # Topic name
            self.speech_callback, # Callback function when a message is received
            10                 # Queue size
        )
        self.subscription  # Prevent unused variable warning
        
        # Declare and read parameters (language and filename)
        self.declare_parameter('language', 'en')   # default language is 'en'
        self.declare_parameter('audio_filename', 'converted.mp3') # default filename
        
    def speech_callback(self, msg):
        # Get parameters (language and filename)
        language = self.get_parameter('language').value
        audio_filename = self.get_parameter('audio_filename').value
        
        # Received text from the topic
        mytext = msg.data
        self.get_logger().info(f"Received text for TTS: {mytext}")

        try:
            # Convert text to speech using gTTS
            tts = gTTS(text=mytext, lang=language, slow=False)
            
            # Save the converted audio
            tts.save(audio_filename)
            
            self.get_logger().info(f"Audio saved as {audio_filename}")

            # Play the converted file (Linux command 'mpg123' or 'start' for Windows)
            if os.name == 'posix':  # Linux/MacOS
                os.system(f"mpg123 {audio_filename}")
            elif os.name == 'nt':  # Windows
                os.system(f"start {audio_filename}")
                
            self.get_logger().info("Playing the audio...")
        
        except Exception as e:
            self.get_logger().error(f"Error in TTS conversion: {e}")

def main(args=None):
    rclpy.init(args=args)
    
    # Create the Text to Speech Node
    tts_node = TextToSpeechNode()
    
    try:
        # Keep the node running until it is shut down
        rclpy.spin(tts_node)
    except KeyboardInterrupt:
        tts_node.get_logger().info('Keyboard interrupt, shutting down.')
    finally:
        # Clean up
        tts_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

