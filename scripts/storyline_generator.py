import openai
from scripts.settings import OPENAI_API_KEY

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_storyline(user_prompt):
    """Generate a short story based on user prompt."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Create a simple text-based story for a game."},
                {"role": "user", "content": f"Generate a short adventure story about {user_prompt} that involves if-else decisions."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Storyline Error: {e}")
        return f"A simple adventure about {user_prompt}!"
