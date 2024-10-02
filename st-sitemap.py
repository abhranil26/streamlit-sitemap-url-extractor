import requests
import csv
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import streamlit as st

def get_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)

    if response.status_code == 200:
        xml_content = response.text
        root = ET.fromstring(xml_content)

        urls = []
        for elem in root.iter():
            if elem.tag.endswith("url"):
                for loc_elem in elem.iter():
                    if loc_elem.tag.endswith("loc"):
                        urls.append(loc_elem.text)

        return urls
    else:
        st.error(f"Failed to fetch sitemap: {response.status_code}")
        return []

if __name__ == "__main__":
    # Add sidebar
    st.sidebar.title("About This Tool")
    st.sidebar.write("""
    This is a Sitemap URL Extractor tool that allows you to:
    
    - Extract URLs from sitemaps
    - Parse XML sitemaps online
    - Generate a list of all URLs in a sitemap
    
    Keywords: sitemap extractor, extract urls from sitemap, url extractor online
    
    How to use:
    1. Enter the sitemap URL in the main panel
    2. Click 'Fetch URls'
    3. View the extracted URLs and download the CSV file
    """)

    st.title("Sitemap URL Extractor")

    sitemap_url = st.text_input("Enter the sitemap URL:")

    if st.button("Fetch URls"):
        urls = get_sitemap_urls(sitemap_url)
        if urls:
            # Generate the CSV filename based on the website address
            parsed_url = urlparse(sitemap_url)
            website_address = parsed_url.netloc
            output_filename = f"{website_address}_url_list.csv"
            # Display a prominent download button at the top
            csv_data = '\n'.join(urls)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=output_filename,
                mime="text/csv"
            )


            # Display the parsed URLs in a text box with a copy button
            st.subheader("Parsed URLs:")
            url_text = "\n".join(urls)
            st.code(url_text, language='http')

            
        else:
            st.warning("No URLs found in the sitemap.")
