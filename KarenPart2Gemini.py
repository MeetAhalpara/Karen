import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("KAREN_GEMINI")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# List of all common movie genres
ALL_GENRES = [
    "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", 
    "Romance", "Sci-Fi", "Thriller", "War", "Western", "Documentary", "Animation"
]

# Function to analyze user input and extract movie preferences
def analyze_preferences(user_input):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Extract movie preferences from the user's message. Identify:
    - Preferred genre (if mentioned, else omit it)
    - Disliked genres (if mentioned, else omit it)
    - Mood (if mentioned, else omit it)

    If the user only provides dislikes, return a list of movie genres excluding the disliked ones.

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

        # If dislikes exist, remove them from the full genre list
        if "disliked_genre" in preferences:
            disliked = preferences["disliked_genre"]
            available_genres = [genre for genre in ALL_GENRES if genre not in disliked]
            preferences["available_genres"] = available_genres  # Add the list of remaining genres

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
        print(f"🎬 Available Genres: {', '.join(preferences['available_genres'])}")

        # Ask again if the user only gave dislikes
        if not preferred_genre:
            preferred_genre = input("\nWhich genre do you prefer from the available options? ")
            print(f"\n✅ Great! You chose: {preferred_genre}")

    # Ask for mood if not provided
    if not mood:
        mood = input("\nHow do you want the movie to feel? (e.g., fast-paced, emotional, thrilling, relaxing): ")
        print(f"\n🎭 Got it! You prefer {mood} movies.")
        
