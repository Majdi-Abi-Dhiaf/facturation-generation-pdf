# Génération de Documents (PDF) — Logiciel de Facturation

Module de génération de documents PDF (factures, devis, factures d'avoir) pour un logiciel de facturation destiné aux indépendants, artisans et petites entreprises.

Ce module transforme des données structurées (fournies par le Backend) en documents PDF professionnels, personnalisables et légalement conformes.

## Stack technique

- **Python 3.12 (64-bit)**
- **Jinja2** — moteur de templates pour injecter dynamiquement les données dans le HTML
- **WeasyPrint** — conversion HTML/CSS → PDF

## Structure du projet

```
Génération de Documents (PDF)/
├── config.py                # Chemins et configuration (assets, output)
├── requirements.txt         # Dépendances Python
├── generate_invoice.py      # Script de génération de la facture PDF
├── test_pdf.py              # Script de test initial (validation de l'environnement PDF)
├── templates/
│   └── invoice.html         # Template HTML/CSS de la facture (placeholders Jinja2)
├── assets/
│   ├── fonts/                # Polices personnalisées (optionnel)
│   └── images/                # Logos, images utilisées dans les templates
├── output/                  # PDF générés (ignoré par Git)
└── venv/                    # Environnement virtuel (ignoré par Git)
```

## Installation

1. Cloner le repo :
```bash
git clone https://github.com/TON-USERNAME/facturation-generation-pdf.git
cd facturation-generation-pdf
```

2. Créer et activer un environnement virtuel (Python 64-bit requis) :
```bash
py -3.12 -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. **Windows uniquement** : WeasyPrint nécessite le runtime GTK3 (Pango, Cairo, GObject).
   Installer la version correspondant à l'architecture de ton Python (64-bit) :
   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

## Utilisation

Générer une facture de test avec des données mockées :
```bash
python generate_invoice.py
```

Le PDF est généré dans `output/facture.pdf`.

### Format des données attendu

```python
data = {
    "company_name": "Atelier Bois & Co",
    "company_siret": "123 456 789 00012",
    "company_address": "12 rue des Artisans, 75011 Paris",
    "logo_path": None,
    "primary_color": "#1D9E75",
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
    "legal_mentions": "En cas de retard de paiement...",
}
```

## Comment ça fonctionne

1. Le template `invoice.html` contient des placeholders Jinja2 (`{{ invoice_number }}`, `{{ client_name }}`, `{% for item in items %}`, etc.)
2. `generate_invoice.py` charge ce template, calcule les totaux (sous-total HT, TVA, total TTC), puis injecte les données réelles dans le HTML via Jinja2
3. WeasyPrint convertit le HTML/CSS final en fichier PDF

## État d'avancement

- [x] Configurer la bibliothèque de génération PDF (WeasyPrint + Jinja2, environnement 64-bit)
- [x] Créer le template de facture personnalisable
  - [x] Maquette HTML/CSS (logo, en-tête, tableau articles, totaux, pied de page)
  - [x] Placeholders dynamiques (`{{ numero_facture }}`, `{{ date }}`, `{{ montant_ht }}`, etc.)
  - [x] Test avec données d'exemple
- [ ] Créer le template de devis personnalisable
- [ ] Ajouter la personnalisation logos et couleurs (au-delà de `primary_color`)
- [ ] Intégrer les mentions légales par pays (via endpoint Backend)
- [ ] Développer le service de génération PDF générique (`generer_pdf(donnees, template_type, personnalisation)`)
- [ ] Implémenter la génération de factures d'avoir
- [ ] Écrire les tests unitaires et fonctionnels

## Notes techniques

- WeasyPrint sur Windows nécessite impérativement une correspondance d'architecture entre Python et le runtime GTK3 (32-bit avec 32-bit, 64-bit avec 64-bit), sous peine d'erreur `OSError: cannot load library 'libgobject-2.0-0'`.
- Le module est pensé pour être appelé directement par le Backend (fonction réutilisable), pas comme une interface utilisateur autonome.