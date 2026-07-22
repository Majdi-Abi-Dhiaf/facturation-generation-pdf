from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from config import OUTPUT_DIR
from personalization import appliquer_personnalisation


def generate_quote_pdf(data: dict, filename: str = "devis.pdf") -> str:
    # Valide et traite le logo + les couleurs avant de les injecter dans le template
    perso = appliquer_personnalisation(
        logo_path=data.get("logo_path"),
        couleur_primaire=data.get("primary_color", "#1D9E75"),
        couleur_secondaire=data.get("secondary_color", "#333333"),
    )
    data = {**data, **perso}

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("devis.html")

    vat_rate = data.get("vat_rate", 0.20)
    subtotal = sum(item["qty"] * item["unit_price"] for item in data["items"])
    vat_amount = subtotal * vat_rate
    total_ttc = subtotal + vat_amount

    html_content = template.render(
        **data,
        subtotal=subtotal,
        vat_amount=vat_amount,
        total_ttc=total_ttc,
    )

    filepath = os.path.join(OUTPUT_DIR, filename)
    HTML(string=html_content).write_pdf(filepath)
    return filepath


if __name__ == "__main__":
    mock_data = {
        "company_name": "Atelier Bois & Co",
        "company_address": "12 rue des Artisans, 75011 Paris",
        "company_vat_number": None,
        "logo_path": None,
        "primary_color": "#1D9E75",
        "secondary_color": "#555555",
        "quote_number": "D-2026-0087",
        "quote_status": "En attente",
        "issue_date": "20/07/2026",
        "validity_date": "20/08/2026",
        "client_name": "Julie Marchand",
        "client_address": "Tunis, Tunisie",
        "intro_message": ("Merci pour votre demande. Voici notre proposition détaillée pour "
                           "la fabrication et la livraison de votre mobilier sur mesure."),
        "items": [
            {"description": "Table sur mesure chêne", "qty": 1, "unit_price": 450.00},
            {"description": "Livraison et installation", "qty": 1, "unit_price": 60.00},
        ],
        "vat_rate": 0.20,
        "payment_conditions": "30% d'acompte à la commande, solde à la livraison.",
        "acceptance_conditions": ("Ce devis est valable 30 jours à compter de sa date d'émission. "
                                   "Toute acceptation doit être formalisée par retour signé."),
        "legal_mentions": "TVA non applicable, art. 293B du CGI si franchise en base.",
    }

    path = generate_quote_pdf(mock_data)
    print(f"Devis généré : {path}")