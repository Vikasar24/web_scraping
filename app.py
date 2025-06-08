from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Fetch page content with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract full text and count words
        texts = soup.stripped_strings
        full_text = " ".join(texts)
        word_count = len(re.findall(r'\w+', full_text))

        # Count paragraphs and headings
        paragraph_count = len(soup.find_all("p"))
        heading_count = sum(len(soup.find_all(f"h{i}")) for i in range(1, 7))

        # Process links and categorize
        all_links = soup.find_all("a", href=True)
        internal_links, external_links, mailto_links, tel_links, other_links = [], [], [], [], []

        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc

        for a in all_links:
            href = a['href'].strip()
            if href.startswith("mailto:"):
                mailto_links.append(href)
            elif href.startswith("tel:"):
                tel_links.append(href)
            elif href.startswith("#") or not href:
                other_links.append(href)
            else:
                full_link = urljoin(url, href)
                link_domain = urlparse(full_link).netloc
                if link_domain == base_domain:
                    internal_links.append(full_link)
                else:
                    external_links.append(full_link)

        # Count images
        image_count = len(soup.find_all("img"))

        # Extract tables data
        tables_data = []
        for table in soup.find_all("table"):
            # Extract headers, if any
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            rows_data = []

            # Extract rows
            for row in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in row.find_all("td")]
                if cells:
                    # Map headers to cells if headers count matches cell count
                    if headers and len(headers) == len(cells):
                        rows_data.append(dict(zip(headers, cells)))
                    else:
                        rows_data.append(cells)

            tables_data.append({
                "headers": headers,
                "rows": rows_data
            })

        return jsonify({
            "word_count": word_count,
            "paragraph_count": paragraph_count,
            "heading_count": heading_count,
            "image_count": image_count,
            "link_counts": {
                "internal": len(internal_links),
                "external": len(external_links),
                "mailto": len(mailto_links),
                "tel": len(tel_links),
                "other": len(other_links)
            },
            "links": {
                "internal": internal_links,
                "external": external_links,
                "mailto": mailto_links,
                "tel": tel_links,
                "other": other_links
            },
            "tables": tables_data
        })

    except Exception as e:
        # Log the full traceback to the console for debugging
        print("ERROR:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
