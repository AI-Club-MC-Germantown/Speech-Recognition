from vosk import Model, KaldiRecognizer
import pyaudio
import json

'''
 	a recognizer in vosk terms is the functionality responsible for interpreting the audio into speech.
  	Here a recognizer is being initialized with a model path and the sample rate of the audio to interpret (in Hertz) in this case it's 16 kHz
    -The first parameter is the directory path within either the project or general computer that leads to your model
   	NOTE:
    		-The sample rate must be the same as the sample rate of audio otherwise it may lead to issues in transcription accuracy
      		-Vosk models run best at 16 kHz though other samples rate will be adjusted automatically by vosk
		    -Vosk models other than sampling require audio to be inputted with the following configuration:
  			    -Mono Channel or 1 channel
     			-Audio format must be in PCM form (often as .WAV or .RAW)
			-Vosk is typically used with 16-bit audio, but it can handle other bit depths if the audio is correctly interpreted and resampled. 
   	You will see this note reflected when initializing the microphone
'''
recognizer = KaldiRecognizer(Model(r'C:\Users\user\Downloads\simple_vosk\simple_vosk_virtual_enviornment\vosk-model-small-en-us-0.15'), 16000)

'''
 	Pyaudio is a python wrapper for the open source I/O library, PortAudio
  	A stream is an object that encapsulates PyAudio's functionality, it can be used for various things however here we just use it to read audio
   	This stream automatically connects to the first known audio device on system, if needed set parameter "input_device_index = #"
    	pyaudio.paInt16 - sets bit depth of audio to 16 bits
     	channel = 1 - sets mono audio
      	rate - the sample rate of the audio (MUST BE THE SAME VALUE AS SET IN RECOGNIZER)
        input - boolean that sets whether or not the stream will listen through mic
	frames_per_buffer - The number of frames per buffer. This controls how many audio samples are processed at a time. 
 		Smaller buffer sizes reduce latency but increase CPU usage.
'''
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

'''
	initiate stream state of listening through mic.
''' 
stream.start_stream()

print("Say exit when you want to terminate the program... \n")

#infinite loop that terminates when the word 'exit' is spoken 
while True:
    '''
    This program reads audio in segments at a time 
    here the raw audio is being held 4096 bytes at a time
    '''
    data = stream.read(4096)

    '''
    acceptWaveform processes the given audio buffer and checks if it contains 
    enough data for a complete speech segment. 
 
    -Returns true: if the current audio buffer contains a full segment that 
    can be recognized (i.e., a complete phrase or sentence). The result() 
    function should then be called to get the recognized text.
 
    -Returns false: if the audio buffer is incomplete, indicating that more 
    audio is needed for a full recognition. In this case, partial_result() 
    can be called to get an interim (partial) transcription until more audio is provided
    '''
    if recognizer.AcceptWaveform(data) == True:

        #result is the captured-text raw sample read from before
        result = recognizer.Result()

        #result dict then takes result and takes out the json formatting of the raw text output and assign it to a single key dictionary
        #formatted Ex. {"text": #####}
        result_dict = json.loads(result)

        #extracts actual text from dictionary format
        text = result_dict.get("text", "")
        print(text)

        #if 'exit' is found within a lowercase version of the text output, then while loop terminates
        if "exit" in text.lower():
            print("Exiting...")
            break

stream.stop_stream()
stream.close()
