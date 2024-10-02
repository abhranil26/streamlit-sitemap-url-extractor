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
    st.title("Sitemap URL Extractor")

    sitemap_url = st.text_input("Enter the sitemap URL:")

    if st.button("Parse and Generate CSV"):
        urls = get_sitemap_urls(sitemap_url)
        if urls:
            # Generate the CSV filename based on the website address
            parsed_url = urlparse(sitemap_url)
            website_address = parsed_url.netloc
            output_filename = f"{website_address}_url_list.csv"

            # Display download links at the top and bottom
            st.markdown(f"### [Download CSV]({output_filename})")
            st.markdown("---")

            # Display the parsed URLs in a text box with a copy button
            st.subheader("Parsed URLs:")
            url_text = "\n".join(urls)
            st.code(url_text, language='http')

            # Display another download link at the bottom
            st.markdown("---")
            st.markdown(f"[Download CSV]({output_filename})")
        else:
            st.warning("No URLs found in the sitemap.")
