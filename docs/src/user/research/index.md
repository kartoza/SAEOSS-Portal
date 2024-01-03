# SANS 1878 research

> 6.1. Metadata shall be provided for geographic datasets and may, optionally, also be provided for aggregations of datasets, features and attributes of features.

## Core metadata elements

As described on _Table2 - Core metadata for geographic datasets_

| Element | Obligation and Condition | Exists in stock CKAN | Notes |
| ------- | ------------------------ | -------------------- | ----- |
| Dataset title | Mandatory | Yes |
| **Dataset reference date** | **Mandatory** | **No** | To be implemented |
| **Dataset responsible party** | **Mandatory** | **Yes*** | Need to make it mandatory |
| **Geographic location of the dataset** (by four coordinates or by geographic identifier) | **Mandatory** | **No** | (As seen on Annex D - Creating the South African community profile)<br /><br />To be implemented |
| **Dataset language** | **Mandatory** | **No** | To be implemented |
| **Dataset character set** | **Mandatory** | **No** | To be implemented |
| **Dataset topic category** | **Mandatory** | **No** | To be implemented |
| **Spatial resolution of the dataset** | **Mandatory** | **No** | (As seen on Annex D - Creating the South African community profile)<br /><br /administrator>To be implemented |
| **Abstract describing the dataset** | **Mandatory** | **Yes*** | Need to make it mandatory |
| **Distribution format** | **Mandatory** | **No** | To be implemented |
| Additional extent information for the dataset (vertical and temporal) | Optional | No |
| **Spatial representation type** | **Mandatory** | **No** | (As seen on Annex D - Creating the South African community profile)<br /<br />To be implemented |
| **Reference system** | **Mandatory** | **No** | (As seen on Annex D - Creating the South African community profile)<br /><br />To be implemented |
| **Lineage statement** | **Mandatory** | **No** |
| On-line resource | Conditional | Yes |
| Metadata file identifier | Mandatory | Yes |
| Metadata standard name | Conditional | **No** | To be implemented |
| Metadata standard version | Conditional | **No** | To be implemented |
| **Metadata language** | **Mandatory** | **No** | To be implemented |
| **Metadata character set** | **Mandatory** | **No** | To be implemented |
| Metadata point of contact | Mandatory | Yes |
| Metadata date stamp | Mandatory | Yes |

### Additional elements

As found scattered throughout the SANS 1878 document

| Name | Obligation and condition | Notes |
| ---- | ------------------------ | ----- |
| **hierarchyLevel** | Mandatory | Unclear whether this should be implemented or not, as there is a question mark in the standard |
| **referenceSystemInfo** | Mandatory |
| metadataMaintenance | Optional |
| **purpose** | Mandatory |
| acknowledgement | Optional |
| **status** | Mandatory |
| resourceMaintenance | Optional |
| descriptiveKeywords | Optional |
| resourceSpecificUsage | Optional |
| graphicOverview | Optional |
| resourceConstraints | Optional | These are the constraints applicable to the resource. Can be defined as either LegalConstraints or SecurityConstraints, or both |
| MetadataConstraints | Optional | These apply to the metadata. Can be defined as either LegalConstraints or SecurityConstraints, or both |

## STAC API research

*STAC is a standardized way to expose collections of spatial temporal data. If you are a provider of data about the earth needing to catalog your holdings, STAC is driving a uniform means for indexing assets.*

At its core, the SpatioTemporal Asset Catalog (STAC) specification provides a common structure for describing and cataloguing spatio-temporal assets.

A spatio-temporal asset is any file that represents information about the earth captured in a certain space and time.

### The STAC Specification

The STAC Specification consists of 4 semi-independent specifications. Each can be used alone, but they work best in concert with one another.

- **STAC Item** is the core atomic unit, representing a single spatio-temporal asset as a GeoJSON feature plus datetime and links.

- **STAC Catalog** is a simple, flexible JSON file of links that provides a structure to organize and browse STAC Items. A series of best practices helps make recommendations for creating real world STAC Catalogs.

- **STAC Collection** is an extension of the STAC Catalog with additional information such as the extents, license, keywords, providers, etc that describe STAC Items that fall within the Collection.

- **STAC API** provides a RESTful endpoint that enables search of STAC Items, specified in OpenAPI, following OGC's WFS 3.

### Examples of STAC files

This JSON is what would be expected from an API that only implements STAC API - Core. It is a valid STAC Catalog with additional Links and a conformsTo attribute. In practice, most APIs will also implement other conformance classes, and those will be reflected in the links and conformsTo attribute. A more typical Landing Page example is in the overview document.

This particular catalog provides both the ability to browse down to child Catalog objects through its child links, and also provides the search endpoint to be able to search across items in its collections. Note that some of those links are not required and other servers may provide different conformance classes and a different set of links.

```
{
    "stac_version": "1.0.0",
    "id": "example-stac",
    "title": "A simple STAC API Example",
    "description": "This Catalog aims to demonstrate a simple landing page",
    "type": "Catalog",
    "conformsTo" : [
        "https://api.stacspec.org/v1.0.0/core"
    ],
    "links": [
        {
            "rel": "self",
            "type": "application/json",
            "href": "https://stac-api.example.com"
        },
        {
            "rel": "root",
            "type": "application/json",
            "href": "https://stac-api.example.com"
        },
        {
            "rel": "service-desc",
            "type": "application/vnd.oai.openapi+json;version=3.0",
            "href": "https://stac-api.example.com/api"
        },
        {
            "rel": "service-doc",
            "type": "text/html",
            "href": "https://stac-api.example.com/api.html"
        },
        {
            "rel": "child",
            "type": "application/json",
            "href": "https://stac-api.example.com/catalogs/sentinel-2"
        },
        {
            "rel": "child",
            "type": "application/json",
            "href": "https://stac-api.example.com/catalogs/landsat-8"
        }
    ]
}
```

*For more information about STAC please visit [https://github.com/radiantearth/stac-api-spec](https://github.com/radiantearth/stac-api-spec)*

## Upload Metadata

### Add Metadata via file upload

- Metadata can be added via file upload on the Metadata page (http://{sitename}/dataset/)
  - This supports xml, json and yaml files
![Upload Button]()

> *Please note the file needs to conform SANS 1878*

**Below is an example of mandatory fields in xml format**

```xml
<?xml version="1.0" encoding="UTF-8" ?>``
<dataset>
        <title>test 2</title>
        <MetadataStandardName>SANS1878</MetadataStandardName>
        <MetadataStandardVersion>1</MetadataStandardVersion>
        <notes>Abstract from the dataset</notes>
        <ResponsiblePartyIndividualName>Hugh Mann</ResponsiblePartyIndividualName>
        <ResponsiblePartyPositionName>Person</ResponsiblePartyPositionName>
        <ResponsiblePartyRole>Point of contact</ResponsiblePartyRole>
        <ResponsiblePartyElectronicMailAddress>example@example.com</ResponsiblePartyElectronicMailAddress>
        <IsoTopicCategory>society</IsoTopicCategory>
        <OwnerOrg>test</OwnerOrg>
        <private>False</private>
        <lineage_statement>test</lineage_statement>
        <spatial>-22.1265,16.4699,-34.8212,32.8931, -22.1265</spatial>
        <EquivalentScale>0</EquivalentScale>
        <SpatialRepresentationType>001</SpatialRepresentationType>
        <SpatialReferenceSystem>EPSG:4326</SpatialReferenceSystem>
        <ReferenceDate>2004-11-03T01:00:00</ReferenceDate>
        <ReferenceDateType>Publication</ReferenceDateType>
        <StampDate>2004-11-03T00:12:00</StampDate>
        <StampDateType>Creation</StampDateType>
        <DistributionFormatName>format name</DistributionFormatName>
        <DistributionFormatVersion>1.0</DistributionFormatVersion>
        <DatasetLanguage>english</DatasetLanguage>
        <MetadataLanguage>English</MetadataLanguage>
        <DatasetCharacterset>UCS-2</DatasetCharacterset>
        <MetadataCharacterset>UCS-2</MetadataCharacterset>
</dataset>
```

**Below is an example of mandatory fields in yaml format**

```yml
---
dataset:
  title: test-from-xml
  MetadataStandardName: SANS1878
  MetadataStandardVersion: 1
  notes: Abstract from the dataset
  ResponsiblePartyIndividualName: Hugh Mann
  ResponsiblePartyPositionName: Person
  ResponsiblePartyRole: Point of contact
  ResponsiblePartyElectronicMailAddress: example@example.com
  IsoTopicCategory: society
  OwnerOrg: kartoza
  private: False
  lineage_statement: test
  spatial: -22.1265,16.4699,-34.8212,32.8931, -22.1265
  EquivalentScale: 0
  SpatialRepresentationType: 001
  SpatialReferenceSystem: EPSG:4326
  ReferenceDate: 2004-11-03T01:00:00
  ReferenceDateType: Publication
  StampDate: 2004-11-03T00:12:00
  StampDateType: Creation
  DistributionFormatName: format name
  DistributionFormatVersion: 1.0
  DatasetLanguage: english
  MetadataLanguage: English
  DatasetCharacterset: UCS-2
  MetadataCharacterset: UCS-2
```

**Below is an example of mandatory fields in json format**

```json
{
  "dataset": {
    "title": "test-from-xml",
    "MetadataStandardName": "SANS1878",
    "MetadataStandardVersion": 1,
    "notes": "Abstract from the dataset",
    "ResponsiblePartyIndividualName": "Hugh Mann",
    "ResponsiblePartyPositionName": "Person",
    "ResponsiblePartyRole": "Point of contact",
    "ResponsiblePartyElectronicMailAddress": "example@example.com",
    "IsoTopicCategory": "society",
    "OwnerOrg": "kartoza",
    "private": "False",
    "lineage_statement": "test",
    "spatial": "-22.1265,16.4699,-34.8212,32.8931, -22.1265",
    "EquivalentScale": 0,
    "SpatialRepresentationType": 1,
    "SpatialReferenceSystem": "EPSG:4326",
    "ReferenceDate": "2004-11-03T01:00:00",
    "ReferenceDateType": "Publication",
    "StampDate": "2004-11-03T00:12:00",
    "StampDateType": "Creation",
    "DistributionFormatName": "format name",
    "DistributionFormatVersion": 1,
    "DatasetLanguage": "english",
    "MetadataLanguage": "English",
    "DatasetCharacterset": "UCS-2",
    "MetadataCharacterset": "UCS-2"
  }
}
```
