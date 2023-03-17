import pyaudio, json, pyttsx3
from vosk import Model, KaldiRecognizer
from files.order import Order
from files.checks import Check
import pyttsx3
import time

with open("files\system_files\\remind.txt", "w", encoding="utf-8") as remind:
    remind.write("")

engine = pyttsx3.init()
engine.setProperty('voice', r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Natalia")
engine.setProperty("rate", 150)

def say_text(text):
    engine.say(text)
    engine.runAndWait()

model = Model("files/model1")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

say_text("З поверненням")
try:
    stream.start_stream()
except OSError:
    print("Ви не підключили мікрофон")

def listen():
    while True:
        with open("files\system_files\\remind.txt", "r", encoding="utf-8") as remind:
            read = remind.readlines()
        if len(read) != 0:
            # print(float("".join(read[2].split("\n"))) - time.time())
            if float("".join(read[2].split("\n"))) - time.time() <= 0:
                print("Ви просили нагадати вам - "+read[0])
                say_text("Ви просили нагадати вам - "+read[0])

                with open("files\system_files\\remind.txt", "w", encoding="utf-8") as remind:
                    remind.write("")

        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            if answer["text"]:
                yield answer["text"]

check = Check()
if __name__ == "__main__":
    for text in listen():
        if "п'ятниц" in text:
            print(f"Запит: {text}")

            d = ["п'ятниця", "п'ятниці", "п'ятницю", "п'ятниці"]
            for i in d:
                text = "".join(text.split(i))

            ordr = Order(text).blocks()
            print(ordr)

            check.check(ordr)

            
    