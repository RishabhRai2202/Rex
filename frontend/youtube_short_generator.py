
import requests

# Replace this with your OpenRouter API Key from https://openrouter.ai
API_KEY = "YOUR_API_KEY_HERE"

def get_youtube_short_script(topic: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "example.com",  # replace with your domain if needed
        "X-Title": "YouTube Shorts Generator"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a creative YouTube content writer."},
            {"role": "user", "content": f"Write a 15-second script for a YouTube Short about: {topic}"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    user_topic = input("Enter a topic for your YouTube Short: ")
    script = get_youtube_short_script(user_topic)
    print("\nGenerated Script:\n")
    print(script)
