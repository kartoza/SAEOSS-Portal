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

# Documentation: Creating SuperUser

## Creating SuperUser from Terminal

To create a superuser, open the terminal.
Use the following command to add a superuser with the username `admin`:

```bash
docker exec -ti saeoss_ckan-web_1 poetry run ckan sysadmin add admin
```
- Replace `admin` with the desired username for the superuser.

![command](./img/super-user-1.png)

After running the command to add a superuser, the system typically asks for confirmation. Users are prompted to confirm whether they indeed want to create a superuser. The user is expected to input either `Y` for Yes or `n` for No based on their intention to create a superuser.

![confirmation](./img/super-user-2.png)

If the user chooses `Y` then they need to provide the email and password for the administrator account.

![required information](./img/super-user-3.png)

## Converting Normal User to SuperUser

Existing users can be elevated to superuser status through the terminal.
Use the following command, replacing <username> with the username of the registered user:

```bash
docker exec -ti saeoss_ckan-web_1 poetry run ckan sysadmin add <username>
```

![convert the normal user to a superuser](./img/super-user-4.png)

This command promotes the specified user to superuser status.

Before the superuser privileges

![Bob002 as a normal user](./img/super-user-5.png)

After the superuser privileges

![Bob002 as a superuser](./img/super-user-6.png)

**Important Notes:**

- Superusers have elevated privileges and can access and modify system-wide settings.
- Superusers can only be created via the terminal and not through the CKAN site.

**Important Security Considerations:**

- Superuser and super admin credentials should be kept secure.
- Regularly review and update superuser/admin credentials to enhance system security.
