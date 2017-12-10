The XSL transformation `pubmed2bioc.xsl` needs to be called with the
parameter `article-date` set to the date when the article was downloaded
from PubMed, in the format YYYYMMDD (ex. 20171210). An `xsltproc` commandline
that does this:

    xsltproc --nonet --path . --stringparam article-date `date +%Y%m%d` pubmed2bioc.xsl inputfile.xml

* `--nonet` disables the downloading of remote items like DTDs
* `--path .` tells the processor that the relevant DTD files are in the
  current directory
* ``--stringparam article-date `date +%Y%m%d` `` sets the parameter to the
  current date
* `pubmed2bioc.xsl` specifies the XSL transformation file to be used
* `inputfile.xml` is the file to be transformed
