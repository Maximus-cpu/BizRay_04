### Are blueprints or database schema's for XML files

#### Root => xs:schema
- targetNamesspace: all elements defined in the schema belong to this namespace

XML files to be parse with this schema are expected to declare the following so that the elements match.
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
|Concept|Meaning / Description|Example|
|---|---|---|
|**Namespace**|Unique identifier grouping XML elements; prevents name conflicts|`xmlns="https://finanzonline.bmf.gv.at/bilanz"`|
|**Prefix**|Local alias for a namespace, used for readability|`<xs:element>` where `xs` = schema namespace|
|`<xs:element>`|Defines one XML tag (element)|`<xs:element name="ANZAHL" type="xs:int"/>`|
|`<xs:complexType>`|Element containing sub-elements and/or attributes|`<Parent><Child/></Parent>`|
|`<xs:simpleType>`|Element containing only text (no sub-elements)|Numbers, strings, dates|
|**simpleContent**|Text content with optional attributes|`<Date type="x">2025-11-04</Date>`|
|**complexType**|Nested structure combining sub-elements or attributes|`<Parent><Child/></Parent>`|
|`ref=`|References another element definition elsewhere in the schema|`<xs:element ref="INFO_DATEN"/>`|
|**Schema attribute (e.g., ref, type)**|Instruction to the schema processor (not part of XML data)|`<xs:element ref="INFO_DATEN"/>`|
|**Attribute (in XML instance)**|Key=value metadata inside an XML tag|`<BILANZ_GLIEDERUNG ART="HGB">...</BILANZ_GLIEDERUNG>`|
|**Attribute (in XSD)**|Defines XML attributes inside element definitions|`<xs:attribute name="ART" use="required"/>`|
|**use="required"**|Makes an attribute mandatory in the XML instance|Must appear in XML|
|**include**|Imports definitions from another XSD file|`<xs:include schemaLocation="..."/>`|
|**sequence**|Ordered sub-elements — must appear in this order|`<xs:sequence> <A/> <B/> </xs:sequence>`|
|**choice**|One-of options — only one element may appear|`<xs:choice> <A/> <B/> </xs:choice>`|
|**minOccurs / maxOccurs**|Cardinality — defines how many times an element can appear|`minOccurs="0"` (optional), `maxOccurs="300"` (repeatable)|
|**Built-in base type**|Primitive data type predefined by XML Schema|`xs:string`, `xs:integer`, `xs:date`|
|**Restriction**|Narrows allowed values for a base type|Enumeration, numeric range, pattern, etc.|
|**Enumeration**|Restriction listing all allowed literal values|`<xs:enumeration value="FASTNR"/>`|
|**enumeration (in XML)**|Fixes element or attribute value to a specific literal|e.g. only `"HGB"` allowed|
|**Element content**|What’s between `<Tag>` and `</Tag>` — text or nested XML|Can be simple text or complex nested structure|
### Next Prompts:

- Lets take this xml file and analyze how it matches the schema step by step