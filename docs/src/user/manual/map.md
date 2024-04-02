---
title: SAEOSS Portal
summary: Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision-making.
    - Jeremy Prior
    - Juanique Voot
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/kartoza/SAEOSS-Portal
copyright: Copyright 2024, SANSA
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Map User Manual

This interface displays footprints of datasets in polygon format by displaying the boundary that is covered by the respective metadata record.
The user is provided with a visual map to interact with to understand the extent, location and number of spatial Earth Observation datasets available.

![Map](img/map-1.png)

These are some of the components found on the map tab:

1. **Right Arrow:** Users can view available metadata records by clicking on the `Right Arrow`. When the user clicks on this arrow, a side panel opens with the metadata record list and the search filter.

    ![Map](img/map-2.png)

    1. **Search filters:** This provides a casual graphical interface to explore individual metadata records to discover items of interest in terms of content, time and location. This is where users can search for metadata by keywords and date.

        ![searched by keyword](./img/map-3.png)

    2. **Date:** Users can search for metadata records by specifying the start and end dates. Users can enter the dates directly into the fields or use the calendar icon to select the start and end dates.

        ![searched by date](./img/map-8.png)

    3. **Metadata Record:** To visualise the geographical area associated with the `Metadata Record`, users can click on the metadata, triggering its display on the map.

        ![metadata on map](./img/map-9.png)

        1. **Highlighted Area:** The geographic area corresponding to the metadata is highlighted on the map, providing a visual reference for the user.

        2. **Data:** Users can obtain detailed information by clicking anywhere within the highlighted area. This action reveals specific data associated with the metadata, including:

            - DateTime
            - Description
            - Keyword
            - Name
        
        This detailed information provides insights into the metadata record, aiding users in understanding its specific attributes and content.

2. **Zoom functionality:** This allows users to zoom in and out on the map.
 
3. **Base map options:** This allows users to choose a specific base map.

![base map options](./img/map-10.png){: style="height:200px"}

1. **OpenStreetMap Street View:**

    ![OpenStreetMap Street View](./img/map-4.png)

    - Provides a traditional street map view.
    - Displays road networks, landmarks, and geographical features commonly found in urban and suburban areas.

2. **OpenStreetMap Hybrid View:**

    ![OpenStreetMap Hybrid View](./img/map-5.png)

    - Combines satellite imagery with street map information.
    - Offers a hybrid perspective, allowing users to see both the physical landscape and mapped infrastructure.

3. **OpenStreetMap Pioneer View:**

    ![OpenStreetMap Pioneer View](./img/map-6.png)
    
    - Designed for exploration and outdoor activities.
    - Highlights topographic details, terrain, and natural features, making it suitable for adventurous and nature-related mapping.

4. **OpenStreetMap Neighbourhood View:**

    ![OpenStreetMap Street View](./img/map-7.png)

    - Emphasises localised mapping for neighbourhood-level details.
    - Useful for focusing on smaller-scale features, such as streets, parks, and amenities within specific neighbourhoods or community areas.
