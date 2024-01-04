from habanero import cn
import requests
import random
import pandas as pd
import csv
import os

def get_random_doi():

    for i in range(50):
        # Define the URL for the OpenAlex API
        url = "https://api.openalex.org/works/random"

        # Make a GET request to the OpenAlex API
        response = requests.get(url)

        # Parse the JSON response
        data = dict(response.json())

        if data['doi'] != None:
            return data['doi']
        else:
            continue

def get_bibtex(doi):
    try:
        return cn.content_negotiation(ids = doi, format = 'text', style='bibtex')
    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occurred: {e}")

def get_random_style(doi):

    styles = ['apa', 'harvard3', 'elsevier-harvard', 'mla', 'ecoscience', 'chicago-author-date','ieee', 'council-of-science-editors']
    random_style = random.choice(styles)
    styled_citation = cn.content_negotiation(ids = doi, format = 'text', style=random_style)
    return styled_citation, random_style

def main():
    # Create a dataframe to store the results
    df = pd.DataFrame(columns=['doi', 'bibtex', 'citation', 'citation_format'])

    # Define the URL for the Crossref API
    doi = get_random_doi()

    # Get the bibtex
    bibtex = get_bibtex(doi)

    try:
        if bibtex is None:
            return
        
        bibtex = bibtex.replace('\n', ' ')
        # Get the citation
        citation, random_style = get_random_style(doi)

        # Remove newlines from the citation
        citation = citation.replace('\n', ' ')

        # Add the results to the dataframe, using concat
        df = pd.concat([df, pd.DataFrame([[doi, bibtex, citation, random_style]], columns=['doi', 'bibtex', 'citation', 'citation_format'])], ignore_index=True)
        print(df)

        # Check if the output.csv file already exists
        if os.path.isfile('output.csv'):
            # Append the dataframe to the existing file
            df.to_csv('output.csv', mode='a', header=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        else:
            # Save the dataframe to a new file
            df.to_csv('output.csv', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        # Print the citation
        print(citation)
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    main()