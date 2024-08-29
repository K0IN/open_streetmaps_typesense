import typesense
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
import time

api_key = "xyz"
collection_name = "addresses"


def format_hit(hit):
    return f"{hit['document']['city']} {hit['document']['postcode']} {hit['document']['housenumber']} {hit['document']['street']}"


def format_hit_with_highlight(hit):
    # Start with the original format
    formatted = f"{hit['document']['city']} {hit['document']['postcode']} {hit['document']['housenumber']} {hit['document']['street']}"

    # Apply highlights
    for highlight in hit.get('highlights', []):
        field = highlight['field']
        snippet = highlight['snippet']

        # Replace the original text with the highlighted snippet
        formatted = formatted.replace(hit['document'][field], snippet)

    # Convert Typesense HTML highlights to ANSI color codes
    formatted = formatted.replace(
        '<mark>', '<ansigreen>').replace('</mark>', '</ansigreen>')

    return formatted


class TypesenseCompleter(Completer):
    def __init__(self, client):
        self.client = client

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if len(text) < 2:
            return

        search_parameters = {
            'q': text,
            'query_by': 'city,street,housenumber,postcode',
            'prefix': True,
            'num_typos': 2,
            'per_page': 8
        }

        try:
            start_time = time.time()
            results = self.client.collections[collection_name].documents.search(
                search_parameters)
            for hit in results['hits']:
                yield Completion(
                    format_hit(hit),
                    start_position=-len(text),
                    display=HTML(format_hit_with_highlight(hit))
                )
            yield Completion(
                "",
                start_position=-len(text),
                display=HTML(
                    f"<ansiyellow>Took: {time.time() - start_time } Milliseconds to Search</ansiyellow>")
            )

        except Exception as e:
            print(f"Error during search: {e}")


def main():
    client = typesense.Client({
        'nodes': [{
            'host': 'localhost',
            'port': '8108',
            'protocol': 'http'
        }],
        'api_key': api_key,
        'connection_timeout_seconds': 2
    })

    session = PromptSession(
        completer=TypesenseCompleter(client),
        complete_while_typing=True,
    )

    while True:
        try:
            user_input = session.prompt('Enter a city name: ')
            print(f"You entered: {user_input}")
        except KeyboardInterrupt:
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
