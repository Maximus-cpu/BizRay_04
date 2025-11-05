### Analyzing the File with FNR: 122f
- **File Name:** dec_000122_5690241110320_000___000_30_3995576_XML.json
- **Data format was converted to Json for easier reading**
##### TLDR
|Section|Purpose|Real-world analogy|
|---|---|---|
|`INFO_DATEN`|Metadata about the **submission**|“Header info” of the filing|
|`BILANZ_GLIEDERUNG`|Contains the **financial report content**|The actual annual statement|
|`ALLG_JUSTIZ`|General company information|“Company master data”|
|`FIRMA`, `FNR`|Company identification|Legal name and register ID|
|`HGB_Form_2`|Balance sheet (assets/liabilities)|“Bilanz”|
|`HGB_Form_3`|Income statement (revenues/expenses)|“GuV”|
|`BETRAG`, `BETRAG_VJ`|Financial amounts|Current year / previous year|
|`SPIEGELWERTE`|Detailed breakdown per column|Used for cross-section totals

##### INFO_DATEN
```json
"INFO_DATEN": {
  "ART_IDENTIFIKATIONSBEGRIFF": "FASTNR",
  "IDENTIFIKATIONSBEGRIFF": "900985706",
  "PAKET_NR": 1477,
  "DATUM_ERSTELLUNG": {"@type": "datum", "$": "2011-08-25"},
  "UHRZEIT_ERSTELLUNG": {"@type": "uhrzeit", "$": "14:56:17"},
  "ANZAHL": 1
}
```

- This is all FinanzOnline-layer metadata, not company data.

| Field                                     | Meaning                                  | Notes                                    |
| ----------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `ART_IDENTIFIKATIONSBEGRIFF`              | Type of identifier                       | “FASTNR” = FinanzOnline tax-side number  |
| `IDENTIFIKATIONSBEGRIFF`                  | The actual identifier (here `900985706`) | Unique for the submitting entity         |
| `PAKET_NR`                                | Submission / package number              | Each upload gets a new PaketNr           |
| `DATUM_ERSTELLUNG` / `UHRZEIT_ERSTELLUNG` | Timestamp of XML creation                | “type” attributes describe the data type |
| `ANZAHL`                                  | Number of balance sheets in this package | Typically `1`                            |
##### BILANZ_GLIEDERUNG
```json
"BILANZ_GLIEDERUNG": [
  {
    "@ART": "HGB",
    "ALLG_JUSTIZ": {...},
    "HGB_Form_2": {...},
    "HGB_Form_3": {...}
  }
]

```

| Key                        | Meaning                                                              |
| -------------------------- | -------------------------------------------------------------------- |
| `@ART`                     | Filing type (here “HGB” for Handelsgesetzbuch = commercial code)     |
| `ALLG_JUSTIZ`              | General company metadata                                             |
| `HGB_Form_2`, `HGB_Form_3` | Actual financial statement data (balance sheet and income statement) |
##### ALLG_JUSTIZ
**Company & Filing metadata**
```json
"ALLG_JUSTIZ": {
  "@EINORDNUNG": "K",
  "VERS": "3.23",
  "PRUEF": "...",
  "SOFTWARE": {"SOFT": "BMD", "SOFT_VERS": "2011.14.22.15"},
  "EB": {...},
  "JABFORM": {"HGBFORM": "UGB23"},
  "ABSCHLUSSART": "J",
  "FIRMA": {...},
  "GJ": {...},
  "VOR_GJ": {...},
  "WAEHRUNG": "EUR",
  "UNTER": [...]
}
```

| Field          | Meaning                                                     |
|----------------|-------------------------------------------------------------|
| `@EINORDNUNG`  | "K" = Kapitalgesellschaft (capital company)                 |
| `VERS`         | Version of schema used                                      |
| `PRUEF`        | Validation checksum for integrity                           |
| `SOFTWARE`     | Accounting software that produced the file (BMD, RZL, etc.) |
| `EB`           | "Einbringung" / Filing entity (contact/banking data)        |
| `JABFORM`      | Type of financial statement (`UGB23` = standard form)       |
| `ABSCHLUSSART` | Type of closing ("J" = Jahresabschluss, annual statement)   |
| `FIRMA`        | Company identification and name                             |
| `GJ`, `VOR_GJ` | Current and previous financial year periods                 |
| `WAEHRUNG`     | Currency                                                    |
| `UNTER`        | People responsible (managing director, owner, etc.)         |
##### FIRMA
**Company Info**
```json
"FIRMA": {
  "FNR": "000122f",
  "F_NAME": {"Z": ["Elektrotechnik Kappacher", "GmbH & Co KG"]}
}
```
- FNR: Firmenbuchnummer (Company Register Unique Number)
- F_NAME: Name of the Company

###### FNR vs FASTNR
| Code                          | Full Name               | Responsible Ministry                                          | Purpose                       |
| ----------------------------- | ----------------------- | ------------------------------------------------------------- | ----------------------------- |
| **FNR / Firmenbuchnummer**    | Company Register Number | **Justice Ministry (BMJ) (Responsible for Company Register)** | Legal company identification  |
| **FASTNR / Finanzamtsnummer** | Tax Office Number       | **Finance Ministry (BMF)**                                    | Tax and fiscal administration |
##### GJ / VOR_GJ
**Accounting Periods**
```json
"GJ": {"BEGINN": "2010-03-01", "ENDE": "2011-02-28", "FORM": "KG"}
"VOR_GJ": {"BEGINN": "2009-03-01", "ENDE": "2010-02-28", "FORM": "KG", "WERT_TSD": "j"}
```
- Current fiscal year vs previous one
- `WERT_TSD="j"` means the values are reported in **thousands** (TSD = Tausend).
##### HGB_Form_2 and HGB_Form_3 (Financial Data)
**Two balance sheet forms**

| Form           | Type                                                  | Content                   |
| -------------- | ----------------------------------------------------- | ------------------------- |
| **HGB_Form_2** | Balance sheet (*Bilanz*)                              | Assets, liabilities, etc. |
| **HGB_Form_3** | Income statement (*GuV - Gewinn und Verlustrechnung*) | Revenues, costs, profit   |
**Example**
```json
"HGB_224_2_A": {
  "POSTENZEILE": {
    "BETRAG": "1471189.76",
    "BETRAG_VJ": "1500",
    "SPIEGELWERTE": {...}
  },
  ...
}
```

| Key             | Meaning                                                       |
| --------------- | ------------------------------------------------------------- |
| `BETRAG`        | Current year value                                            |
| `BETRAG_VJ`     | Prior year value                                              |
| `SPIEGELWERTE`  | Cross-references (sub-columns used for comparative structure) |
| `SPALTE_1...15` | Column data for specific HGB/UGB line groupings               |
