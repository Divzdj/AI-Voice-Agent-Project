import pyttsx3  

engine = pyttsx3.init()  
engine.save_to_file("Hello, this is a test audio file.", "sample.wav")  
engine.runAndWait()  

print("Audio file saved as sample.wav")
