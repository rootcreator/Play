from googleapiclient.discovery import build

# YouTube API credentials
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_youtube_video(track_name, artist_name=None):
    # Formulate the search query based on the provided track and artist information
    search_query = f"{track_name} {artist_name}" if artist_name else track_name

    # Example: Search for a video related to the track on YouTube
    search_response = youtube.search().list(
        q=search_query,
        part='id',
        maxResults=1,
        type='video'
    ).execute()

    if 'items' in search_response and search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        # Retrieve other video information or proceed to display the video
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    else:
        return None

