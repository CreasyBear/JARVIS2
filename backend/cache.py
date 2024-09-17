from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_data(query):
    # Fetch data from the database or external API
    data = fetch_data(query)
    return data