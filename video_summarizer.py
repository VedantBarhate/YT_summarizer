import google.generativeai as genai
from dotenv import load_dotenv
import os

class VideoSummarizer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

    def generate(self, transcript):
        generation_config = {"temperature": 0.4, "top_p":0.7, "top_k":20, "max_output_tokens":9999}
        model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
        try:
            response = model.generate_content(f"Clean and correct the following transcript by fixing typos and grammatical errors while keeping the meaning intact and then please ONLY and ONLY return the full detailed SUMMARY of the cleaned transcript created covering all the points discussed (Make sure to keep title as 'SUMMARY'):\n\n```{transcript}```")
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    with open("transcript.txt", 'r') as file:
        transcript = file.read()

    vid_summarizer = VideoSummarizer()
    resp = vid_summarizer.generate(transcript)
    print(resp)