import requests

for i in range(5):
    # Define the URL for the OpenAlex API
    url = "https://api.openalex.org/works/random"

    # Make a GET request to the OpenAlex API
    response = requests.get(url)

    # Parse the JSON response
    data = dict(response.json())

    # Extract the necessary information
    try:
        resource_type = data['type']
        title = data['title']
        author = data['authorships'][0]['author']['display_name']
        year = data['publication_year']
        publisher = data['primary_location']['source']['display_name']
    except (TypeError, IndexError):
        continue


    # Format the extracted information into a BibLaTeX entry
    bib_entry = f"@{resource_type }" + "{\n"
    if 'title' in locals():
        bib_entry += f"  title={{ {title} }},\n"
    if 'author' in locals():
        bib_entry += f"  author={{ {author} }},\n"
    if 'year' in locals():
        bib_entry += f"  year={{ {year} }},\n"
    if 'publisher' in locals():
        bib_entry += f"  publisher={{ {publisher} }},\n"
    bib_entry += "}\n\n"

    # Write the BibLaTeX entry to a .bib file
    with open('output.bib', 'a') as f:
        f.write(bib_entry)