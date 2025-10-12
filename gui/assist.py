# System imports:
import os               # For environment variables
import time             # For performance measurement
import perplexity       # For Perplexity AI API

# Class Gemini: A wrapper that fetches responses from Google's Gemini API:
class Assistant:

    # Initializer:
    def __init__(self):

        self._api_key = os.getenv("PERPLEXITY_API_KEY") # Read API-key from environment variable.
        self._enabled = bool(self._api_key)             # Check if API-key is defined.
        self._msg_arr = [
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information."
             }
        ]

        # Open JSON-instructions for assistant:
        if  os.path.exists("rss/JSON-instructions.txt"):
            self._msg_arr[0]['content'] = open("rss/JSON-instructions.txt", "r").read()

        # Initialize the client:
        try:
            # Initialize Perplexity AI client:
            self._client = perplexity.Client(api_key=self._api_key)

        except Exception as exception:
            print(f"INFO: An exception occurred: {exception}")
            print(f"AI - assistant has been disabled")
            self._enabled = False

    # Get response from Perplexity:
    def get_response(self, query: str, json: str | None = None):

        # Disabled-check:
        if  not self._enabled:  return "AI-assistant is disabled!"

        # Append the query to the message-array:
        self._msg_arr.append(
            {
                "role": "user",
                "content": query
            }
        )

        # Append user query to message-array:
        try:
            response = self._client.chat.completions.create(
                model = "sonar-reasoning",
                messages = self._msg_arr,
            )

            return response.choices[0].message.content

        except Exception as exception:
            print(f"ERROR: An exception occurred: {exception}")
            return "An error occurred while age-array with system prompt"