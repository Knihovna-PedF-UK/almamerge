# almamerge

**almamerge** je nástroj pro propojení a aktualizaci dat mezi Excel tabulkou
(XLSX) a MARCXML souborem. Projekt slouží k doplnění bibliografických informací
(klíčová slova, vydavatel, ISBN) do Excel tabulky na základě odpovídajících
záznamů v MARCXML souboru.

---

## Funkce

- Načte data z Excel tabulky (XLSX) a MARCXML souboru.
- Propojí záznamy podle ID (pole `001` v MARCXML a sloupec `mms` v XLSX).
- Doplní do Excel tabulky nové sloupce:
  - **Keywords**: Klíčová slova z pole `650` v MARCXML.
  - **Publisher**: Vydavatel z pole `260` nebo `264` v MARCXML.
  - **ISBN**: ISBN z pole `020` v MARCXML.
- Uloží aktualizovanou tabulku do nového XLSX souboru.

---

## Požadavky

Pro spuštění projektu je potřeba mít nainstalovaný Python 3 a následující knihovny:

- `pandas`
- `pymarc`
- `openpyxl`

Knihovny nainstalujete pomocí příkazu:

```bash
$ pip install pandas pymarc openpyxl
```

## Spuštění

```bash 
$ python merge.py ~/Stažené/pujcovanost_tituly_2025_02.xlsx ~/Stažené/BIBLIOGRAPHIC_24798032960006986_24798032940006986_1.xml ~/Stažené/pujcovanost_tituly_updated.xlsx
```


