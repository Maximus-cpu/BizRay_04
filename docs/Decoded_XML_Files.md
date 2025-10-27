### Data Fields

##### General Legal and Company Data
- Company Classification (Ex: K = Kommanditgesellschaft)
```xml
<ALLG_JUSTIZ EINORDNUNG="K">
```
- Filing Entity
	- IBAN
	- BIC
```xml
<EB>
	<CODE>W804611</CODE>
	<NAME/>
	<BEZUG>STERNAD GESELLSCHAFT M.B.</BEZUG>
	<IBAN>AT304477032340020000</IBAN>
	<BIC>VBOEATWWGRA</BIC>
	<KUNDEN>000081206742</KUNDEN>
	<ZUSTELL>j</ZUSTELL>
</EB>
```
- Company Info
	- FNR
	- Company Name
```xml
<FIRMA>
	<FNR>000108i</FNR>
	<F_NAME>
		<Z>Sternad Gesellschaft m.b.H. Co KG</Z>
	</F_NAME>
</FIRMA>
```
- Financial Year
```xml
<GJ>
	<BEGINN>2017-01-01</BEGINN>
	<ENDE>2017-12-31</ENDE>
	<FORM>KG</FORM>
</GJ> 
```
- Previous Year
```xml
<VOR_GJ>
	<BEGINN>2016-01-01</BEGINN>
	<ENDE>2016-12-31</ENDE>
	<FORM>KG</FORM>
	<WERT_TSD>j</WERT_TSD>
</VOR_GJ>
```
- Currency
```xml
<WAEHRUNG>EUR</WAEHRUNG>
```
- Person submitting
```xml
<UNTER>
	<GEB_DAT>1982-07-31</GEB_DAT>
	<V_NAME>Peter</V_NAME>
	<Z_NAME>Sternad</Z_NAME>
	<DAT_UNT>2018-06-18</DAT_UNT>
	<REG_BEZ>F</REG_BEZ>
	<KOMP_NUM>070030k</KOMP_NUM>
	<KOMP_NAME>
		<Z>Sternad Gesellschaft m.b.H</Z>
	</KOMP_NAME>
</UNTER>
```

##### Firmenbuch ID's
- Official Firmenbuchnummer (FN) is managed by the Federal Ministry of Justice and this is for the **legal register**
	- FN 70030k
	- FN 108i
- FNR for Firmenbuchnummer inside of XML
	- 000108i

##### Balance Sheet Figures
```xml
<HGB_Form_2>
```
- Assets Section of Balance Sheet
```xml
<HGB_224_2>
```
- Liabilities + Equity
```xml
<HGB_224_3>
```