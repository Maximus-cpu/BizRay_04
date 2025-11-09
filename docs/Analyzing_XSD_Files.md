- **Are blueprints or database schema's for XML files**
# Analyzing AllgemeineStruktur.xsd
- **The root of the whole schema with it "importing" 8 other xsd files with source**
#### Root => xs:schema
- targetNamesspace: all elements defined in the schema belong to this namespace
- XML files to be parse with this schema are expected to **declare the following** so that the elements match.
```xml
xmlns="https://finanzonline.bmf.gv.at/bilanz"
```
##### Includes => xs:includes
- This is the root schema, and in our case is pulled from 8 other .xsd files
- It is like using `import` in python
##### Elements => xs:element
- `xs:element name="ANZAHL"` here the XML tag would be `<ANZAHL></ANZAHL>`
- `<xs:element ref="INFO_DATEN" minOccurs="0"/>` 
	- Here the element is referring to a "INFO_DATEN" element defined somewhere else with the ref attribute
	- Here the `minOccurs="0"` means it is optional because the minimum occurrence is 0. You could have the `maxOccurs` attribute as well
##### Single Value => xs:simpleType
- `xs:simpleType` means it only holds a single value with no nested tags underneath
##### Simple Content => xs:simpleContent
Is content that is just text (string).
##### Restriction => xs:restriction
- `xs:restriction base="xs:positiveInteger"` it must be a positive integer
	- `xs:maxInclusive` determines a upper bound
	- `xs:minInclusive` determines a lower bound
##### Enumerations => xs:enumeration
Are allowed string or numeric values. Usually combined with `xs:restriction` to list possible allowed values
- `xs:enumeration value="FASTNR"`
*Ex:*
```xml
<xs:restriction base="xs:string">
  <xs:enumeration value="FASTNR"/>
</xs:restriction>
```
- Above a restriction of only strings is placed with a possible value being `FASTNR`
##### Referencing predefined types
Used to reference a type that is defined somewhere else for a new element
- `xs:element name="IDENTIFIKATIONSBEGRIFF type="fastnr"`
	- Here the type **fastnr** which is defined elsewhere is used
##### Complex elements => xs:complexType
Means the element has sub-elements and/or attributes
- `xs:complexType`
*Ex:*
```xml
<xs:element name="DATUM_ERSTELLUNG">
    <xs:complexType>
        <xs:simpleContent>
            <xs:extension base="xs:date">
                <xs:attribute name="type" type="datumtype" use="required"/>
            </xs:extension>
        </xs:simpleContent>
    </xs:complexType>
</xs:element>
```
##### Sequence => xs:sequence
Elements must appear in certain sequential order for the parent element defined with `xs:sequence`

##### Choice => xs:choice
One of several possible elements can appear in that position. Like using OR
```xml
<xs:choice>
  <xs:element ref="ALLG_FINANZ"/>
  <xs:element ref="ALLG_JUSTIZ"/>
</xs:choice>

```
- Above the xml can have **either**, but **not both** in that position
##### Attributes => xs:attribute
Defined inside of complex types
### XML Schema Reference Table
| Concept                                | Meaning / Description                                            | Example                                                    |
| -------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| **Namespace**                          | Unique identifier grouping XML elements; prevents name conflicts | `xmlns="https://finanzonline.bmf.gv.at/bilanz"`            |
| **Prefix**                             | Local alias for a namespace, used for readability                | `<xs:element>` where `xs` = schema namespace               |
| `<xs:element>`                         | Defines one XML tag (element)                                    | `<xs:element name="ANZAHL" type="xs:int"/>`                |
| `<xs:complexType>`                     | Element containing sub-elements and/or attributes                | `<Parent><Child/></Parent>`                                |
| `<xs:simpleType>`                      | Element containing only text (no sub-elements)                   | Numbers, strings, dates                                    |
| **simpleContent**                      | Text content with optional attributes                            | `<Date type="x">2025-11-04</Date>`                         |
| **complexType**                        | Nested structure combining sub-elements or attributes            | `<Parent><Child/></Parent>`                                |
| `ref=`                                 | References another element definition elsewhere in the schema    | `<xs:element ref="INFO_DATEN"/>`                           |
| **Schema attribute (e.g., ref, type)** | Instruction to the schema processor (not part of XML data)       | `<xs:element ref="INFO_DATEN"/>`                           |
| **Attribute (in XML instance)**        | Key=value metadata inside an XML tag                             | `<BILANZ_GLIEDERUNG ART="HGB">...</BILANZ_GLIEDERUNG>`     |
| **Attribute (in XSD)**                 | Defines XML attributes inside element definitions                | `<xs:attribute name="ART" use="required"/>`                |
| **use="required"**                     | Makes an attribute mandatory in the XML instance                 | Must appear in XML                                         |
| **include**                            | Imports definitions from another XSD file                        | `<xs:include schemaLocation="..."/>`                       |
| **sequence**                           | Ordered sub-elements — must appear in this order                 | `<xs:sequence> <A/> <B/> </xs:sequence>`                   |
| **choice**                             | One-of options — only one element may appear                     | `<xs:choice> <A/> <B/> </xs:choice>`                       |
| **minOccurs / maxOccurs**              | Cardinality — defines how many times an element can appear       | `minOccurs="0"` (optional), `maxOccurs="300"` (repeatable) |
| **Built-in base type**                 | Primitive data type predefined by XML Schema                     | `xs:string`, `xs:integer`, `xs:date`                       |
| **Restriction**                        | Narrows allowed values for a base type                           | Enumeration, numeric range, pattern, etc.                  |
| **Enumeration**                        | Restriction listing all allowed literal values                   | `<xs:enumeration value="FASTNR"/>`                         |
| **enumeration (in XML)**               | Fixes element or attribute value to a specific literal           | e.g. only `"HGB"` allowed                                  |
| **Element content**                    | What’s between `<Tag>` and `</Tag>` — text or nested XML         | Can be simple text or complex nested structure             |
# Analyzing HGBForm2XSD.xsd
- **Represents the balance sheet (Bilanz) / financial statements**

##### TLDR
| Code               | Legal section | Meaning                               | Data type                   |
| ------------------ | ------------- | ------------------------------------- | --------------------------- |
| **POSTEN**         | Generic type  | Simple numeric posting (amounts only) | decimal                     |
| **POSTEN_SPIEGEL** | Generic type  | Posting with mirror columns           | decimal + nested decimals   |
| **HGB_224_2_A**    | §224(2)A      | Assets                                | sequence of POSTEN_SPIEGEL  |
| **HGB_224_2_B**    | §224(2)B      | Liabilities & Equity                  | sequence of POSTEN_SPIEGEL  |
| **HGB_224_3**      | §224(3)       | Income-statement bridge               | sequence of POSTEN          |
| **FREI**           | optional      | Free / custom entries                 | same as POSTEN but optional |
##### HGB_Form_2
- **Top level (assets & liabilities)**

##### HGB_224_2
- **complex type** declaring the sequence of sub sections

| Element                                                  | Meaning (semantic)                                   | Likely Data Type                                 | Notes                                                   |
| -------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------- |
| **`HGB_Form_2`**                                         | Root of the balance sheet form                       | complexType (sequence of HGB_224_2 and children) | Contains the actual assets/liabilities hierarchy        |
| **`HGB_224_2`**                                          | Top-level for §224(2) – “Bilanzgliederung”           | complexType                                      | Parent node grouping all sub-sections                   |
| **`HGB_224_2_A`**                                        | “Aktiva” (Assets)                                    | complexType                                      | Split into A.I, A.II, A.III, etc.                       |
| **`HGB_224_2_B`**                                        | “Passiva” (Liabilities and Equity)                   | complexType                                      | Split into B.I, B.II, etc.                              |
| **`POSTENZEILE`**                                        | Numeric row entry                                    | complexType (decimal values)                     | Holds `BETRAG` and optional `BETRAG_VJ` (previous year) |
| **`BETRAG`**                                             | Value for the current year                           | xs:decimal                                       | May include fraction digits, typically 2                |
| **`BETRAG_VJ`**                                          | Value for the prior year                             | xs:decimal                                       | Optional, for comparison                                |
| **`SPIEGELWERTE`**                                       | Optional sub-columns (15 fields)                     | complexType                                      | Each `SPALTE_1`–`SPALTE_15` is xs:decimal               |
| **`SPALTE_1`–`SPALTE_15`**                               | Column data for sub-items or cross totals            | xs:decimal                                       | Represent detailed “mirror” breakdowns                  |
| **`HGB_224_2_A_I`, `HGB_224_2_A_II`, `HGB_224_2_A_III`** | Subsections of “Anlagevermögen” (A.I, A.II, etc.)    | complexType                                      | Contain their own POSTENZEILE + SPIEGELWERTE            |
| **`HGB_224_2_B_I`, `HGB_224_2_B_II`, etc.**              | Subsections under liabilities                        | complexType                                      | Similar structure to A.*                                |
| **`HGB_224_3`**                                          | Continuation for income-statement linkage (optional) | complexType                                      | May include additional POSTENZEILE                      |
| **`TEXT`** (in some variants)                            | Optional free text annotation                        | xs:string                                        | Rarely used in numeric forms                            |
##### HGB_224_2_A – _Aktiva (Assets)_
- **Represents the assets side of the balance sheet.**

**Contains:**
- **A.I Anlagevermögen (Fixed assets)**
    - intangible assets
    - tangible assets
    - financial assets
- **A.II Umlaufvermögen (Current assets)**
    - inventories
    - receivables
    - securities
    - cash
- **A.III Rechnungsabgrenzung (Prepaid expenses)**

Each of these sections has `<POSTENZEILE>` entries (POSTEN_SPIEGEL) with amounts for each line item.  
So you can think of this as the **left side of the balance sheet**.

##### HGB_224_2_B – _Passiva (Liabilities & Equity)_
- **Represents the liabilities and equity side of the balance sheet.**

**Includes**:
- **B.I Eigenkapital (Equity)**
    - capital, reserves, retained earnings
- **B.II Rückstellungen (Provisions)**
- **B.III Verbindlichkeiten (Liabilities)**
- **B.IV Rechnungsabgrenzung (Deferred income)**

Structured as nested posting lines (`POSTENZEILE`) using `POSTEN_SPIEGEL`.

> **A** = assets you own  
> **B** = where that money came from (equity or debt)

##### HGB_224_3 – _GuV (Profit and Loss linkage)_
- **This section transitions toward the income statement structure (GuV) in §224(3).**

**Includes:**
- **C. GuV Positionen** (e.g. revenues, expenses, net income) 
- The POSTENZEILEs here often mirror totals or aggregates that connect balance-sheet items to the profit and loss statement.

So `HGB_224_3` is essentially the **next layer** that continues the structure —  
while `HGB_Form_3` holds the full GuV form separately, `HGB_224_3` sometimes acts as the “bridge”.

##### Hierarchy

```less
BILANZ_GLIEDERUNG (ART="HGB")
│
├── ALLG_JUSTIZ
│   └── General info: FNR, company name, legal form, representatives
│
├── HGB_Form_2  (Balance Sheet)
│   ├── HGB_224_2  (Assets)
│   └── HGB_224_3  (Equity & Liabilities)
│
└── HGB_Form_3  (Notes / Anhang)
    ├── HGB_Form_3_5   → Explanations of special items (e.g. negative equity)
    ├── HGB_Form_3_16  → Average number of employees
    ├── HGB_Form_3_25  → Partner and profit allocation info
    └── ... other optional disclosures
```

**HGB_Form_2: Balance Sheet**
```less
HGB_Form_2  (Balance Sheet Form)
│
├── HGB_224_2  (Assets / Aktiva)
│   │
│   ├── POSTENZEILE              → Total Assets (Bilanzsumme)
│   ├── HGB_224_2_A              → Fixed Assets (Anlagevermögen)
│   │    ├── A.I  → Intangible assets
│   │    ├── A.II → Tangible assets
│   │    └── A.III → Financial assets
│   │
│   ├── HGB_224_2_B              → Current Assets (Umlaufvermögen)
│   │    ├── B.I  → Inventories
│   │    ├── B.II → Receivables and other assets
│   │    ├── B.III → Securities
│   │    └── B.IV → Cash and cash equivalents
│   │
│   ├── HGB_224_2_C              → Prepaid Expenses (Rechnungsabgrenzungsposten)
│   └── HGB_224_2_D              → Deferred Tax Assets (aktive latente Steuern)
│
└── HGB_224_3  (Equity & Liabilities / Passiva)
    │
    ├── POSTENZEILE              → Total Liabilities + Equity (must = Assets total)
    ├── HGB_224_3_A              → Equity (Eigenkapital)
    │    ├── A.I  → Subscribed capital
    │    ├── A.II → Capital reserves
    │    ├── A.III → Retained earnings
    │    ├── A.IV → Net income/loss for the year (Jahresüberschuss/-fehlbetrag)
    │
    ├── HGB_224_3_B              → Provisions (Rückstellungen)
    ├── HGB_224_3_C              → Liabilities (Verbindlichkeiten)
    ├── HGB_224_3_D              → Accruals / Deferred income (Rechnungsabgrenzungsposten)
    └── HGB_224_3_E              → Deferred tax liabilities (Passive latente Steuern)

```

(Comment => Is this meant to be for HGB_Form_3_5?)
**HGB_Form_3: General Notes**
```less
HGB_Form_3  (Notes / Anhang)
│
├── General information
│   ├── HGB_Form_3_1     → Accounting principles
│   ├── HGB_Form_3_2     → Changes in valuation methods
│   └── HGB_Form_3_3     → Depreciation, amortization
│
├── Explanations of balance sheet items
│   ├── HGB_Form_3_5     → Explanation of asset/liability structure
│   ├── HGB_Form_3_8     → Collateral, off-balance-sheet items
│   └── HGB_Form_3_9     → Events after reporting date
│
├── Disclosures on employees and management
│   ├── HGB_Form_3_16    → Average employees
│   ├── HGB_Form_3_19    → Management / supervisory board
│   ├── HGB_Form_3_20    → Branches
│   └── HGB_Form_3_22    → Dividend proposals
│
└── Partner and ownership structure
    ├── HGB_Form_3_25_1  → Partner identification
    ├── HGB_Form_3_25_2  → Amounts due to partners
    └── HGB_Form_3_25_3  → Profit/loss allocation
```