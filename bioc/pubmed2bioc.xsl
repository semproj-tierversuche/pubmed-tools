<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output indent="yes" method="xml"
		doctype-system="BioC.dtd" encoding="UTF-8" />
	<!--
		 this parameter should be set when performing the transformation.
		 The expected formatting is as follows:
		 `date +%Y%m%d`
	-->
	<xsl:param name="article-date" />
	<xsl:template match="/">
		<xsl:apply-templates select="/PubmedArticleSet/PubmedArticle" />
	</xsl:template>
	<xsl:template match="MedlineCitation">
		<xsl:element name="collection">
			<xsl:element name="source">
				<xsl:text>PubMed</xsl:text>
			</xsl:element>
			<xsl:element name="date">
				<xsl:value-of select="$article-date" />
			</xsl:element>
			<xsl:element name="key">
				<xsl:text>collection.key</xsl:text>
			</xsl:element>
			<xsl:element name="document">
				<xsl:call-template name="document" />
			</xsl:element>
		</xsl:element>
	</xsl:template>
	<xsl:template name="document">
		<xsl:element name="id">
			<xsl:value-of select="PMID" />
		</xsl:element>
		<xsl:element name="passage">
			<xsl:element name="infon">
				<xsl:attribute name="key">type</xsl:attribute>
				<xsl:text>title</xsl:text>
			</xsl:element>
			<xsl:element name="offset">
				<xsl:text>0</xsl:text>
			</xsl:element>
			<xsl:element name="text">
				<xsl:value-of select="Article/ArticleTitle" />
			</xsl:element>
		</xsl:element>
		<xsl:element name="passage">
			<xsl:element name="infon">
				<xsl:attribute name="key">type</xsl:attribute>
				<xsl:text>abstract</xsl:text>
			</xsl:element>
			<xsl:element name="offset">
				<xsl:value-of select="string-length(Article/ArticleTitle) + 1" />
			</xsl:element>
			<xsl:element name="text">
				<xsl:apply-templates select="Article/Abstract/AbstractText" />
			</xsl:element>
		</xsl:element>
	</xsl:template>
	<!--
		 This template matches sections from structured abstracts.
		 These have a set "Label" attribute.
	-->
	<xsl:template match="AbstractText[@Label]">
		<xsl:value-of select="@Label" />
		<xsl:text>: </xsl:text>
		<xsl:value-of select="." />
		<xsl:if test="position() != last()">
			<xsl:text> </xsl:text>
		</xsl:if>
	</xsl:template>
	<!-- This template matches for non-structured abstracts. -->
	<xsl:template match="AbstractText[not(@Label)]">
		<xsl:value-of select="." />
	</xsl:template>
	<!--
		 this empty template is required to remove extraneous text and
		 whitespace from the output. see
		 https://stackoverflow.com/questions/1468984
	-->
	<xsl:template match="text()" />
</xsl:transform>
