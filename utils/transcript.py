"""
transcript.py
─────────────
Fetches YouTube transcript using youtube-transcript-api (primary)
with yt-dlp as a fallback. Handles rate limiting and multiple languages.
"""

import re
import json
import time
import urllib.request


def extract_video_id(url: str):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript_via_api(video_id: str):
    """Primary method: uses youtube-transcript-api"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try manual English first, then auto-generated, then any language
        transcript = None
        try:
            transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
        except Exception:
            pass

        if not transcript:
            try:
                transcript = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
            except Exception:
                pass

        if not transcript:
            # Take whatever is available
            for t in transcript_list:
                transcript = t
                break

        if not transcript:
            return None, "No transcripts available."

        segments = transcript.fetch()
        text = " ".join(seg["text"].strip() for seg in segments if seg.get("text", "").strip())
        return text, None

    except Exception as e:
        err = str(e)
        if "disabled" in err.lower() or "TranscriptsDisabled" in err:
            return None, "Transcripts are disabled for this video."
        return None, f"youtube-transcript-api error: {e}"


def get_transcript_via_ytdlp(video_id: str):
    """Fallback method: uses yt-dlp"""
    try:
        import yt_dlp

        full_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "socket_timeout": 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(full_url, download=False)

            subtitles = info.get("subtitles", {}) or {}
            auto_captions = info.get("automatic_captions", {}) or {}

            chosen = subtitles.get("en") or auto_captions.get("en")
            if not chosen:
                for v in list(subtitles.values()) + list(auto_captions.values()):
                    if v:
                        chosen = v
                        break

            if not chosen:
                return None, "No captions found for this video."

            json3_url = next((f["url"] for f in chosen if f.get("ext") == "json3"), None)
            if not json3_url:
                json3_url = chosen[0]["url"]

            req = urllib.request.Request(json3_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as response:
                content = response.read().decode("utf-8")

            try:
                data = json.loads(content)
                texts = [
                    seg.get("utf8", "").strip()
                    for event in data.get("events", [])
                    for seg in event.get("segs", [])
                    if seg.get("utf8", "").strip()
                ]
                transcript_text = " ".join(texts)
            except Exception:
                transcript_text = re.sub(r"<[^>]+>", " ", content)
                transcript_text = re.sub(r"\s+", " ", transcript_text).strip()

            return transcript_text, None

    except Exception as e:
        err = str(e)
        if "429" in err or "too many requests" in err.lower():
            return None, "YouTube is rate limiting. Please try again in a few minutes."
        return None, f"yt-dlp error: {e}"


def get_video_title(video_id: str) -> str:
    """Get video title using oEmbed API (no rate limiting)"""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("title", f"YouTube Video ({video_id})")
    except Exception:
        return f"YouTube Video ({video_id})"


def get_transcript(url: str):
    """
    Main entry point. Returns (transcript_text, video_title, error).
    Tries youtube-transcript-api first, then yt-dlp as fallback.
    """
    video_id = extract_video_id(url)
    if not video_id:
        return "", "", "Could not parse YouTube video ID from URL."

    # Get title separately (more reliable)
    video_title = get_video_title(video_id)

    # Method 1: youtube-transcript-api
    text, err = get_transcript_via_api(video_id)
    if text and len(text.strip()) > 50:
        return text, video_title, None

    # Method 2: yt-dlp fallback
    text2, err2 = get_transcript_via_ytdlp(video_id)
    if text2 and len(text2.strip()) > 50:
        return text2, video_title, None

    # Both failed — return best error message
    final_err = err2 or err or "Could not extract transcript from this video."
    return "", video_title, final_err