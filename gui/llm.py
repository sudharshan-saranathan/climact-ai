# System imports:
import os                               # For environment variables
import google.generativeai as genai     # Gemini API client

# Class Gemini: A wrapper that fetches responses from Google's Gemini API:
class Assistant:

    # Initializer:
    def __init__(self):

        self._api_key = os.getenv("GOOGLE_API_KEY")     # Read API-key from environment variable.
        self._enabled = bool(self._api_key)             # Check if API-key is defined.
        self._msg_arr = [
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information."
             }
        ]

        # Open instructions for the assistant, if available:
        if  os.path.exists("rss/sys-instructions.txt"):
            self._msg_arr[0]['content'] = open("rss/JSON-instructions.txt", "r").read()

        # Create a chat session with the Gemini API:
        try:
            self._conf = genai.configure(api_key=self._api_key)
            self._chat = genai.GenerativeModel('gemini-2.5-flash').start_chat(enable_automatic_function_calling=True)

        except Exception as exception:
            print(f"INFO: An exception occurred: {exception}")
            print(f"AI - assistant has been disabled")
            self._enabled = False

    # Get response from Perplexity API:
    def get_response(self, prompt: str) -> str:

        if  not self._enabled:
            return str("The assistant is disabled")

        if  not bool(prompt):
            return str("No prompt provided")

        if  not hasattr(self, '_client'):
            return str("API client is not initialized.")

        return str()
