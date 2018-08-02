 
This tutorial will cover some usages of XSLT language in transforming XML to HTML files including ***Loop*** in xslt. There are a lot more than I have known about XSLT and can cover here at this point. So, when you discover more about using XSLT, please add to this document.
Useful tutorials I have used are from [Moziila](https://developer.mozilla.org/en-US/docs/Web/XSLT) and [Microsoft](https://msdn.microsoft.com/en-us/library/ms256058(v=vs.110).aspx)
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
```
<xsl:text> Name: </xsl:text>
<xsl:value-of select="persName" />
<xsl:text> <br/> </xsl:text>
<xsl:text> Person ID : </xsl:text>
<xsl:value-of select="@key" />
```
HTML ouput:
```
Name: John Parrish
Person ID: jparr1
```
#### `<xsl:attribute name="xx">`
It ceates an attribute to an output element. The element must be defined be before. `<xsl:attribute name="xx">` is put inside the element, and no other output element can be included within this element, non-ouput elements link`</xsl:apply-templates/>` can be included.
```
<an element>
<xsl:attribute name="xx">
[template for the value of attribute you want to add to this element]
</xsl:attribute>
</xsl:apply-templates/>
</ end of this element>
```
For example, we can add an `href` attribute to a text and make in to a link in HTML output:
In an XML document, again, we have:` <persName key="jparr1">John Parrish</persName>`
`transform.xslt:`
```
<xsl:template match="tei:persName">
  <a id="person">
     <xsl:attribute name="href">
        <xsl:text>#</xsl:text>
	<xsl:value-of select="@key" />
     </xsl:attribute>
     </xsl:apply-templates/>
  </a>
</xsl:template>
 ```
 HTML output:
 ```
 <a id="person" href=#jparr1>John Parrish</a>
 ```
### Loop in XSLT
`<xsl:for-each select="XXX">` and `<xsl:for-each>` inform the start and end of a loop. `select="XXX"` is required to specifiy which elements to loop through. 
```
<xsl:for-each select=EXPRESSION>
	TEMPLATE
</xsl:for-each>
```
We also can get index numbers link `i` in Pytho ***for loop*** in XSLT. `<xsl:value-of select="position()"/>`gives the index number of a node in the loop. 
For example in an XML document you have:
```
<?xml version="1.0" encoding="UTF-8"?>
<persName>John</persName>
<persName>William</persName>
<persName>Joseph</persName>
...
```
XSLT code:
```
<xsl:template match="/">
<html>
<body>
   <xsl: for-each select="persName>
     <xsl:text>Person</xsl:text> 
     <xsl:value-of select="position()"/>
     <xsl:text>: </xsl:text>
     <xsl:value-of select="persName"/>
   </xsl: for-each>
</body>
</html>
</xsl:template>
```
**in `match="/"`, "/" denotes the root element**
HTML output:
```
Person1: John
Person2: William
Person3: Joseph
```
