import boto3
import os

# AWS Access Key ID and Secret Access Key
access_key_id = 'AKIAXYKJRRBQSNB7NKG7'
secret_access_key = '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'

def upload_data_to_s3(directory_path):
    bucket_name = 'story21'
    access_key_id = 'AKIAXYKJRRBQSNB7NKG7'
    secret_access_key = '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'

    # Initialize the S3 client
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    uploaded_files = {}  # Dictionary to store file paths and corresponding S3 URLs

    try:
        # Upload files and subfolders to S3
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, directory_path)
                relative_dir = os.path.dirname(relative_path)
                
                # Construct S3 key based on relative directory path
                s3_key = os.path.join(relative_dir, file)

                # Create folder structure on S3
                s3_folder_path = os.path.join(os.path.basename(directory_path), relative_dir)
                s3_folder_path = s3_folder_path.replace('\\', '/')  # for Windows compatibility
                s3_client.put_object(Bucket=bucket_name, Key=s3_folder_path + '/')
                
                # Upload file to S3
                s3_object_key = s3_folder_path + '/' + file
                s3_client.upload_file(local_file_path, bucket_name, s3_object_key)
                print(f"{local_file_path} uploaded to S3 as {s3_object_key}.")

                # Set public read ACL for the uploaded object
                s3_client.put_object_acl(
                    ACL='public-read',
                    Bucket=bucket_name,
                    Key=s3_object_key
                )

                # Construct S3 URL
                s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_object_key}"
                uploaded_files[local_file_path] = s3_url

    except Exception as e:
        print(f"An error occurred while uploading data to S3: {e}")
        return None
    
    print(f"All files and folders in {directory_path} uploaded successfully to S3.")
    return uploaded_files




import os
import boto3

def download_data_from_s3(folder_name):
    local_directory = f'{folder_name}/raw_images'
    bucket_name = 'story21'
    access_key_id = 'AKIAXYKJRRBQSNB7NKG7'
    secret_access_key = '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'
    
    # Create the local directory if it doesn't exist
    os.makedirs(local_directory, exist_ok=True)
    
    # Initialize the S3 client
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    try:
        # List all objects in the specified S3 folder
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        for obj in objects.get('Contents', []):
            # Extract the key (path) of each object
            s3_key = obj['Key']
            if s3_key.endswith('/'):
                continue
            # Construct the local file path
            local_path = os.path.join(local_directory, os.path.basename(s3_key))
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            # Download the file from S3
            s3_client.download_file(bucket_name, s3_key, local_path)
            print(f"{s3_key} downloaded successfully to {local_path}.")
    except Exception as e:
        print(f"An error occurred while downloading files from S3: {e}")
        return False
    
    print(f"All files in {folder_name} downloaded successfully to {local_directory}.")
    return True

#download_data_from_s3("output", "output", bucket_name='story21')

#upload_data_to_s3('output')

    # AWS credentials
    


def text_to_speech(text, lang, output, output_format='mp3'):
    language = {
    'Arabic': 'arb',
    'Arabic (Gulf)': 'ar-AE',
    'Catalan': 'ca-ES',
    'Chinese (Cantonese)': 'yue-CN',
    'Chinese (Mandarin)': 'cmn-CN',
    'Danish': 'da-DK',
    'Dutch (Belgian)': 'nl-BE',
    'Dutch': 'nl-NL',
    'English (Australian)': 'en-AU',
    'English (British)': 'en-GB',
    'English (Indian)': 'en-IN',
    'English (New Zealand)': 'en-NZ',
    'English (South African)': 'en-ZA',
    'English (US)': 'en-US',
    'English (Welsh)': 'en-GB-WLS',
    'Finnish': 'fi-FI',
    'Hindi': 'hi-IN',
    'French': 'fr-FR',
    'French (Belgian)': 'fr-BE',
    'French (Canadian)': 'fr-CA',
    'German': 'de-DE',
    'German (Austrian)': 'de-AT',
    'Icelandic': 'is-IS',
    'Italian': 'it-IT',
    'Japanese': 'ja-JP',
    'Korean': 'ko-KR',
    'Norwegian': 'nb-NO',
    'Polish': 'pl-PL',
    'Portuguese (Brazilian)': 'pt-BR',
    'Portuguese (European)': 'pt-PT',
    'Romanian': 'ro-RO',
    'Russian': 'ru-RU',
    'Spanish (European)': 'es-ES',
    'Spanish (Mexican)': 'es-MX',
    'Spanish (US)': 'es-US',
    'Swedish': 'sv-SE',
    'Turkish': 'tr-TR',
    'Welsh': 'cy-GB'}



    polly_client = boto3.client('polly', region_name='us-east-1',
                                aws_access_key_id = 'AKIAXYKJRRBQY2MQLNAD',
                                aws_secret_access_key = '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')

    # Get the list of available voices
    response = polly_client.describe_voices(LanguageCode=language[lang])  
    print(language[lang])

    voices = response['Voices']
    print("voice=",voices)
    z=0
    if lang=="Hindi":
        voice_id2='Kajal'
        z=1
    else:

        # Iterate over voices to find a suitable voice
        for voice in voices:
            if 'neural' in voice["SupportedEngines"]:
                voice_id2 = voice["Id"]
                print(voice_id2)
                z=1
                break
            else:
                voice_id2 = voice["Id"]
                print(voice_id2)

    try:
        print(z)
        # Request the text-to-speech conversion
        if z==1:  # Check if voice_id2 is assigned a value
            response = polly_client.synthesize_speech(
                Text=text,
                VoiceId=voice_id2,
                OutputFormat=output_format,
                Engine="neural"
            )
        else:
            response = polly_client.synthesize_speech(
                Text=text,
                VoiceId=voice_id2,
                OutputFormat=output_format
            )
    except Exception as e:
        print(f'Error synthesizing speech: {e}')
        return

    # Save the audio stream to a file
    audio_stream = response['AudioStream'].read()
    with open(output, 'wb') as file:
        file.write(audio_stream)

def separate_arrays(urls_dict):
    image_files = []
    video_files = []
    audio_files = []
    csv_files = []

    for file_path, url in urls_dict.items():
        if file_path.endswith('.png'):
            image_files.append(url)
        elif file_path.endswith('.mp4'):
            video_files.append(url)
        elif file_path.endswith('.mp3'):
            audio_files.append(url)
        elif file_path.endswith('.csv'):
            csv_files.append(url)

    return image_files, video_files, audio_files, csv_files