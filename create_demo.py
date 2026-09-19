import math
import os
import struct
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip, AudioFileClip, CompositeAudioClip

PROJECT_ID = "qwiklabs-gcp-03-bec4fda9e582"
BUCKET_NAME = "fitgear-coach-assets-qwiklabs-gcp-03-bec4fda9e582"


def generate_lofi_audio(filename="lofi_music.wav", duration=20.0, sample_rate=44100):
    """Generates an upbeat lo-fi background track with kick, snare, hi-hats, chords, and bass."""
    num_samples = int(duration * sample_rate)
    audio = np.zeros(num_samples, dtype=np.float32)

    bpm = 88.0
    beat_samples = int(sample_rate * (60.0 / bpm))
    bar_samples = beat_samples * 4

    # Chords (Emaj7 -> C#m7 -> F#m7 -> B7)
    chords = [
        [329.63, 415.30, 493.88, 622.25], # Emaj7
        [277.18, 329.63, 415.30, 493.88], # C#m7
        [369.99, 440.00, 554.37, 659.25], # F#m7
        [246.94, 308.41, 369.99, 493.88], # B7
    ]
    bass_freqs = [164.81, 138.59, 185.00, 123.47]

    t = np.linspace(0, duration, num_samples, False)

    # 1. Generate Drums (Kick on 1 & 3, Snare on 2 & 4, Hi-hats every 8th note)
    for i in range(num_samples):
        beat_pos = (i % beat_samples) / sample_rate
        bar_pos = (i % bar_samples) / beat_samples

        # Kick on beat 0 and 2.5
        if int(bar_pos) in [0] and beat_pos < 0.15:
            audio[i] += np.sin(2 * np.pi * 60 * np.exp(-30 * beat_pos) * beat_pos) * np.exp(-15 * beat_pos) * 0.7
        elif bar_pos >= 2.5 and bar_pos < 2.65 and (i % (beat_samples // 2)) / sample_rate < 0.15:
            sub_pos = (i % (beat_samples // 2)) / sample_rate
            audio[i] += np.sin(2 * np.pi * 55 * np.exp(-30 * sub_pos) * sub_pos) * np.exp(-15 * sub_pos) * 0.5

        # Snare/Rimshot on beat 1 and 3
        if int(bar_pos) in [1, 3] and beat_pos < 0.12:
            noise = (np.random.rand() * 2 - 1) * np.exp(-25 * beat_pos)
            tone = np.sin(2 * np.pi * 180 * beat_pos) * np.exp(-30 * beat_pos)
            audio[i] += (noise * 0.4 + tone * 0.3)

        # Hi-hat on every 8th note
        eighth_samples = beat_samples // 2
        eighth_pos = (i % eighth_samples) / sample_rate
        if eighth_pos < 0.05:
            hat = (np.random.rand() * 2 - 1) * np.exp(-60 * eighth_pos) * 0.15
            audio[i] += hat

    # 2. Add Warm Lo-Fi Chords
    for bar in range(int(duration / (bar_samples / sample_rate)) + 1):
        bar_start = bar * bar_samples
        chord = chords[bar % len(chords)]
        bass = bass_freqs[bar % len(bass_freqs)]

        for i in range(bar_start, min(bar_start + bar_samples, num_samples)):
            pos = (i - bar_start) / sample_rate
            
            # Gentle chord pad fade in/out
            pad_env = np.sin(np.pi * pos / (bar_samples / sample_rate))
            
            chord_val = 0
            for freq in chord:
                # Soft sine with subtle detune for lo-fi warmth
                chord_val += np.sin(2 * np.pi * freq * pos) + 0.3 * np.sin(2 * np.pi * (freq * 1.002) * pos)
            
            # Warm sub-bass
            bass_val = np.sin(2 * np.pi * (bass / 2) * pos) * 0.4
            
            audio[i] += (chord_val * 0.08 + bass_val) * pad_env

    # 3. Add Subtle Vinyl Crackle / Warmth
    crackle = (np.random.rand(num_samples) * 2 - 1) * 0.015
    audio += crackle

    # Normalize audio
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = (audio / max_val * 0.85 * 32767).astype(np.int16)

    # Write WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    print(f"Generated lo-fi track: {filename}")
    return filename


def make_frame(t):
    """Renders a 1280x720 video frame at timestamp t."""
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color=(15, 23, 42)) # Slate dark theme
    draw = ImageDraw.Draw(img)

    # Gradient header bar (Emerald / Teal)
    draw.rectangle([0, 0, width, 80], fill=(13, 148, 136))
    
    # Title & Subtitle text
    draw.text((30, 20), "FitGear Coach — Expert AI Fitness & Gear Advisor", fill=(255, 255, 255))
    draw.text((30, 48), "Live Cloud Run Agent Demo | Powered by Google ADK & Gemini", fill=(204, 251, 241))

    # Sidebar
    draw.rectangle([30, 100, 320, 680], fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((50, 120), "Capabilities", fill=(13, 148, 136))
    
    caps = [
        "🏃 Trail Shoes Recommendation",
        "🖼️ Imagen 3 Gear Visualization",
        "🎥 Omni Video Generation",
        "⏱️ Race Split Pace Calculator",
        "🌦️ Outdoor Weather Integration",
        "🗺️ Nearby Parks & Gym Maps",
        "🌿 Herbal RAG Knowledge",
        "🔥 Firestore Workout Plans",
    ]
    for idx, cap in enumerate(caps):
        draw.text((50, 160 + idx * 45), cap, fill=(226, 232, 240))

    # Main Chat Window
    draw.rectangle([340, 100, 1250, 680], fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # Timeline-based scenario rendering
    if t < 4.0:
        # Scene 1: Introduction & Prompt Chips
        draw.rectangle([360, 120, 1230, 180], fill=(30, 41, 59), outline=(13, 148, 136), width=1)
        draw.text((380, 135), "Welcome to FitGear Coach! Click an example prompt or ask any fitness/gear request:", fill=(255, 255, 255))
        
        draw.rectangle([380, 200, 720, 240], fill=(13, 148, 136))
        draw.text((395, 212), "🏃 Recommend trail shoes for wet terrain", fill=(255, 255, 255))
        
        draw.rectangle([735, 200, 1020, 240], fill=(13, 148, 136))
        draw.text((750, 212), "⏱️ Calculate 10k pace splits", fill=(255, 255, 255))

    elif t < 10.0:
        # Scene 2: User Prompt & Agent Reasoning Response
        # User message bubble
        draw.rectangle([700, 120, 1220, 170], fill=(13, 148, 136))
        draw.text((715, 135), "You: Recommend trail shoes for wet terrain & generate an image", fill=(255, 255, 255))

        # Agent A2UI Response Card
        draw.rectangle([360, 190, 1220, 620], fill=(30, 41, 59), outline=(13, 148, 136), width=2)
        draw.text((380, 210), "FitGear Coach | Recommended Trail Running Shoes", fill=(52, 211, 153))
        draw.text((380, 245), "• Shoe Model: MudGrip Pro 3 (Gore-Tex Trail Runner)", fill=(226, 232, 240))
        draw.text((380, 275), "• Traction: Vibram Megagrip 5mm deep lugs for wet mud & slick rock", fill=(226, 232, 240))
        draw.text((380, 305), "• Cushioning: Medium-firm EVA midsole with protective rock plate", fill=(226, 232, 240))

        # Generated Image Mock Card
        draw.rectangle([380, 340, 800, 590], fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        # Simulated trail shoe graphic
        draw.ellipse([420, 420, 760, 520], fill=(5, 150, 105))
        draw.polygon([(420, 470), (500, 400), (680, 420), (760, 470)], fill=(13, 148, 136))
        draw.text((450, 545), "Generated Gear Image | Imagen 3", fill=(204, 251, 241))

    elif t < 16.0:
        # Scene 3: Omni Video & Pacing
        draw.rectangle([700, 120, 1220, 170], fill=(13, 148, 136))
        draw.text((715, 135), "You: Generate a short video showing trail shoes on a wet trail", fill=(255, 255, 255))

        draw.rectangle([360, 190, 1220, 620], fill=(30, 41, 59), outline=(13, 148, 136), width=2)
        draw.text((380, 210), "FitGear Coach | Gemini Omni Video Generation", fill=(52, 211, 153))
        draw.text((380, 245), "Generating video with Google's Omni Model (gemini-omni-flash-preview)...", fill=(226, 232, 240))
        
        # Simulated Video Player Box
        draw.rectangle([380, 280, 950, 580], fill=(15, 23, 42), outline=(13, 148, 136), width=3)
        draw.polygon([(630, 400), (630, 460), (690, 430)], fill=(52, 211, 153))
        draw.text((430, 535), "Public URL: https://storage.googleapis.com/.../gear_video.mp4", fill=(148, 163, 184))

    else:
        # Scene 4: Call to Action & Conclusion
        draw.rectangle([360, 190, 1220, 620], fill=(30, 41, 59), outline=(13, 148, 136), width=3)
        draw.text((450, 250), "FitGear Coach is Live and Deployed!", fill=(255, 255, 255))
        draw.text((420, 320), "Cloud Run URL:", fill=(204, 251, 241))
        draw.text((420, 360), "https://fitgear-coach-frontend-1083993840257.us-central1.run.app", fill=(52, 211, 153))
        draw.text((420, 430), "Features Supported:", fill=(204, 251, 241))
        draw.text((440, 470), "• Full Google ADK Agent Engine Integration", fill=(226, 232, 240))
        draw.text((440, 505), "• A2UI v0.8 Structured Cards", fill=(226, 232, 240))
        draw.text((440, 540), "• Firestore, Maps, Weather, RAG & Multimodal Generation", fill=(226, 232, 240))

    return np.array(img)


def main():
    duration = 20.0
    fps = 10

    # 1. Generate Lo-Fi Music Track
    audio_file = generate_lofi_audio("lofi_music.wav", duration=duration)

    # 2. Render Frames
    frames = []
    total_frames = int(duration * fps)
    print(f"Rendering {total_frames} video frames...")
    for f in range(total_frames):
        t = f / fps
        frames.append(make_frame(t))

    video_clip = ImageSequenceClip(frames, fps=fps)
    audio_clip = AudioFileClip(audio_file)
    
    # Attach audio to video
    video_clip = video_clip.with_audio(audio_clip)

    out_file = "fitgear_coach_demo.mp4"
    video_clip.write_videofile(
        out_file,
        codec="libx264",
        audio_codec="aac",
        fps=fps,
    )
    print(f"Successfully generated demo video with upbeat lo-fi music: {out_file}")

    # 3. Upload demo video to public Cloud Storage bucket
    try:
        from google.cloud import storage
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob("fitgear_coach_demo.mp4")
        blob.upload_from_filename(out_file, content_type="video/mp4")
        print(f"Uploaded demo video to GCS: https://storage.googleapis.com/{BUCKET_NAME}/fitgear_coach_demo.mp4")
    except Exception as e:
        print("GCS upload warning:", e)


if __name__ == "__main__":
    main()
