<!-- ``` 
# Functionality

### Managing your profile

**Applicable roles:** All users are able to update their profile details.

To manage your account details, log in as normal, and you will be redirected to your dashboard. On this page, you will be able to view your activity and navigate to view the metadata you have created, organisations that you follow and groups that you are a member of. On the right-hand side of this page, you will see a green button, ‘Profile Settings’. Select this button to edit your account details.

![profile](img/profile-1.png)

Here you will be able to edit your contact information, affiliation, and occupation, and you will also have the option of changing your password.

![profile settings](img/profile-2.png)

### Managing non-owned profile

<b> Applicable roles</b>: System administrator and organisational publisher

To manage profiles belong to certain organisations as a system administrator or an organisational publisher, you need to navigate to the organisation and click 'Manage'

![manage organisation](img/manage-members-1.png)

Then click on the 'Members' tab.

![manage organisation](img/manage-members-2.png)

You can:

1. Add new members to the organisation.
2. Edit the member's role.
3. Remove the member from the organisation.

![manage members](img/manage-members-3.png)

### Search metadata

Users are able to search for metadata on the 'Metadata' tab. Depending on the user role, users can view public or private records. Users can search for data using different filters.

#### 1. Search metadata by Text

    <b>Applicable roles</b>: All

    Select 'Metadata' in the navigation bar, located horizontally at the top of the screen.

    ![search-text](img/search-text-1.png)
    You can use the search bar to look for specific metadata or you can filter through the results to find suitable records. To use the search bar, click on it and type in the term you are looking for. Click on the little magnifying glass located on the right-hand side of the search bar to see if any records match your search. 

    <b>Expected results</b>: Searching by title, abstract, or by a unique identifier in the search bar will yield results that meet the search criteria.

#### 2. Search metadata by Location

    <b>Applicable roles</b>: All

    You can filter the records by their spatial extent to find the records that you are looking for. You can search by location using three methods:
    1. Draw a grid: The pencil icon allows you to draw a rectangle over area of interest.
    2. Draw a radius: The circle icon allows you to search using proximity radius over area of interest.
    3. Select spatial layer: The layers icon allows you to select based on pre-existing boundary layers available on the system.

    ![search-location-functions](img/search-location-filters-1.png)
    
    
    To filter by drawing a grid, click on the little pen in the top right-hand corner of the map.

    ![search-location-pen](img/search-location-1.png)

    Use the plus and minus icons in the top right corner of the map to zoom in and out (1), and use your mouse to pan around the map canvas by clicking down and dragging your cursor (when it looks like a hand). Click on the pen icon (2) and drag your cursor over the area you are finding metadata for. You should see a red rectangle appear over that area (3). If you are not happy with the area, click on the little pen to re-draw a selection.If you are happy with the select, select 'Apply'(4)
    ![search-location-pen-2](img/search-location-2.png)

   To filter by proximity, click on the circle icon in the top right-hand corner of the map.

    ![search-location-circle](img/search-location-3.png)

    Use the plus and minus icons in the top right corner of the map to zoom in and out (1), and use your mouse to pan around the map canvas by clicking down and dragging your cursor (when it looks like a hand). Click on the circle icon (2) and drag from a point on the map. This will draw a buffer area around that point, based on a proximity radius. You should see a red circle appear over that area (3). If you are not happy with the area, click on the little pen to re-draw a selection.If you are happy with the select, select 'Apply'(4)
    
    ![search-location-circle-2](img/search-location-4.png) 

    To filter by spatial layers, click on the layers icon in the top right-hand corner of the map.
    ![search-location-layer](img/search-location-5.png)

    Select the spatial layer you want to apply

    ![search-location-layer-2](img/search-location-6.png) 

    This example chose the Provinces layer.

    ![search-location-layer-3](img/search-location-7.png) 

    Once you have chosen a desired layer, click on a spatial feature to set the search area (the example selects North West Province).
    Note: There is no apply button for this search functionality, clicking on a desired spatial feature automatically applies the filter.The search area will automatically resize to the bounding box of the spatial feature selected and all records that intersect with that particular spatial feature will be returned.

    ![search-location-layer-4](img/search-location-8.png) 

#### 3. Search metadata by Temporal range

        <b>Applicable roles</b>: All

        You can filter metadata records using atemporal range. Set the temporal range by selecting a start date, end date, or both a start and end date depending on the temporal extent of the record you are searching for.


        ![search-temporal](img/search-temporal-1.png)

        Click on the calendar icon, located on the right of the start and end date fields. To clear your results, select 'clear' and to set your extent to today's date, select 'today'.

        Please note that the calendar icon is not present in all browsers. In those browsers just click on the date fields and a calendar should appear where you can select a date.

        ![search-temporal-2](img/search-temporal-2.png)

#### 4. Search metadata by Organisation

        <b>Applicable roles</b>: All

        You can search for records by the organisations that published them. To do this, simply select the organisation or multiple organisations from whom you would like to view their records. To deselect the organisations, just click on the little 'x' that will appear next to a selected organisation.

        ![search-organisation](img/search-organisation-1.png)

        Click on the calendar icon, located on the right of the start and end date fields. To clear your results, select 'clear' and to set your extent to today's date, select 'today'.

        Note: As an anonymous user or a registered user who does not belong to the specific organisation you filtered by, you cannot see records that are private. This means that the number of records available may not be the number of records that appear.

#### 5. Search metadata by other filters

    The other filters include:

    1. Harvest source
    2. Featured metadata records
    3. Tags

    ![search-others](img/search-other-1.png)

### Save searches

<b>Applicable roles:</b> Registered users, organisational members, editors, publishers and system administrators.

Registered users can save search parameters in order to be able to reproduce a search query at a future date.

Navigate to 'Metadata' and select the desired filters. In the image below, the user searched by text, location and temporal range.

![save-searches](img/save-1.png)

Once you have your desired records on screen, click the 'Save' icon, which is to the right of the 'Search" icon, to save your search.

![save-search-icon](img/save-2.png)

Once you select it, the icon will be filled.

![save-search-icon-filled](img/save-3.png)

To view your saved search select 'Saved Search, which is located in the drop-down menu under your username, and it will direct you to your saved searches.

![view-saved-search-1](img/save-4.png)

![view-saved-search-2](img/save-5.png)

To reproduce a search, click on one of your previous searches and the site will automatically redirect you to the results for that search.

### Metadata capturing and publishing

#### Create metadata record in owned organisation using System UI

<b> Applicable roles</b>: Metadata editor, metadata publisher and system administrator

Method 1:

Navigate to 'Metadata' and select 'Add metadata record'.

![add metadata](img/metadata-system-ui-1.png)

This will take you to the form that needs to be completed in order to create metadata record.Fill in all the necessary information about the record. All fields marked with an asterisk (*) are mandatory. The information you add will become the information that is available on the site about the record you are adding.  When adding the metadata record thumbnail, make sure the image URL is a public image link and not a private one. Remember to also make sure that the image ratio is 1:1 for the best results.

![add metadata](img/metadata-system-ui-2.png)

Method 2:
Navigate to the organisation you belong to. You can do this by going to your profile and select 'Add metadata record' then fill out the form.

![add metadata](img/metadata-system-ui-3.png)

#### Create metadata record in owned organisation using XML upload

On the metadata page, select 'Add metadata record from xml file'.

![add metadata xml](img/metadata-xml-upload-1.png)

Then select the XML file on your local machine.

The xml file should look something like this:
![xml file standard](img/metadata-xml-upload-2.png)

#### Edit metadata record using system UI

Navigate to the record you want to edit and select 'manage'
```
-->