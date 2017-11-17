<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.w3.org/1999/xhtml">
	<xsl:output method="text" />
		<xsl:template match="/">
			<xsl:apply-templates select="/PubmedArticleSet/PubmedArticle" />
		</xsl:template>
		<xsl:template match="MedlineCitation">
			{
				"PMID": <xsl:value-of select="PMID" />,
				"Title": "<xsl:value-of select="Article/ArticleTitle" />",
				"Authors": [
				<xsl:apply-templates select="Article/AuthorList" />
				],
				"Date": "<xsl:apply-templates select="Article//PubDate" />",
				"Journal": [
				<xsl:apply-templates select="Article/Journal" />
				],
				"Link": "https://www.ncbi.nlm.nih.gov/pubmed/<xsl:value-of select="PMID" />",
				"Keywords": [],
				"Identifier": [],
				"Annotations": [],
				"Suggest": "",
				"Abstract": [
				<xsl:apply-templates select="//AbstractText" />
				],
				"PublicationType": "<xsl:value-of select="//PublicationType[1]" />",
				"Substances": [],
				"MeshHeadings": [
				<xsl:apply-templates select="//MeshHeading" />
				],
				"TextminingVersion": "0"
			}
		</xsl:template>
		<xsl:template match="AuthorList">
			<xsl:for-each select="Author">
				<xsl:text>"</xsl:text>
				<xsl:value-of select="LastName" />
				<xsl:text>, </xsl:text>
				<xsl:value-of select="ForeName" />
				<xsl:text>"</xsl:text>
				<xsl:if test="position() != last()">, </xsl:if>
			</xsl:for-each>
		</xsl:template>
		<xsl:template match="PubDate">
			<xsl:value-of select="Year" />
		</xsl:template>
		<xsl:template match="Journal">
			<xsl:text>"</xsl:text>
			<xsl:value-of select="Title" />	
			<xsl:text>"</xsl:text>
			<xsl:if test="position() != last()">, </xsl:if>
		</xsl:template>
		<xsl:template match="AbstractText">
			<xsl:text>"</xsl:text>
			<xsl:value-of select="." />
			<xsl:text>"</xsl:text>
			<xsl:if test="position() != last()">, </xsl:if>
		</xsl:template>
		<xsl:template match="MeshHeading">
			<xsl:text>"</xsl:text>
			<xsl:value-of select="DescriptorName" />
			<xsl:text>"</xsl:text>
			<xsl:if test="position() != last()">, </xsl:if>
		</xsl:template>
		<xsl:template name="date">
			<xsl:element name="div">
				<xsl:attribute name="class">
					<xsl:value-of select="local-name()" />
					<xsl:text> date</xsl:text>
				</xsl:attribute>
				<span class="day"><xsl:value-of select="Day" /></span>
				<span class="month"><xsl:value-of select="Month" /></span>
				<span class="year"><xsl:value-of select="Year" /></span>
			</xsl:element>
		</xsl:template>
		<xsl:template match="PublicationType">
			<span class="PublicationType"><xsl:value-of select="." /></span>
		</xsl:template>
		<xsl:template match="MedlineJournalInfo">
			<span class="Country"><xsl:value-of select="Country" /></span>
		</xsl:template>
		<xsl:template match="text()" />
</xsl:transform>