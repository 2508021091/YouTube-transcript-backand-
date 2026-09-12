from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)


def get_video_id(url):
    url = url.strip()

    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    if "youtube.com/shorts/" in url:
        return url.split("youtube.com/shorts/")[1].split("?")[0]

    return None


@app.route("/")
def home():
    return "TextFinder YouTube Transcript Backend is running!"


@app.route("/test")
def test():
    return jsonify({
        "success": True,
        "message": "Backend connection is working!"
    })


@app.route("/transcript", methods=["GET"])
def transcript():

    url = request.args.get("url")

    if not url:
        return jsonify({
            "success": False,
            "error": "YouTube URL is required"
        }), 400

    video_id = get_video_id(url)

    if not video_id:
        return jsonify({
            "success": False,
            "error": "Invalid YouTube URL"
        }), 400

    try:
        api = YouTubeTranscriptApi()

        transcript_data = api.fetch(video_id)

        text = " ".join(
            item.text for item in transcript_data
        )

        return jsonify({
            "success": True,
            "video_id": video_id,
            "transcript": text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
