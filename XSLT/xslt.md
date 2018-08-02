This tutorial will cover some usages of XSLT language in transforming XML to HTML files. There are a lot more than I have known about XSLT and can cover here at this point. So, when you discover more about using XSLT, please add to this document.
## Introduction for XSLT
Extensible Stylesheet Language Transformations (XSLT) is an XML-based language for transformation of XML documents. XML documents are both human-readable and machine-readable documents marked up based on a set of encoding rules. 
From my understanding, an XSLT file finds tags, and apply specific HTML templates to specific tags.

#### `<xsl: stylesheet>`
It is similar to `<html>` tag. It is required at the beginning and end of every XSLT file.
```
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:msxsl="urn:schemas-microsoft-com:xslt">
[EVERYTHING]
</xslt:stylesheet>
```
#### `<xsl:template>`
This is one of the basic elements we need in tranforming files with XSLT language. 
```
<xsl:template match="tei:xx">
[template you need]
</xsl:template>
```
#### `<xsl:apply-templates/>`


#### Loop in XSLT
The tag for loop in XSLT is `<xsl:for-each select=EXPRESSION>`
