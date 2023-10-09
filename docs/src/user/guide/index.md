# Guide
<!-- List all of the Functionalities in BRIEF detail here. This serves as a reference guide where the user manual goes into GREAT detail -->

The guide section of the documentation provides short narrative / workflow based tutorials on the functionalities of the SAEOSS-Portal platform. The guide in intended to function as a collection of workflow based tutorials a user can follow to opbtain the nessacerry knowlege to perform mandated tasks. If you prefer a more detailed discription, you may prefer to work through our [User Manual](../manual/index.md) 

### Index:

**[Registering:](./registering.md)**  This page will show you how to register on the platform.
Help and Contact Pages: Here we explain how to get help with the platform, either from the documentation or through contacting the SAWPS team.
**[Functionality:](./functionality/index.md)** This section explains the various functionalities that can be performed on the site and what the required user roles are for those functionalities. This includes ,managing your profile, searching for metadata, saving searches, creating, editting and publishing metadata and managing organisational members.


### Error reporting:
We take pride and care to ensure our work is factual, accurate and informative. In the highly unlikely event that an error or bug is found please report it through one of the following channels:

<<<<<<< HEAD
**Github Issues:** Github is the prefered method of error reporting ensuring reported errors are addressed in the quickest turnaround time possible. [Read more...](../manual/opening_issues.md)
=======
- [**Upload Metadata**]()
- [**Adding a User to a Organisation**]()
  - [sub-Workflow]()
    - [sub-sub-Workflow]()
- [**Workflow**]()
- [**Workflow**]()
- [**Workflow**]()
- [**Workflow**]()

### Error repoting:
We take pride and care to esure our work is facutal, accurate and informative. In the highly unlikely event that and error or bug is found please report it through one of the following channels:


**Github Issues:** Github is the prefered method of error reporting ensuring reported errors are addressed in the quickest turnaround time possible. [Read more...](opening_issues.md)
>>>>>>> a5b7739a9c6953f9afff15481102ac8213a22f38

**Email:** Errors can be raised via email through the following channels. However this is not a recommended wpath as it has long turn around times.

<!-- we need permission to do this before implementing the mails

- info@kartoza.com
- example@sansa.cm
- exanple@saeonn.com -->
**Administrator:** Errors can be raised with your administrator if affiliated with an orgenisation. Administrators can escalate the the error to developers if required.

### Contributing:
If you would like to contribute to the documentation

## Upload Metadata

### Add Metadata via file upload

- Metadate can be added via file upload on the Metadata page (http://{sitename}/dataset/)
  - This supports xml, json and yaml files 
![Alt text](img/upload-btn.png)

*Please note the file needs to conform SANS 1878*

**Below is an example of mandatory fields in xml format**
```
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

```
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

```
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

