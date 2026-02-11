import os
from dotenv import load_dotenv
from google import genai
import re

# --- CONFIGURATION ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_targeted_search_strings(
        syllabus: str,
        student_bio : str,
        language : str,
        time_limit: str
):
    prompt = f"""
   As an expert educational consultant, generate 10 precise YouTube search strings for a student with the following profile:
    - Syllabus: {syllabus}
    - Student Level: {student_bio}
    - Preferred Language: {language}
    - Time Available: {time_limit}
    - Each string suggested should be such that if searched in youtube, the output video should cover all the topics present in the syllebus.
    - The string should not be so long. It should be of normal length.
    - Example:- If the syllebus is :- Electrostatics field, electric flux density, electric field strength,
    absolute permittivity, relative permittivity, capacitance and
    capacitor, composite dielectric capacitors, capacitors in series and
    parallel, energy stored in capacitors, charging and discharging of
    capacitors and time constant.
    -One of the string here can be "Electrostatics and capacitance full chapter for BTech first year Hinglish"
    Return ONLY a numbered list of the 10 strings.
    """


    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text
        search_strings = re.findall(r'^\d+\.\s*(.*)', raw_text, re.MULTILINE)

        return search_strings

    except Exception as e:
        raise RuntimeError(f"Gemini error: {str(e)}")
