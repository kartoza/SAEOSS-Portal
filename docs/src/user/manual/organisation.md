---
title: SAEOSS Portal
summary: Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision-making.
    - Jeremy Prior
    - Juanique Voot
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/SANSA-EO/SAEOSS-PORTAL
copyright: Copyright 2024, SANSA
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Organisations

Users can view all the organisations on the platform on this page. Users with administrative rights for certain organisations are able to manage the organisation from this page. Additionally, if system administrators can add an organisations on this page.

![Organisations 1](./img/organisations-1.png)

## Organisation Home Page

Users can view an organisation's home page by clicking on an organisation on the `Organisations` page.

![Organisation Home Page 1](./img/organisation-home-page-1.png)

They will then be redirected to the organisation's home page. There are four main elements on an organisation's home page that all users can see:

1. **[The Overview](#overview)**
2. **[Metadata Records](#metadata-records)**
3. **[Activity Stream](#activity-stream)**
4. **[About](#about)**

Only the System Administrator and the Organisation's Publishers can see:

5. **[Manage Button](#manage-button)**

![Organisation Home Page 2](./img/organisation-home-page-2.png)

### Overview

The overview contains information regarding the organisation. This includes the organisation's profile picture, the organisation's name, a description of the organisation, the number of followers, the number of records, and the `Follow` button. The `Organisations` and `Tags` subsections, can be populated with reference links to keywords and organisations to filter the organisation's metadata records.

![Organisation Overview 1](./img/organisation-overview-1.png)

1. **Profile Picture:** This is an image (usually a logo) that is visually associated with the organisation.
2. **Organisation Name:** This is the name of the organisation.
3. **Description:** This is a short descriptor regarding the organisation (if provided).
4. **Number of Followers:** This is the number of users who follow the organisation.
5. **Number of Records:** This is the number of public records the organisation owns.
6. **`Follow` button:** This button allows users to follow the organisation and in turn receive notifications on their respective dashboards when there is activity from the organisation.

### Metadata Records

The `Metadata Records` section of an organisation's home page displays all of the organisation's public metadata records to all users.

![Organisation Metadata 1](./img/organisation-metadata-1.png)

If a user is a member, editor, or publisher (or system administrator) of the organisation then they will see all of the organisation's metadata records, including `Private` records.

![Organisation Metadata 2](./img/organisation-metadata-2.png)

1. **`Add metadata record` button:** Publishers and Editors within the organisation can see this button which allows them to add records to the organisation.
2. **Search bar and `Search` button:** All users can search for public records using the search functionality while organisation members, editors, and publishers can search for all the metadata records within the organisation.
3. **Metadata records:** These are the records that a user can see, either only the public, or all of the organisation's, records.

### Activity Stream

The `Activity Stream` section of an organisation's home page displays all of the activity related to the organisation, including members creating records, updates to the organisation, and more.

![Organisation Activity Stream 1](./img/organisation-activity-stream-1.png)

### About

The `About` section of an organisation's home page displays the full description about the organisation (if added) as some organisations may have longer descriptions that will not fully display in the overview panel.

![Organisation About 1](./img/organisation-about-1.png)

### Manage Button

If organisation users with the necessary permissions (publishers and the system administrator), click on the `Manage` button.

![Organisation Management 1](./img/organisation-managment-1.png)

This will redirect you to the management page of the organisation.

![Organisation Management 2](./img/organisation-managment-2.png)

#### Edit Details

The `Edit` tab allows users with the necessary permissions to change multiple details relating to the organisation. There is also the choice to update the organisation's details or to delete the organisation, utilising the relevant buttons at the bottom of the form.

![Organisation Management 3](./img/organisation-managment-3.png)

1. **Details:** These are fields that can be populated to change the organisation's displayed information in the [Overview](#overview) and [About](#about) sections.
2. **`Update Organisation` button:** This button stores changes made to the organisation's details.
3. **`Delete` button:** This button will delete organisation.

#### Manage Metadata Records

The `Metadata Records` tab allows users with the necessary permissions to add/delete, publish/unpublish, or search for the organisation's metadata records.

![Organisation Management 4](./img/organisation-managment-4.png)

1. **`Add metadata record` button:** This will redirect users to the [Add metadata](./metadata.md#add-metadata-record) form.
2. **Search bar and `Search` button:** Users can search for specific records with which they would like to interact.
3. **`Make public` button:** This button will "publish" a metadata record so that all users can see it.
4. **`Make private` button:** This button will "unpublish" a metadata record so that only the organisation's users can see it.
5. **`Delete` button:** This button will delete the metadata record from the organisation and the entirety of the platform.
6. **Checkboxes:** These allow users to select one, or many, metadata record(s) to perform an action on. The topmost checkbox will select all of the records.

#### Manage Members

The `Members` tab allows users with the necessary permissions to change other members' relative permissions within the organisation and to add new members to the organisation.

![Organisation Management 5](./img/organisation-managment-5.png)

1. **`Add Member` button:** This button redirects users to the [Add Member](#add-member) page.
2. **Number of members:** This displays the total number of members within the organisation.
3. **Table of users:** This table displays the organisation members and their respective roles.
4. **`Edit Member` button:** This button redirects users to the [Edit Member](#edit-member) page.
5. **`Delete Member` button:** This button causes the [Delete Member](#delete-member) popup to appear.

##### Add Member

The `Add Member` page allows users with the necessary permissions to add a current user on the platform to the organisation or to invite a new user to the platform and in turn the organisation. There is a description of the various user role permissions in the overview on the left.

![Organisation Management 6](./img/organisation-managment-6.png)

1. **Existing User:** This dropdown is where a current user's username should be entered.
    ![Organisation Management 7](./img/organisation-managment-7.png)
2. **New User:** This field is where a new user's email address should be entered.
    ![Organisation Management 8](./img/organisation-managment-8.png)
3. **Role:** The user's role (member, editor, or publisher) should be selected from this dropdown.
    ![Organisation Management 9](./img/organisation-managment-9.png)

##### Edit Member

The `Edit Member` page allows users with the necessary permissions to change a user's role within the organisation. There is a description of the various user role permissions in the overview on the left.

![Organisation Management 10](./img/organisation-managment-10.png)

1. **Role:** The user's role (member, editor, or publisher) should be selected from this dropdown.
    ![Organisation Management 9](./img/organisation-managment-9.png)
2. **`Update Member` button:** This button will commit the changes made to the member's role.
3. **`Delete` button:** This button will cause the [Delete Member](#delete-member) popup to appear.

##### Delete Member

The `Delete Member` popup prompts the user to confirm their action.

![Organisation Management 11](./img/organisation-managment-11.png)

1. **`Confirm` button:** This confirms the removal of the user from the organisation.
2. **`Cancel` button:** This cancels the action and closes the popup.

#### `View` Button

This button will redirect users back to the organisation's landing page.

![Organisation Management 12](./img/organisation-managment-12.png)
