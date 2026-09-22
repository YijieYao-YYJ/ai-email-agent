import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=api_key)

email = """
Hallo,

meine Bestellung 12345 ist seit einer Woche
noch nicht angekommen. Können Sie bitte prüfen,
wo sich mein Paket befindet?

Viele Grüße
Max
"""

response = client.interactions.create(
    model="gemini-3.6-flash",
    input=f"""
Analysiere die folgende Kunden-E-Mail.

Bestimme:
- Kategorie
- Bestellnummer
- Sprache
- Dringlichkeit

E-Mail:
{email}
"""
)

print(response.output_text)