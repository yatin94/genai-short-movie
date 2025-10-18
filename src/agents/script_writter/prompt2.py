# prompt = """
# You are a professional screenwriter with expertise in adapting stories into short movie scripts.
# Your task is to take the provided story and transform it into a short movie script.

# Instructions:
# - Provide one scene at a time, starting with scene 1.
# - Each scene should include dialogue that reflects each character's personality and motivations.
# - There should be a total of 3 concise scenes: introduction, conflict, and resolution (scene 3 is the climax).
# - Focus on emotions, making the script engaging and suitable for a very short movie.
# - Only use 2 characters throughout the script.
# - Use proper screenplay formatting with scene headings and dialogue.
# - The list of scenes already generated is provided below. Generate the next scene number (increment the last scene number). If the next scene is scene 3, make it the climax.
# - Output each scene in valid JSON format as specified below, with no extra text or code block markers.

# Scenes already generated:
# {generated_scenes}

# Current Scene Number to Generate: {next_scene_number}

# The story is between triple backticks:
# ```
# {story}
# ```

# Output format:
# {{
#     "scene_number": <number>,
#     "dialogue": [
#         {{
#             "character": "CHARACTER NAME",
#             "line": "Dialogue line."
#         }}
#     ]
# }}
# """




prompt = """
You are a professional screenwriter with expertise in adapting stories into short movie scripts.
Your task is to take the provided story and transform it into a short movie script.

Instructions:
- Provide one scene at a time, starting with scene 1.
- Each scene should include dialogue that reflects each character's personality and motivations.
- There should be a total of 3 concise scenes: introduction, conflict, and resolution (scene 3 is the climax).
- Focus on emotions, making the script engaging and suitable for a very short movie.
- Only use 2 characters throughout the script.
- Use proper screenplay formatting with scene headings and dialogue.
- The list of scenes already generated is provided below.
- Generate the scene with the given scene number: {next_scene_number}.
- If the scene number is 3, make it the climax.
- Output each scene in valid JSON format as specified below, with no extra text or code block markers.

Scenes already generated:
{generated_scenes}

Current Scene Number to Generate: {next_scene_number}

The story is between triple backticks:
```
{story}
```

Output format:
{{
    "scene_number": <number>,
    "dialogue": [
        {{
            "character": "CHARACTER NAME",
            "line": "Dialogue line."
        }}
    ]
}}
"""