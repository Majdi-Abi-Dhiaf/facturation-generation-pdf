from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from config import OUTPUT_DIR
from personalization import appliquer_personnalisation


def generate_invoice_pdf(data: dict, filename: str = "facture.pdf") -> str:
    # Valide et traite le logo + les couleurs avant de les injecter dans le template
    perso = appliquer_personnalisation(
        logo_path=data.get("logo_path"),
        couleur_primaire=data.get("primary_color", "#1D9E75"),
        couleur_secondaire=data.get("secondary_color", "#333333"),
    )
    data = {**data, **perso}

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice.html")

    subtotal = sum(item["qty"] * item["unit_price"] for item in data["items"])
    vat_amount = subtotal * data["vat_rate"]
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
        "company_siret": "123 456 789 00012",
        "company_address": "12 rue des Artisans, 75011 Paris",
        "logo_path": None,
        "primary_color": "#1D9E75",
        "secondary_color": "#555555",
        "invoice_number": "F-2026-0142",
        "issue_date": "15/07/2026",
        "due_date": "14/08/2026",
        "client_name": "Julie Marchand",
        "client_address": "Tunis, Tunisie",
        "items": [
            {"description": "Table sur mesure chêne", "qty": 1, "unit_price": 450.00},
            {"description": "Livraison et installation", "qty": 1, "unit_price": 60.00},
        ],
        "vat_rate": 0.20,
        "legal_mentions": ("En cas de retard de paiement, une pénalité de 3 fois le taux "
                            "d'intérêt légal sera applicable. Indemnité forfaitaire de 40 € "
                            "pour frais de recouvrement."),
    }
    path = generate_invoice_pdf(mock_data)
    print(f"Facture générée : {path}")