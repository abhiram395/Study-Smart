from googlesearch import search

query = "Compiler design previous year question paper pdf post 2020"
print(f"Searching for: {query}")

try:
    for i, url in enumerate(search(query, num_results=10)):
        print(f"{i+1}: {url}")
except Exception as e:
    print(f"Error: {e}")
