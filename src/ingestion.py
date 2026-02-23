import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from docx import Document


def fetch_url(url: str) -> str:
    """Fetch a URL and return clean text content."""

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchAssistant/1.0)"
    }

    response = requests.get(url, headers=headers, timeout=10)
    # now response contains HTML content,Status code, Headers, Everything returned by the server

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # tag.decompose() completely removes the tag and its contents from the page.
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # soup.get_text() pulls out all visible text from the HTML
    # separator="\n" → Adds a newline between elements
    text = soup.get_text(separator="\n")

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    clean_text = "\n".join(line for line in lines if line)

    return clean_text

def extract_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    # reader.pages becomes a list of all pages in the PDF.
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()

def extract_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()

def load_text(source: str) -> str:
    """Accept either a URL or raw pasted text."""
    if source.startswith("http://") or source.startswith("https://"):
        print("Fetching URL...")
        return fetch_url(source)
    else:
        return source


def load_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)  # function to be defined soon
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)  # function to be defined soon
    else:
        return open(file_path, "r").read()
