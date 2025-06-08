# Website Scraper Frontend

A simple frontend interface for scraping website data. Users can input a URL, and the app fetches and displays:

- Word count
- Paragraph count
- Heading count (h1-h6)
- Link count
- Image count
- The first scraped table in a clean, responsive layout

---

## Features

- URL input with validation
- Loading indicator while fetching data
- Displays summary stats about the webpage content
- Renders the first available table with proper alignment and styling
- Handles tables with header/rows or arrays of objects
- Clean and responsive design with minimal dependencies (vanilla JS, HTML, CSS)

---

## Demo

![Demo Screenshot](screenshot.png)

---

## Getting Started

### Prerequisites

- A backend API that accepts POST requests at `/scrape` and returns JSON with the following fields:
  - `word_count`: number
  - `paragraph_count`: number
  - `heading_count`: number
  - `link_count` or `link_counts`: number or object
  - `image_count`: number
  - `tables`: array of table data, where each table can have:
    - `headers`: array of strings
    - `rows`: array of arrays or array of objects

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/website-scraper-frontend.git
   cd website-scraper-frontend
