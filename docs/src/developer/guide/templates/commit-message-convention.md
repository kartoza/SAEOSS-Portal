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

# Commit Message Convention
<!-- To Be Populated -->

When committing changes to the platform informative commit messages are necessary to assist developers to easily review changes and speed up merging of pull requests once the yah been created. In this case all who contribute to the platform whether through development or any additions to its features or information, the following commit message convention should be used:

### Message crop

Git automatically crops messages at 75 characters and the subject is capped at 50 characters. This is easily viewed when using an IDE like `vs code` as the character cap changes color. What this means in simple terms is a message is only allowed to contain 75 characters per line.

### Subject

When creating a commit message its important to give it a short descriptive subject. The subject should also be separate from the body of the commit massage. This can be achieved by simply adding a blank line.

```
# Commit message subject
#
# Commit message body
```
### Message body

It is important to specify as much information in the body of the commit message as possible whilst being mindful of the character limit imposed by Git. In this section elaborate on what the commit does: "Fix broken image links on index page" or "Implement proposed messaging system". In many cases the commit message should be the answer to this phrase: `When this commit is implemented then it will...`.

```
# Implement SANS 1876 standard 
# 
# Ensure new metadata records are compliant with the proposed standard.
```

### Related tickets

In many cases GitHub issues are more explanatory than the commit message. When possible ensure related tickets are linked either in the body or subject line of your commit message. This makes tracking issue fixes easier as ell as diagnosing future issues.

```
# Ticket/183
# 
# Ensure metadata records are sans 1876 compliant.
```

### Tests
In cases where development should pass tests, the results thereof should be indicated where possible. This can also be indicated with Pull Requests.

```
# Ticket/183
# 
# Ensure metadata records are sans 1876 compliant.
# Test1: pass
```
