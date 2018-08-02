 
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
This is one of the basic elements we need when transforming files with XSLT language. 
```
<xsl:template match="tei:xx">
[template you need for the element]
</xsl:template>
```
`match="xx"` speicifies the elements for which this template should be used. You can also use `name="XX"` to spefcifies a name for this tmeplate, and invoke the template through `<xsl:call-template name="XX">`

#### `<xsl:apply-templates/>`
`<xsl:apply-templates select="xx"/>` element applies templates to the current element's child nodes. `selec="xx"` is optional. If you don't have it, it will apply templates of all child nodes to corresponded nodes. <br/>
If you specify  `select="xx"`, for example: 
```
  <xsl:template match="tei:p">
    <p>
      <xsl:apply-templates select="tei:persName"/>
    </p>
  </xsl:template>
```
This will only apply the template you defined to elements with `<persName>` tag inside `<p> and </p>`, other templates for other child nodes under `<p>` will not be applied.

#### `<xsl:text>`
`<xslt:text>` enables you to write text into your desired HTML files.
```
<xsl:text>
	your text
</xsl:text>
```
#### `<xsl:value-of select="xx"/>`
`<xsl:value-of select="xx"/>` extracts the value of a selected node. <br/>
For example, you have ` <persName key="jparr1">John Parrish</persName>` in an XML document,
transform.xslt :
```
<xsl:text> Name: </xsl:text>`<xsl:value-of select="persName" />`<br/>`<xsl:text> <br/> </xsl:text>`<br/>`<xsl:text> Person ID : </xsl:text>`<br/>`<xsl:value-of select="@key" />`| `Name: John Parrish`<br/>`Person ID: jparr1` 



#### `<xsl:attribute name="xx">`
```
 <xsl:attribute name="href">

        <xsl:text>#</xsl:text>
        <xsl:value-of select="@key" />
      </xsl:attribute>
 ```
#### Loop in XSLT
The tag for loop in XSLT is `<xsl:for-each select=EXPRESSION>`
