import google.generativeai as genai
import os

# Configure the Gemini API with the provided API key.
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

# Read the diff from the file.
with open("diff.txt") as f:
    diff = f.read()

# Generate the review using a formatted multi-line string.
response = model.generate_content(
    f"""Analyze this code diff as a senior developer. Focus on:
1. Potential bugs and errors
2. Security vulnerabilities
3. Code quality improvements
4. Best practices violations

Format response in markdown with clear sections. Be concise but thorough.

Code diff:
{diff}"""
)

# Write the generated review to a file.
with open("review.md", "w") as f:
    f.write(response.text)
