#!/usr/bin/env python3
"""
RealtimeSTT Wake Word Detection and Transcription Script - Simplified Version
Author: Assistant
Description: Detects wake words and performs real-time transcription with fallback options
"""

import logging
import time
import os
from RealtimeSTT import AudioToTextRecorder

# Configure comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('realtimestt_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WakeWordTranscriber:
    def __init__(self):
        self.is_transcribing = False
        self.wake_word_detected = False
        self.use_wake_words = True
        
    def print_separator(self, text=""):
        """Print a visual separator for better readability"""
        print("\n" + "="*60)
        if text:
            print(f"  {text}")
            print("="*60)
        
    def on_recording_start(self):
        """Callback when recording starts"""
        self.is_transcribing = True
        self.print_separator("RECORDING STARTED")
        logger.info("Recording started - listening for speech")
        
    def on_recording_stop(self):
        """Callback when recording stops"""
        self.is_transcribing = False
        self.print_separator("RECORDING STOPPED")
        logger.info("Recording stopped")
        
    def on_transcription_start(self):
        """Callback when transcription starts"""
        self.print_separator("TRANSCRIPTION STARTED")
        logger.info("Transcription process started")
        
    def on_realtime_transcription_update(self, text):
        """Callback for real-time transcription updates"""
        if text.strip():
            print(f"\rReal-time: {text}", end="", flush=True)
            logger.debug(f"Real-time update: {text}")
            
    def on_realtime_transcription_stabilized(self, text):
        """Callback for stabilized real-time transcription"""
        if text.strip():
            print(f"\nStabilized: {text}")
            logger.info(f"Stabilized transcription: {text}")
            
    def on_recorded_chunk(self, chunk):
        """Callback when audio chunk is recorded"""
        logger.debug(f"Audio chunk recorded: {len(chunk)} bytes")
        
    def on_vad_start(self):
        """Callback when voice activity starts"""
        print("Voice activity detected")
        logger.debug("Voice activity detection: START")
        
    def on_vad_stop(self):
        """Callback when voice activity stops"""
        print("Voice activity ended")
        logger.debug("Voice activity detection: STOP")
        
    def on_vad_detect_start(self):
        """Callback when VAD starts listening"""
        print("Started listening for voice activity")
        logger.debug("VAD detection started")
        
    def on_vad_detect_stop(self):
        """Callback when VAD stops listening"""
        print("Stopped listening for voice activity")
        logger.debug("VAD detection stopped")
        
    def on_wakeword_detected(self):
        """Callback when wake word is detected"""
        self.wake_word_detected = True
        self.print_separator("WAKE WORD DETECTED!")
        print("Wake word detected! Now listening for speech...")
        logger.info("Wake word detected - activating transcription")
        
    def on_wakeword_timeout(self):
        """Callback when wake word times out"""
        self.wake_word_detected = False
        self.print_separator("WAKE WORD TIMEOUT")
        print("No speech detected after wake word - going back to sleep...")
        logger.info("Wake word timeout - returning to idle state")
        
    def on_wakeword_detection_start(self):
        """Callback when wake word detection starts"""
        print("Started listening for wake words...")
        logger.info("Wake word detection started")
        
    def on_wakeword_detection_end(self):
        """Callback when wake word detection ends"""
        print("Stopped listening for wake words")
        logger.info("Wake word detection ended")
        
    def get_base_config(self):
        """Get base configuration without wake words"""
        return {
            # Model Configuration
            "model": "small.en",
            "language": "en",
            "compute_type": "float32",
            "device": "cpu",
            "input_device_index": 3,
            "spinner": False,
            
            # Debug and Logging
            "debug_mode": True,
            "level": logging.DEBUG,
            "print_transcription_time": True,
            
            # Real-time Transcription Settings
            "enable_realtime_transcription": True,
            "use_main_model_for_realtime": False,
            "realtime_model_type": "tiny",
            "realtime_processing_pause": 0.1,
            "realtime_batch_size": 8,
            "beam_size_realtime": 3,
            
            # Voice Activity Detection
            "silero_sensitivity": 0.6,
            "silero_use_onnx": True,
            "silero_deactivity_detection": True,
            "webrtc_sensitivity": 2,
            "post_speech_silence_duration": 2.0,
            "min_gap_between_recordings": 0.5,
            "min_length_of_recording": 0.5,
            "pre_recording_buffer_duration": 0.3,
            
            # Audio Processing
            "use_microphone": True,
            "handle_buffer_overflow": True,
            "allowed_latency_limit": 50,
            
            # Text Processing
            "ensure_sentence_starting_uppercase": True,
            "ensure_sentence_ends_with_period": True,
            "batch_size": 16,
            "beam_size": 5,
            "suppress_tokens": [-1],
            
            # Performance
            "early_transcription_on_silence": 500,
            "start_callback_in_new_thread": False,
            
            # Callback Functions
            "on_recording_start": self.on_recording_start,
            "on_recording_stop": self.on_recording_stop,
            "on_transcription_start": self.on_transcription_start,
            "on_realtime_transcription_update": self.on_realtime_transcription_update,
            "on_realtime_transcription_stabilized": self.on_realtime_transcription_stabilized,
            "on_recorded_chunk": self.on_recorded_chunk,
            "on_vad_start": self.on_vad_start,
            "on_vad_stop": self.on_vad_stop,
            "on_vad_detect_start": self.on_vad_detect_start,
            "on_vad_detect_stop": self.on_vad_detect_stop,
        }
        
    def get_porcupine_config(self):
        """Get configuration with Porcupine wake words"""
        config = self.get_base_config()
        config.update({
            # Porcupine Wake Word Configuration
            "wakeword_backend": "pvporcupine",
            "wake_words": "jarvis,computer",  # Using built-in wake words
            "wake_words_sensitivity": 0.6,
            "wake_word_activation_delay": 0,
            "wake_word_timeout": 10.0,
            "wake_word_buffer_duration": 1.0,
            
            # Wake word callbacks
            "on_wakeword_detected": self.on_wakeword_detected,
            "on_wakeword_timeout": self.on_wakeword_timeout,
            "on_wakeword_detection_start": self.on_wakeword_detection_start,
            "on_wakeword_detection_end": self.on_wakeword_detection_end,
        })
        return config
        
    def get_oww_config(self):
        """Get configuration with OpenWakeWord"""
        config = self.get_base_config()
        config.update({
            # OpenWakeWord Configuration
            "wakeword_backend": "oww",
            "openwakeword_model_paths": "hey_kaba.onnx,okay_kaaba.onnx",
            "openwakeword_inference_framework": "onnx",
            "wake_words_sensitivity": 0.35,
            "wake_word_activation_delay": 0,
            "wake_word_timeout": 10.0,
            "wake_word_buffer_duration": 1.0,
            
            # Wake word callbacks
            "on_wakeword_detected": self.on_wakeword_detected,
            "on_wakeword_timeout": self.on_wakeword_timeout,
            "on_wakeword_detection_start": self.on_wakeword_detection_start,
            "on_wakeword_detection_end": self.on_wakeword_detection_end,
        })
        return config
        
    def check_dependencies(self):
        """Check for required dependencies"""
        try:
            import openwakeword
            logger.info("OpenWakeWord found")
            return True
        except ImportError:
            logger.warning("OpenWakeWord not found, will try Porcupine")
            return False
            
    def check_model_files(self):
        """Check if wake word model files exist"""
        model_files = ["hey_kaba.onnx", "okay_kaaba.onnx"]
        missing_files = []
        
        for model_file in model_files:
            if not os.path.exists(model_file):
                missing_files.append(model_file)
                
        if missing_files:
            logger.error(f"Missing wake word model files: {missing_files}")
            print(f"Missing wake word model files: {missing_files}")
            return False
        else:
            logger.info(f"Wake word models found: {model_files}")
            print(f"Wake word models found: {model_files}")
            return True
            
    def try_initialize_recorder(self, config, config_name):
        """Try to initialize recorder with given configuration"""
        try:
            logger.info(f"Trying to initialize recorder with {config_name}")
            print(f"Attempting initialization with {config_name}...")
            
            recorder = AudioToTextRecorder(**config)
            logger.info(f"Successfully initialized with {config_name}")
            print(f"Successfully initialized with {config_name}")
            return recorder
            
        except Exception as e:
            logger.error(f"Failed to initialize with {config_name}: {e}")
            print(f"Failed to initialize with {config_name}: {e}")
            return None
            
    def start_listening(self):
        """Start the wake word detection and transcription loop"""
        self.print_separator("INITIALIZING REALTIMESTT")
        print("Initializing RealtimeSTT with multiple fallback options...")
        print("Model: small.en")
        print("Device: CPU")
        print("Input device index: 3")
        
        recorder = None
        
        # Try different configurations in order of preference
        
        # 1. Try OpenWakeWord with custom models
        if self.check_model_files() and self.check_dependencies():
            print("\nTrying OpenWakeWord with custom models...")
            recorder = self.try_initialize_recorder(self.get_oww_config(), "OpenWakeWord (custom models)")
            if recorder:
                print("Wake words: 'hey kaba', 'okay kaaba'")
                print("Sensitivity: 0.35")
        
        # 2. Try Porcupine with built-in wake words
        if not recorder:
            print("\nTrying Porcupine with built-in wake words...")
            recorder = self.try_initialize_recorder(self.get_porcupine_config(), "Porcupine (built-in)")
            if recorder:
                print("Wake words: 'jarvis', 'computer'")
                print("Sensitivity: 0.6")
        
        # 3. Fall back to no wake words
        if not recorder:
            print("\nFalling back to voice activity detection only...")
            recorder = self.try_initialize_recorder(self.get_base_config(), "Voice Activity Detection only")
            self.use_wake_words = False
            if recorder:
                print("Mode: Voice activity detection")
                print("No wake words - will start transcribing on voice detection")
        
        if not recorder:
            print("Failed to initialize recorder with any configuration")
            return
            
        self.recorder = recorder
        
        try:
            self.print_separator("SYSTEM READY")
            print("System initialized successfully!")
            
            if self.use_wake_words:
                print("Listening for wake words...")
                print("Press Ctrl+C to exit")
            else:
                print("Listening for speech (no wake words)...")
                print("Press Ctrl+C to exit")
            
            # Main listening loop
            while True:
                try:
                    # Get transcription
                    text = self.recorder.text()
                    
                    if text and text.strip():
                        self.print_separator("FINAL TRANSCRIPTION")
                        print(f"Final text: {text}")
                        logger.info(f"Final transcription: {text}")
                        
                        if self.use_wake_words:
                            print("\nListening for wake words again...")
                        else:
                            print("\nListening for more speech...")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Error during transcription: {e}")
                    print(f"Error during transcription: {e}")
                    time.sleep(1)  # Brief pause before retrying
                    
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"Error in main loop: {e}")
            
    def shutdown(self):
        """Clean shutdown of the recorder"""
        if hasattr(self, 'recorder') and self.recorder:
            self.print_separator("SHUTTING DOWN")
            print("Shutting down recorder...")
            try:
                self.recorder.shutdown()
                logger.info("Recorder shutdown completed")
                print("Shutdown completed successfully")
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
                print(f"Error during shutdown: {e}")

def main():
    """Main function to run the wake word transcriber"""
    transcriber = WakeWordTranscriber()
    
    try:
        transcriber.start_listening()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"Unexpected error: {e}")
    finally:
        transcriber.shutdown()
        print("Goodbye!")

if __name__ == "__main__":
    main()