import pytest
from unittest.mock import MagicMock, call
import json
import legacy_functional_solution.insert_product
import logging

logging.basicConfig(level=logging.INFO)


# ---------- Sample product ----------
@pytest.fixture
def sample_product():
    return {
        "id": "ce4d8312-5175-467d-8eec-b323bfed23e9",
        "name": "Kawa ziarnista Arabica Palarnia Kawy Harmonia Kawa ziarnista Palarnia Kawy Harmonia waniliowa 1000 g",
        "category": {
            "id": "74035",
            "path": [
                {"id": "954b95b6-43cf-4104-8354-dea4d9b10ddf", "name": "Allegro"},
                {"id": "258832", "name": "Supermarket"},
                {"id": "73973", "name": "Produkty spożywcze"},
                {"id": "74030", "name": "Kawa"},
                {"id": "74035", "name": "Kawa ziarnista"},
            ],
            "similar": [
                {
                    "id": "251902",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "251902", "name": "Zestawy prezentowe"},
                    ],
                },
                {
                    "id": "261120",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "261120", "name": "Kawa bezkofeinowa"},
                    ],
                },
                {
                    "id": "261121",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "261121", "name": "Kawa zbożowa"},
                    ],
                },
                {
                    "id": "74824",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "74824", "name": "Kapsułki do ekspresów"},
                    ],
                },
                {
                    "id": "254546",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "254546", "name": "Kawa w saszetkach"},
                    ],
                },
                {
                    "id": "251906",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "251906", "name": "Kawa zielona"},
                    ],
                },
                {
                    "id": "261122",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "261122", "name": "Cold brew (parzona na zimno)"},
                    ],
                },
                {
                    "id": "261123",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "261123", "name": "Napoje kawowe"},
                    ],
                },
                {
                    "id": "74034",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "74034", "name": "Kawa rozpuszczalna"},
                    ],
                },
                {
                    "id": "74033",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "74033", "name": "Kawa mielona"},
                    ],
                },
                {
                    "id": "74032",
                    "path": [
                        {
                            "id": "954b95b6-43cf-4104-8354-dea4d9b10ddf",
                            "name": "Allegro",
                        },
                        {"id": "258832", "name": "Supermarket"},
                        {"id": "73973", "name": "Produkty spożywcze"},
                        {"id": "74030", "name": "Kawa"},
                        {"id": "74032", "name": "Cappuccino"},
                    ],
                },
            ],
        },
        "parameters": [
            {
                "id": "248811",
                "name": "Marka",
                "valuesLabels": ["Palarnia Kawy Harmonia"],
                "valuesIds": ["248811_2039670"],
                "values": "",
                "unit": "",
                "options": {"identifiesProduct": "true"},
            },
            {
                "id": "225693",
                "name": "EAN (GTIN)",
                "valuesLabels": ["5905386391122"],
                "values": ["5905386391122"],
                "unit": "",
                "options": {"identifiesProduct": "true", "isGTIN": "true"},
            },
            {
                "id": "221929",
                "name": "Waga",
                "valuesLabels": ["1000,000 g"],
                "values": ["1000.000"],
                "unit": "g",
                "options": {"identifiesProduct": "true"},
            },
            {
                "id": "224017",
                "name": "Kod producenta",
                "valuesLabels": ["PALARNIA KAWY HARMONIA"],
                "values": ["PALARNIA KAWY HARMONIA"],
                "unit": "",
                "options": {"identifiesProduct": "false"},
            },
            {
                "id": "128450",
                "name": "Gatunek kawy",
                "valuesLabels": ["Arabica"],
                "valuesIds": ["128450_1"],
                "values": "",
                "unit": "",
                "options": {"identifiesProduct": "false"},
            },
            {
                "id": "247497",
                "name": "Kraj pochodzenia",
                "valuesLabels": ["Brazylia"],
                "valuesIds": ["247497_1"],
                "values": "",
                "unit": "",
                "options": {"identifiesProduct": "false"},
            },
            {
                "id": "128453",
                "name": "Wielkość opakowania (g)",
                "valuesLabels": ["1000 g"],
                "valuesIds": ["128453_6"],
                "values": "",
                "unit": "",
                "options": {"identifiesProduct": "false"},
            },
            {
                "id": "24028",
                "name": "Rodzaj",
                "valuesLabels": ["kawa czarna aromatyzowana"],
                "valuesIds": ["24028_2"],
                "values": "",
                "unit": "",
                "options": {"identifiesProduct": "false"},
            },
            {
                "id": "250240",
                "name": "Nazwa handlowa",
                "valuesLabels": [
                    "inna (Kawa ziarnista Palarnia Kawy Harmonia waniliowa)"
                ],
                "valuesIds": ["250240_1818933"],
                "values": ["Kawa ziarnista Palarnia Kawy Harmonia waniliowa"],
                "unit": "",
                "options": {"identifiesProduct": "false"},
            },
        ],
        "images": [
            {
                "url": "https://a.allegroimg.com/original/11f209/c9a885f74ae7a554ee6619892d4e"
            },
            {
                "url": "https://a.allegroimg.com/original/11b922/1c62ce1e4e98815050b239efe68d"
            },
            {
                "url": "https://a.allegroimg.com/original/11f0da/80dc522e43e4ad32e7fad64a0d77"
            },
        ],
        "description": {
            "sections": [
                {
                    "items": [
                        {
                            "type": "TEXT",
                            "content": '<h1>KAWA HARMONIA "WANILIOWA" - 1 KG ziarnista</h1> <p><b>100% ARABIKA</b></p> <p>Kawa wyprodukowana ze świeżo palonych ziaren 100% Arabiki pochodzących z plantacji z Brazylii. Jest to jedna z najbardziej cenionych kaw na całym świecie. Przygotowana kompozycja wyselekcjonowanych ziaren Arabiki z dodatkiem smakowych nut WANILII tworzy wyjątkowy, niepowtarzalny smak i aromat.</p> <ul> <li>KOKOSOWA</li> <li>CZEKOLADOWA</li> <li>CZEKOLADOWO WANILIOWA</li> <li>ORZECHOWA</li> <li>… i wiele innych, w tej samej cenie.</li> </ul> <p>Aromaty smakowe zawierają wyciągi z naturalnych składników w tym cukry i tłuszcze. W zależności od poszczególnych smaków posiadają mniej lub bardziej skoncentrowaną oleisto-balsamiczną charakterystykę. Zaleca się zatem, aby wszystkie nasze kawy smakowe były zaparzane w sposób tradycyjny bądź alternatywnymi metodami po uprzednim zmieleniu ziaren na pożądaną grubość. Nie zalecamy mielenia w młynkach ekspresów automatycznych.</p> <p><b></b> Wszystkie nasze kawy są owocem wielu prób i testów przeprowadzanych wśród baristów oraz codziennych bywalców naszej firmowej kawiarni - zostały przetestowane na ekspresach ciśnieniowych kolbowych oraz automatycznych, a także jako zaparzane alternatywnymi metodami.</p>',
                        },
                        {
                            "type": "IMAGE",
                            "url": "https://a.allegroimg.com/original/11b922/1c62ce1e4e98815050b239efe68d",
                        },
                    ]
                },
                {
                    "items": [
                        {
                            "type": "TEXT",
                            "content": "<p><b>…. Z PASJI I MIŁOŚCI DO KAWY CZEKAJĄ NA WAS CIEKAWOSTKI ZE ŚWIATA NA TEMAT KAW.</b></p>",
                        }
                    ]
                },
            ]
        },
        "publication": {"status": "LISTED"},
        "aiCoCreatedContent": {"paths": []},
        "hasProtectedBrand": "false",
        "trustedContent": {"paths": [], "productPaths": []},
    }


# ---------- Mock the DB ----------
@pytest.fixture
def mock_db(monkeypatch):
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Patch globals in old_pipeline
    monkeypatch.setattr(
        legacy_functional_solution.insert_product, "cursor", mock_cursor
    )
    monkeypatch.setattr(legacy_functional_solution.insert_product, "conn", mock_conn)

    return mock_cursor, mock_conn


# ---------- Test the old pipeline ----------
def test_insert_product_old_pipeline(mock_db, sample_product):
    mock_cursor, mock_conn = mock_db
    logging.info("test")

    # Run legacy pipeline
    legacy_functional_solution.insert_product.insert_product(sample_product)
    logging.info("test")

    # Collect only cursor.execute calls
    execute_calls = [call for call in mock_cursor.mock_calls if call[0] == "execute"]

    # --- ASSERT PRODUCT INSERT EXISTS ---
    expected_values = (
        sample_product["id"],
        sample_product["name"],
        "LISTED",
        json.dumps(sample_product.get("description", {})),
        json.dumps([img["url"] for img in sample_product.get("images", [])]),
        sample_product["category"]["id"],
        "5905386391122",  # extracted EAN
    )

    product_insert_found = False

    for c in execute_calls:
        sql, params = c.args
        if sql.strip().startswith("INSERT INTO products"):
            assert params == expected_values
            product_insert_found = True
            break

    assert product_insert_found, "Product INSERT was not executed"

    # --- ASSERT PARAMETERS WERE INSERTED ---
    assert any(
        c.args[0].startswith("INSERT IGNORE INTO parameters") for c in execute_calls
    ), "Parameters were not inserted"

    # --- ASSERT PARAMETER VALUES WERE INSERTED ---
    assert any(
        c.args[0].startswith("INSERT IGNORE INTO parameter_values")
        for c in execute_calls
    ), "Parameter values were not inserted"

    # --- ASSERT PRODUCT ↔ PARAMETER MAPPING ---
    assert any(
        c.args[0].startswith("INSERT IGNORE INTO product_parameter_values")
        for c in execute_calls
    ), "Product-parameter mapping missing"

    # --- ASSERT COMMIT WAS CALLED ---
    mock_conn.commit.assert_called_once()

    # Optional: dump all parameter insert calls for comparison
    param_calls = [c for c in execute_calls]

    with open("old_calls.json", "w") as f:
        json.dump(param_calls, f, indent=2)

    logging.info("DB calls for old pipeline:", execute_calls)
