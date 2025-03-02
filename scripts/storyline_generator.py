import openai
from scripts.settings import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_storyline_and_map(user_prompt, callback):
    """Generate a short story and a map structure with predefined coordinates."""
    def run():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate a VERY short, one-paragraph game story and a valid path."},
                    {"role": "user", "content": f"Create a quick adventure story about {user_prompt} requiring if-else logic. "
                                                 f"Also, provide a JSON format output with hardcoded coordinates for:"
                                                 f"1. Start position (x, y)."
                                                 f"2. Valid paths as a list of (x, y) positions."
                                                 f"3. Obstacle positions as a list of (x, y) positions."}
                ]
            )
            
            ai_response = response.choices[0].message.content.strip()

            # Extract JSON-like structured part
            if "{ " in ai_response:
                json_part = ai_response[ai_response.index("{"):]  # Extract JSON block
                json_data = eval(json_part)  # Convert to dictionary (ensure it's safe)
            else:
                json_data = {"start": (1, 1), "paths": [(2, 1), (3, 1), (4, 1)], "obstacles": [(3, 2), (5, 1)]}

            callback(ai_response, json_data)  # Pass both the story and map structure

        except Exception as e:
            print(f"AI Storyline Error: {e}")
            callback("A simple adventure story: Solve the challenge using if-else logic!", 
                     {"start": (1, 1), "paths": [(2, 1), (3, 1), (4, 1)], "obstacles": [(3, 2), (5, 1)]})

    import threading
    threading.Thread(target=run).start()
