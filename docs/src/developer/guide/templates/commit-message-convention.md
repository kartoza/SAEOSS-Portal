

# Commit Message Convention
<!-- To Be Populated -->
When commiting changes to the platform informative commit messages are nessacerry to assist developers to easily review changes and speed up merging of pull requests once the yah been created. In this case all who contribute to the platform wheather through development or any additions to its features or information, the following commit message convention should be used:


### Message crop
Git automatically crops messages at 75 characters and the sunbject is capped at 50 characters. This is easlity viewed when using an IDE like `vs code` as the character cap changes color. What this means in simple terms is a message is only allowed to contain 75 characters per line. 

### Subject
When creating a commit message its important to give it a short decriptave subject. The subject should also be sparate from the body of the commit massage. This can be achieved by simply adding a blank line.

```
# Commit message subject
#
# Commit message body
```
### Message body
It is iportant to specify as much information in the body of the commit message as possible whilst being mindfule of the character limit imposed by Git. In this section elaborate on what the commit does: "Fix broken image links on index page" or "Implement proposed messiging system". In many cases the commit message should be the answer to this phrase: `When this commit is implemented then it will...`.

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
In cases where development should pass tests, the results therof shoudl be indicated where possible. This can also be indicated with Pull Requests.

```
# Ticket/183
# 
# Ensure metadata records are sans 1876 compliant.
# Test1: pass
```