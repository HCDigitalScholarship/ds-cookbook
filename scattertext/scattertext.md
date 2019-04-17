For any project with a large amount of text, we often want to visualize the differences between texts, between authors and so on.  We can create machine learning models that will categorize a text, but that often does not tell us what features that model learned to differentiate the two texts.  [Scattertext](https://github.com/JasonKessler/scattertext) offers a simple way to generate a visualization to explore the differences between texts and categories of texts.  Scattertext is build on spaCy and can be used with texts in any language supported by spaCy.  

In this tutorial, I will discuss how I have used scattertext to explore what lexical features distinguish Russian-language texts that were published in different journals.  The texts were scraped using scrapy and BeautifulSoup from the [Journal room](http://magazines.russ.ru/) website. 


