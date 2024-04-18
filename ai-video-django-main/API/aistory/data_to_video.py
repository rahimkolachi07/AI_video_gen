from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

def create_video(loc):
    audio_folder = f'{loc}/audio'
    image_folder = f'{loc}/image'
    output_file = f'{loc}/video/output_video.mp4'
    
    # Get list of audio files and image files
    audio_files = sorted([file for file in os.listdir(audio_folder) if file.endswith('.mp3')])  # Assuming audio files are in mp3 format
    image_files = sorted([file for file in os.listdir(image_folder) if file.endswith('.png')])  # Assuming image files are in png format
    
    # Initialize video clip list
    video_clips = []

    # Iterate over audio and image files
    for i, (audio_file, image_file) in enumerate(zip(audio_files, image_files)):
        # Load audio clip
        audio_clip = AudioFileClip(os.path.join(audio_folder, audio_file))
        
        # Load image clip
        image_clip = ImageClip(os.path.join(image_folder, image_file))
        
        # Set the duration of the image clip to match the duration of the audio clip
        image_clip = image_clip.set_duration(audio_clip.duration)
        
        # Apply full-screen effect to the image clip
        image_clip = image_clip.resize(height=720)  # Adjust height as needed
        
        # Add transitions for all images except the first one
        if i > 0:
            # Set transition duration
            transition_duration = min(audio_clip.duration, 0.8)  # Use minimum of audio clip duration and 0.5 seconds
            
            # Crossfade transition
            video_clips[-1] = video_clips[-1].crossfadeout(transition_duration)
            image_clip = image_clip.crossfadein(transition_duration)
        
        # Combine audio and image clips
        video_clip = image_clip.set_audio(audio_clip)
        
        # Append to video clips list
        video_clips.append(video_clip)
    
    # Concatenate video clips
    final_clip = concatenate_videoclips(video_clips, method="compose")
    
    # Write final video to file
    final_clip.write_videofile(output_file, fps=24)
    

