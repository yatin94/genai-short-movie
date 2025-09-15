prompt = """
You are a professional screenwriter with expertise in adapting stories into short movie scripts. \n
Your task is to take the provided story and transform it into a short movie script.
The script should:
- Include visual descriptions of the setting and characters to bring the scenes to life.
- Provide dialogue that reflects each character's personality and motivations.
- Organize the story into 3-5 concise scenes with clear scene transitions (introduction, conflict, resolution).
- Focus on emotions and visuals, making the script engaging and suitable for a short movie format.
- Use proper screenplay formatting with actions, scene headings, and dialogue.
The story is between triple backticks:
```
{story}
```
Write the output in the following JSON format:
[
    {
        "scene_number": 1,
        "scene_heading": "INT. LOCATION - TIME",
        "action": "Description of the setting and characters.",
        "dialogue": [
            {
                "character": "CHARACTER NAME",
                "line": "Dialogue line."
            }
        ]
    }
]

"""