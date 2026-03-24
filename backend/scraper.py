import requests
from bs4 import BeautifulSoup
import re
import json
import urllib3

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_wikipedia_mg(url):
    print(f"Fisintonana ny pejy: {url}...")

    # On simule un vrai navigateur (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # On ajoute les headers et on garde verify=False
        response = requests.get(url, headers=headers, verify=False, timeout=15)

        if response.status_code != 200:
            print(
                f"Erreur status: {response.status_code} (Blocage ou page inexistante)"
            )
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        # On cible le contenu principal pour éviter les menus
        content = soup.find(id="mw-content-text")
        if not content:
            return []

        paragraphs = content.find_all("p")
        text_content = " ".join([p.get_text() for p in paragraphs])

        # Nettoyage des mots (on garde les caractères malgaches)
        # Cette regex prend les mots d'au moins 2 lettres
        words = re.findall(r"\b[a-zàâéèêëîïôûù]{2,}\b", text_content.lower())
        return words

    except Exception as e:
        print(f"Erreur de connexion sur {url}: {e}")
        return []


# Liste d'URLs Wikipedia Malagasy
urls = [
    "https://teny-malagasy.akademia-malagasy.mg/index.php",
    "https://teny-malagasy.akademia-malagasy.mg/tantara.php",
    "https://teny-malagasy.akademia-malagasy.mg/matoanteny.php",
    "https://teny-malagasy.akademia-malagasy.mg/fifehezanteny.php",
    "https://teny-malagasy.akademia-malagasy.mg/feonteny.php",
    "https://teny-malagasy.akademia-malagasy.mg/fandrafetana.php",
    "https://mg.wikipedia.org/wiki/Fiteny_malagasy_%C3%B4fisialy",
    "https://mg.wikipedia.org/wiki/Fiteny_eto_Madagasikara",
    "",
]

dictionnaire_final = set()

for u in urls:
    mots = scrape_wikipedia_mg(u)
    if mots:
        dictionnaire_final.update(mots)
        print(f"-> {len(mots)} mots trouvés sur cette page.")

# Sauvegarde
if len(dictionnaire_final) > 0:
    with open("dictionnaire_mg.json", "w", encoding="utf-8") as f:
        json.dump(list(dictionnaire_final), f, ensure_ascii=False, indent=4)
    print(
        f"\nVita! Teny miisa {len(dictionnaire_final)} no voatahiry ao amin'ny dictionnaire_mg.json"
    )
else:
    print("\nKely loatra ny teny azo. Hamarino ny fifandraisana.")
