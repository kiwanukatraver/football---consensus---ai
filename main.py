from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

SITES = {
    "AI Football Predict": "https://aifootballpredict.com/",
    "Tips180": "https://www.tips180.com/",
    "OyaPredict": "https://oyapredict.com/"
}

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
    <body style="font-family:Arial;padding:20px">
    <h1>⚽ Football Consensus AI</h1>
    <p>Your three-source prediction comparison tool.</p>
    <button onclick="analyse()">Analyse Today's Matches</button>
    <pre id="result"></pre>
    <script>
    async function analyse(){
      document.getElementById('result').innerText='Checking sources...';
      let r=await fetch('/api/analyse');
      let d=await r.json();
      document.getElementById('result').innerText=
        JSON.stringify(d,null,2);
    }
    </script>
    </body>
    </html>
    """)

@app.get("/api/analyse")
def analyse():
    results = []

    for name, url in SITES.items():
        try:
            page = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            results.append({
                "source": name,
                "status": "Connected",
                "page": soup.title.get_text(strip=True)
                if soup.title else "No title"
            })

        except Exception as error:
            results.append({
                "source": name,
                "status": "Failed",
                "error": str(error)
            })

    return {"sources": results}
