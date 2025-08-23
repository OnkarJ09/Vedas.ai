from plugins.audio import take_command
from dotenv import load_dotenv
import sys
import os, re


# Load environment variables from .env file
load_dotenv()


if __name__ == '__main__':
    # Default language is english
    current_language = os.getenv('DEFAULT_LANGUAGE')

    while True:
        """For texting process"""
        query, language_changed = take_command(current_language)


        # query = input("Enter your query: ").lower()
        # language_changed = None

        if query is None:
            continue    # Repeat listening if the command wasn't understood

        if language_changed:
            current_language = query
            continue    # Skip further processing and start listening in new language

        if query == "exit":
            sys.exit(0)
        else:
            """
            Here there will be the logic for the MCP Manager integration.
            """
            pass
            # query = match_query(query)
            #
            # # Find all intent-entity pairs
            # matches = re.findall(r"Intent:\s*(\w+)\s*Entity:\s*(\w+)", query)
            #
            # # Extract and print results
            # res = {}
            # for intent, entity in matches:
            #     print(f"{intent} {entity}")
            #     res[intent] = entity
            #     print(res)