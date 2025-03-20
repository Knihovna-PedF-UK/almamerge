import pandas as pd
# from pymarc import MARCReader
import pymarc
import xml.sax as sax
import sys

# Načtení MARCXML souboru a vytvoření hash tabulky
hash_table = {}  # Hash tabulka pro ukládání dat z MARCXML

def process_record(record):
    # Získání ID záznamu z pole 001
    record_id = record['001'].data if record['001'] else None
    print("Loading ID: ", record_id, type(record_id))
    print(record)

    if record_id:
        # Získání klíčových slov (pole 650)
        keywords = [field['a'] for field in record.get_fields('650')]

        # Získání vydavatele (pole 260 nebo 264)
        # publisher = record.get_fields("260", "264") 
        publisher = record.publisher
        # print("Publisher field: ", publisher_field)
        # publisher = publisher_field['b'] if publisher_field else None

        # Získání ISBN (pole 020)
        # isbn_field = record['020']
        # isbn = isbn_field['a'] if isbn_field else None
        isbn = record.isbn
        print("values: ", keywords, publisher, isbn)

        # Uložení dat do hash tabulky
        hash_table[record_id] = {
                'Keywords': ', '.join(keywords) if keywords else None,
                'Publisher': publisher,
                'ISBN': isbn
                }



def main(xlsx_file, marcxml_file, output_file):
    try:
        print(f"Načítání souboru {marcxml_file}...")
        pymarc.map_xml(process_record, marcxml_file)
        print("Zpracování MARCXML souboru...")
        # Načtení XLSX souboru
        print(f"Načítání souboru {xlsx_file}...")
        df = pd.read_excel(xlsx_file)

        # Inicializace nových sloupců
        df['Keywords'] = None
        df['Publisher'] = None
        df['ISBN'] = None



        # Aktualizace tabulky pomocí hash tabulky
        for index, row in df.iterrows():
            record_id = str(row['mms'])
            print("Record ID: ", record_id, type(record_id))
            if record_id in hash_table:
                print("Record ID found: ", record_id)
                df.at[index, 'Keywords'] = hash_table[record_id]['Keywords']
                df.at[index, 'Publisher'] = hash_table[record_id]['Publisher']
                df.at[index, 'ISBN'] = hash_table[record_id]['ISBN']

        # Převod sloupce mms na řetězec, abysme zabránili jeho zobrazení ve vědecké notaci
        df['mms'] = df['mms'].astype(str)
        # Uložení aktualizované tabulky
        df.to_excel(output_file, index=False)
        print(f"Úspěch: Aktualizovaná tabulka byla uložena do souboru {output_file}")

    except FileNotFoundError as e:
        print(f"Chyba: Soubor nebyl nalezen - {e}")
    except pd.errors.EmptyDataError:
        print("Chyba: Excel soubor je prázdný nebo neplatný.")
    except KeyError as e:
        print(f"Chyba: Chybějící sloupec v Excel souboru - {e}")
    except Exception as e:
        print(f"Chyba: Neočekávaná chyba - {e}")

if __name__ == "__main__":
    # Ověření počtu argumentů
    if len(sys.argv) != 4:
        print("Použití: python marc_xcel_sync.py <vstupní_xlsx> <vstupní_marcxml> <výstupní_xlsx>")
        print("Příklad: python marc_xcel_sync.py data.xlsx data.marcxml updated_data.xlsx")
        sys.exit(1)

    # Získání názvů souborů z příkazové řádky
    xlsx_file = sys.argv[1]
    marcxml_file = sys.argv[2]
    output_file = sys.argv[3]

    # Spuštění hlavní funkce
    main(xlsx_file, marcxml_file, output_file)
