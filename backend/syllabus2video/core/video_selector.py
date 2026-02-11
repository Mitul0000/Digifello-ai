import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from google import genai
from .youtube_searcher import get_unique_youtube_links


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=GEMINI_API_KEY)

def extract_video_id(url):
    return url.split("v=")[-1]


def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item["text"] for item in transcript])
        return text
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None


def prepare_video_data(video_links):
    video_data = []

    for i, links in enumerate(video_links, 1):
        transcript = get_transcript(links["link"])

        video_data.append({
            "description":links["description"],
            "title": links["title"],
            "link": links["link"],
            "transcript": transcript,
            "duration": links["duration"]
        })

    return video_data


def ask_gemini_to_select_videos(
    syllabus,
    student_bio,
    time_limit,
    language,
    video_data
):
    formatted_videos = ""

    for idx, v in enumerate(video_data, 1):
        formatted_videos += f"\nVIDEO {idx}:\n"
        formatted_videos += f"link: {v['link']}\n"
        formatted_videos += f"title: {v['title']}\n"
        formatted_videos += f"description: {v['description']}\n"
        formatted_videos += f"description: {v['duration']}\n"
        if v["transcript"]:
            formatted_videos += f"Transcript:\n{v['transcript'][:4000]}\n"
        else:
            formatted_videos += "Transcript: NOT AVAILABLE\n"

    prompt = f"""
You are an expert academic advisor.

Student profile:
- Level: {student_bio}
- Preferred Language: {language}
- Time Available: {time_limit}

Syllabus:
{syllabus}

You are given multiple YouTube videos.
Some have transcripts, some do not.

TASK:
1. Analyze which videos together cover ALL parts of the syllabus.
2. Prefer videos with transcript available.
3. Also consider title,description while analyzing.
3. Total watch time must fit within the given time limit.
4. Select at MAXIMUM 3 videos.(If any video contains all the topics then suggest only one video only)
5. Videos should be high quality and suitable for the student's level.
6. Do NOT select more than 3 videos.

OUTPUT FORMAT (STRICT):
Note: Use only english language to answer.
1. Video Link
   Reason (short)
2. Video Link
   Reason (short)
3. Video Link
   Reason (short)

Here are the videos:
{formatted_videos}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

def pipeline(syllabus,student_bio,language,time_limit):
    video=get_unique_youtube_links(syllabus,student_bio,language,time_limit)
    final_video=prepare_video_data(video)

    result=ask_gemini_to_select_videos(
    syllabus,
    student_bio,
    time_limit,
    language,
    final_video)
    return result

