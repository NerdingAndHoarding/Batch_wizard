import os
import wave
import audioop

def stereo_to_mono(input_path, output_path):
    with wave.open(input_path, 'rb') as wf:
        params = wf.getparams()
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        
        frames = wf.readframes(nframes)
        
        # If already mono, just copy
        if nchannels == 1:
            with wave.open(output_path, 'wb') as out:
                out.setparams(params)
                out.writeframes(frames)
            return
        
        # Convert stereo to mono
        mono_frames = audioop.tomono(frames, sampwidth, 0.5, 0.5)
        
        with wave.open(output_path, 'wb') as out:
            out.setnchannels(1)
            out.setsampwidth(sampwidth)
            out.setframerate(framerate)
            out.writeframes(mono_frames)

def main():
    for filename in os.listdir('.'):
        if filename.lower().endswith('.wav'):
            input_file = filename
            output_file = f"mono_{filename}"
            
            print(f"Converting: {input_file} -> {output_file}")
            stereo_to_mono(input_file, output_file)

if __name__ == "__main__":
    main()