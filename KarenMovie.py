import google.generativeai as genai
import os
import json
import difflib
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("KAREN_GEMINI")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# List of valid movie genres
ALL_GENRES = [
    "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western", "Documentary", "Animation"
]

# Common moods (not genres)
MOOD_KEYWORDS = ["slow", "fast-paced", "emotional", "thrilling", "relaxing", "intense", "dark", "uplifting"]

# Function to get the closest match for a genre
def get_closest_genre(user_input, available_genres):
    matches = difflib.get_close_matches(user_input, available_genres, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to analyze user input and extract movie preferences
def analyze_preferences(user_input):
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    Extract movie preferences from the user's message. Identify:
    - Preferred genre (if mentioned and valid)
    - Disliked genres (if mentioned and valid)
    - Mood preferences (if mentioned, otherwise omit)

    IMPORTANT:
    - "Slow" is NOT a genre. It should be treated as a mood.
    - Only recognize genres from this list: {ALL_GENRES}.
    - Only recognize moods from this list: {MOOD_KEYWORDS}.

    User's Message: "{user_input}"

    Reply in a structured JSON format:
    ```
    {{
        "preferred_genre": "Extracted preferred genre (if any, else omit)",
        "disliked_genre": ["Extracted disliked genre(s) (if any, else omit)"],
        "mood": "Extracted mood (if any, else omit)"
    }}
    ```
    """

    try:
        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("Empty response from Gemini.")

        # Clean response (remove ```json ... ```)
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        preferences = json.loads(json_text)  # Convert response to JSON

        # Ensure "slow" is only treated as a mood
        if "mood" in preferences and preferences["mood"] not in MOOD_KEYWORDS:
            preferences.pop("mood")  # Remove invalid mood

        # If "slow" was mistakenly classified as a genre, move it to moods
        if "disliked_genre" in preferences:
            disliked_genres = preferences["disliked_genre"]
            valid_genres = [g for g in disliked_genres if g in ALL_GENRES]
            invalid_moods = [m for m in disliked_genres if m in MOOD_KEYWORDS]

            preferences["disliked_genre"] = valid_genres  # Keep only valid genres
            if invalid_moods:
                preferences["mood"] = invalid_moods[0]  # Move the first invalid mood to moods

        return preferences

    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Error parsing Gemini response: {e}. Using default values.")
        return {}

# Example Usage
if __name__ == "__main__":
    user_input = input("\nDescribe the kind of movies you like (e.g., 'I love sci-fi but hate romance and slow movies'): ")
    preferences = analyze_preferences(user_input)

    print("\n🎬 Extracted Preferences:")

    # Display extracted preferences
    preferred_genre = preferences.get("preferred_genre")
    disliked_genres = preferences.get("disliked_genre", [])
    mood = preferences.get("mood")

    if preferred_genre:
        print(f"✅ Preferred Genre: {preferred_genre}")

    if disliked_genres:
        print(f"❌ Disliked Genre(s): {', '.join(disliked_genres)}")

    if mood:
        print(f"🎭 You dislike {mood} movies. We won’t recommend that.")

    # Ask for a mood only if not already extracted and ensure it's not disliked
    if not mood:
        while True:
            mood = input("\nHow do you want the movie to feel? (e.g., fast-paced, emotional, thrilling, relaxing): ")

            if mood.lower() in [d.lower() for d in disliked_genres]:
                print(f"❌ You mentioned you dislike '{mood}'. Please choose a different mood.")
            else:
                print(f"\n🎭 Got it! You prefer {mood} movies.")
                break
