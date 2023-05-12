from flask import Flask, render_template, request
import openai
from googleapiclient.discovery import build
import os

app = Flask(__name__)


# Set up OpenAI API credentials
openai.api_key = 'OPEN_AI_API_KEY'


# Set up YouTube API credentials

youtube_api_key = 'YOUTUBE_API_KEY'


youtube = build('youtube', 'v3', developerKey=youtube_api_key)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")

    # Check if the user is searching for videos
    if message.startswith("search"):
        # Extract the search query from the message
        query = message.split("search ")[1]

        # Send a search request to the YouTube API and retrieve the results
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=3
        ).execute()

        # Extract the relevant information from the search results and display it to the user
        videos = []
        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            description = search_result['snippet']['description']
            thumbnail_url = search_result['snippet']['thumbnails']['default']['url']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                "title": title,
                "description": description,
                "thumbnail_url": thumbnail_url,
                "video_url": video_url
            })

        return {"videos": videos}

    else:

        # Send the message to OpenAI's API and receive the response

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
        
        
    if completion.choices[0].message != None:
        return completion.choices[0].message

    else:
        return 'Failed to Generate response!'


if __name__ == '__main__':
    app.run()
