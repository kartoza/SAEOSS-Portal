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

# Sysadmin settings

Sysadmin settings are designed to provide administrator access to manage accounts, organisations, and datasets. Certain 
administration tasks are unavailable through the web UI but require access to the server where CKAN is installed. 
This manual covers the administration features in the web UI.

![sysadmin settings](./img/sysadmin-settings-1.png)

1. Click on the `Sysadmin settings` option to have control of CKAN's instance. 

![sysadmin settings](./img/sysadmin-settings-2.png)

    
## Sysadmins

The first tab, `Sysadmin`, has the list of all sysadmin users. By clicking on one user, the administrator can manage 
the user account as if it were in the [profile](profile.md).

![sysadmin settings](./img/sysadmin-settings-3.png)


## Config

The second tab, `Config`,  is a page where the administrator can change some configurations from the web interface. 
It is a simple interface to quickly customise the `look and feel` of CKAN.

![sysadmin settings](./img/sysadmin-settings-4.png)


## Trash

The third tab, `Trash`, is a page that shows all deleted datasets, organisations, and groups. It allows the 
administrator to delete them permanently.

![sysadmin settings](./img/sysadmin-settings-5.png)

1. **Purge all**: To remove permanently all deleted datasets, organisations, and groups.
2. **Purge**: To remove permanently all deleted metadata records
3. **Purge**: To remove permanently all deleted organisation
