# pubmed2json.xsl
* Only the Year is being put into the "Date" value, because the other fields
  are optional and I haven't written XSLT for that yet.
* An article can have multiple PublicationType entries in PubMed. The
  DB schema currently doesn't support this, so only the first entry is
  used.
* Structured abstracts are not yet fully supported.
* The `_escape` template should be applied to every string from the source XML. Also, the template should escape backslashes (`\`) into double-backslashes (`\\`).
