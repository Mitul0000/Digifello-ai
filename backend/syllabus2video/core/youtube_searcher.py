from yt_dlp import YoutubeDL
from .input_and_processing import generate_targeted_search_strings


def search_youtube(query:str, max_results=20):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True
    }

    search_url = f"ytsearch{max_results}:{query}"
    links = []

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_url, download=False)
        for entry in result.get("entries", []):
            duration = entry.get("duration")
            if (duration is None or duration<600):
                continue
            links.append({
                "link": f"https://www.youtube.com/watch?v={entry['id']}",
                "title": entry.get("title"),
                "description": entry.get("description"),
                "duration":duration
                })

    return links

def get_unique_youtube_links(syllabus: str,
    student_bio: str,
    language: str,
    time_limit: str):

    search_strings = generate_targeted_search_strings(
        syllabus=syllabus,
        student_bio=student_bio,
        language=language,
        time_limit=time_limit)

    all_links = []

    # Step 2: Search YouTube for each string
    for i, query in enumerate(search_strings, 1):
        videos = search_youtube(query)
        all_links.extend(videos)

    # Step 3: Remove duplicate videos using link as key
    unique_map = {}
    for video in all_links:
        unique_map[video["link"]] = video

    unique_links = list(unique_map.values())
    return unique_links


