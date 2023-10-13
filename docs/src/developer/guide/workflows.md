# Developer Workflows

## Adding a Feature

- Create an Issue
- Wait for it to be added to a Sprint
- Functional Tests
- Playwright Tests
- Write end user documentation

## Fixing a Bug

- Claim an Issue
- Wait for it to be added to a Sprint
- Regression Test
- Implement Fix

## Creating Pull Requests

> **NOTE:** *Frequent PR's should be made to ensure quality of development. Read more on this later in the document.*

### Pull Request Workflow

#### 1. Fork the Repository

Follow the instructions for setting up a proper developer environment, which includes forking the repository.

#### 2. Clone the Repository

Clone the forked repository to your local machine using Git. This allows you to make changes to the code.

#### 3. Create a New Branch

Before making any changes, create a new branch for your feature or bug fix. This keeps your changes isolated from the main branch.

#### 4. Make and Commit Changes

 Make the necessary code changes in your local branch. Use Git to commit these changes with clear and descriptive commit messages.

#### 5. Push Changes to GitHub

Push your local branch with changes to your forked repository on GitHub.

#### 6. Open a Pull Request

Visit the original repository on GitHub, and GitHub will detect your recently pushed branch. Click on the "Compare & pull request" button.

#### 7. Resolving Conflicts

When conflicts are detected, GitHub will generate a message indicating that your pull request cannot be merged until all conflicts have been resolved. This message typically appears when the conflict is too intricate for GitHub's automatic conflict resolver to handle.

#### 8. Submitting Your Pull Request

Simply click the "Create pull request" button to submit your pull request. Your request will become visible to the repository's maintainers. It is their responsibility to review the code and merge your pull request into the main repository.

**Congratulations!** You've successfully created a pull request on GitHub, contributing your changes to the open-source project. Your code is now part of the main project for others to use and build upon.

## Frequent Pull Requests for Efficient Collaboration

Developers should embrace the practice of creating frequent pull requests (PRs) when working on a project for several compelling reasons. Here's why:

**Collaboration and Feedback:** Frequent PRs foster a culture of collaboration. They enable developers to share their work early and often with team members, facilitating peer review and feedback. This iterative process ensures that code changes align with project goals and coding standards and provides an opportunity for knowledge sharing among team members.

**Code Quality Assurance:** By making smaller, incremental changes through frequent PRs, developers can identify and rectify issues more easily. This proactive approach to code review helps catch bugs, improve code readability, and maintain a high level of code quality. It minimizes the risk of introducing complex and hard-to-fix issues that can arise from large, monolithic code changes.

**Continuous Integration:** Frequent PRs seamlessly integrate with continuous integration (CI) and continuous delivery (CD) workflows. CI systems can automatically build, test, and deploy changes submitted through PRs, ensuring that new code integrates smoothly with the existing codebase. This leads to a more stable and reliable project.

**Project Transparency:** Frequent PRs provide transparency into the development process. Team members, stakeholders, and project managers can easily track progress and stay informed about the latest changes. This transparency is especially valuable in agile and collaborative environments.

**Risk Mitigation:** Smaller, more frequent PRs help identify and mitigate potential risks early in the development cycle. If a particular PR introduces an issue, it's easier to identify the source and resolve it promptly, minimizing the impact on the overall project timeline.

In summary, creating frequent pull requests is a best practice that enhances collaboration, code quality, and project efficiency. It's a fundamental approach that not only helps developers work more effectively but also contributes to the success of the entire project.

### Committing To Project

Follow our [commit message conventions](./templates/commit-message-convention.md).

### Pull Request Template

If it has related issues, add links to the issues(like `#123`) in the description.
Fill in the [Pull Request Template](./templates/pull-request-template.md) by check your case.

<!-- List all developer workflows here improve this whole page -->

## How to Open Issues and Create Pull Requests on GitHub

![GitHub Logo](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png){: style="height:60px"}

When contributing to the development of the platform, it's **essential** to adhere to the correct workflow guidelines. Begin by configuring your [IDE](../../developer/guide/ide-setup.md) and [developer environment](../../developer/guide/building.md) and familiarizing yourself with the approved [coding standards](../manual/coding-conventions.md). Following the proper workflow guarantees high-quality development and strict adherence to endorsed code standards.
