TOOLS: WhipserModel
## Speech Recognition With OpenAI's Whisper
Hardware Components: Raspberry Pi, adafruit mini usb microphone

Wiring Connections: There are none.

- First we make an audio recording using these commands:
```Linux
$ arecord -l
ffmpeg -f alsa -i plughw:0,0 -t 10 output_feb_21_a.mp4
```


```
```Python
from faster_whisper import WhisperModel

model_size = "tiny.en"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(
    "output_feb_21_a.mp4",
    beam_size=5
)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

```

- This code downloads whisper which is openai model for speech recognition and prints out the text from an audio recording. 
## Menu ordering via voice
```Python
import os
import subprocess
from faster_whisper import WhisperModel
from rapidfuzz import process, fuzz

# -----------------------------
# CONFIG
# -----------------------------
AUDIO_DEVICE = "plughw:0,0"   # Change if needed from arecord -l
RECORD_SECONDS = 10
AUDIO_FILE = "order.mp4"

MODEL_SIZE = "tiny.en"        # 🔥 Using tiny.en (fastest for Pi)
COMPUTE_TYPE = "int8"

MENU = [
    "cheeseburger",
    "big mac",
    "french fries",
    "chicken nuggets",
    "coke",
    "sprite",
    "iced coffee",
    "water",
    "milkshake"
]

MATCH_THRESHOLD = 55


# -----------------------------
# RECORD AUDIO
# -----------------------------
def record_audio():
    print(f"\n🎙️ Recording for {RECORD_SECONDS} seconds...")
    cmd = [
        "ffmpeg",
        "-f", "alsa",
        "-i", AUDIO_DEVICE,
        "-t", str(RECORD_SECONDS),
        "-y",
        AUDIO_FILE
    ]
    subprocess.run(cmd)
    print("✅ Recording saved.")


# -----------------------------
# TRANSCRIBE WITH WHISPER
# -----------------------------
def transcribe_audio():
    print("\n🧠 Loading Whisper tiny.en model...")
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type=COMPUTE_TYPE)

    print("📝 Transcribing...")
    segments, info = model.transcribe(AUDIO_FILE, beam_size=5)

    full_text = ""
    for seg in segments:
        print(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
        full_text += seg.text.strip() + " "

    print("\n✅ Recognized Text:")
    print(full_text.strip())

    return full_text.strip()


# -----------------------------
# RAPIDFUZZ MATCHING
# -----------------------------
def match_menu_items(recognized_text):
    print("\n🔎 Running RapidFuzz matching...")

    if not recognized_text:
        return []

    text = recognized_text.lower()

    # 1) Sentence-level matching (primary)
    ranked = process.extract(
        text,
        MENU,
        scorer=fuzz.WRatio,
        limit=len(MENU)
    )

    print("\nSentence-level matches (sorted):")
    for item, score, _ in ranked:
        print(f"  {item:16s} → Score: {score}")

    selected = [item for item, score, _ in ranked if score >= MATCH_THRESHOLD]

    # 2) Chunk-level matching (secondary) — no single-word matching
    words = [w.strip(".,?!") for w in text.split()]
    chunks = []

    # build 2-word and 3-word chunks
    for i in range(len(words) - 1):
        chunks.append(words[i] + " " + words[i+1])
    for i in range(len(words) - 2):
        chunks.append(words[i] + " " + words[i+1] + " " + words[i+2])

    print("\nChunk-level matches (proof):")
    for c in chunks[:12]:
        best = process.extractOne(c, MENU, scorer=fuzz.token_set_ratio)
        if best:
            item, score, _ = best
            # use a slightly higher threshold for chunks
            if score >= MATCH_THRESHOLD + 5 and item not in selected:
                print(f"  chunk='{c}' matched '{item}' score={score}")
                selected.append(item)

    return selected
# -----------------------------
# SYSTEM RESOURCE CHECK
# -----------------------------
def show_resources():
    print("\n📊 RAM Usage:")
    subprocess.run(["free", "-h"])

    print("\n📊 CPU Snapshot:")
    subprocess.run(["bash", "-c", "top -b -n 1 | head -n 10"])


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("=== Checkpoint 2: Voice Menu Ordering (tiny.en) ===")

    record_audio()
    text = transcribe_audio()
    selected_items = match_menu_items(text)

    print("\n🧾 FINAL ORDER:")
    if selected_items:
        for item in selected_items:
            print("-", item)
    else:
        print("No confident menu items matched.")

    show_resources()
    print("\n✅ System Complete.")


if __name__ == "__main__":
    main()

```

- This program creates a simple voice-based food ordering system that runs locally on a Raspberry Pi. First, it records 10 seconds of audio from a USB microphone using ffmpeg and saves it as an audio file. Then, it uses the Faster-Whisper tiny.en speech recognition model to convert the spoken audio into text. After that, RapidFuzz compares the recognized text against a predefined list of menu items and calculates similarity scores to determine which items were ordered. Finally, the matched menu items are displayed as the final order, and the system prints CPU and memory usage to demonstrate awareness of resource usage on an embedded device.
![[20260225_15h52m41s_grim.png]]
