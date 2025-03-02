import openai
import json
from scripts.settings import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_storyline(user_prompt, callback):
    """Generate a very short, one-paragraph story."""
    def run():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Generate a VERY short, one-paragraph game story."},
                          {"role": "user", "content": f"Create a quick adventure story about {user_prompt} requiring if-else logic."}]
            )
            
            story = response.choices[0].message.content.strip()
            callback(story)

        except Exception as e:
            print(f"AI Storyline Error: {e}")
            callback("A simple adventure story: Solve the challenge using if-else logic!")

    import threading
    threading.Thread(target=run).start()

def generate_map_from_story(story, callback):
    """Generate path & obstacle coordinates based on the story."""
    def run():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Generate coordinates for a 2D game map based on the story."},
                          {"role": "user", "content": f"Using this story: '{story}', generate a JSON output with:" 
                                                    f"1. 'start': (x, y) starting position." 
                                                    f"2. 'paths': List of (x, y) positions forming a valid path."
                                                    f"3. 'obstacles': List of (x, y) positions for obstacles."
                                                    f"Ensure paths connect logically and obstacles make sense. Use as much of the available space as possible."}]
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Attempt to parse JSON from AI response
            try:
                json_data = json.loads(ai_response)  # Safely parse JSON
            except json.JSONDecodeError:
                print("AI returned invalid JSON, using default map.")
                json_data = {
                    "start": (1, 1),
                    "paths": [(2, 1), (3, 1), (4, 1)],
                    "obstacles": [(3, 2), (5, 1)]
                }

            callback(json_data)

        except Exception as e:
            print(f"AI Map Generation Error: {e}")
            callback({
                "start": (1, 1),
                "paths": [(2, 1), (3, 1), (4, 1)],
                "obstacles": [(3, 2), (5, 1)]
            })

    import threading
    threading.Thread(target=run).start()
