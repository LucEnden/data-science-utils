# Release Workflows

This document outlines the release workflows used in this project. These workflows, implemented using GitHub Actions, automate the process of versioning, bundling, and releasing the project. The workflows are triggered under specific conditions, and they follow semantic versioning. They where created such that any changes made are automatically available to the users of the project.

## Workflow: Create Minor or Patch Release

```mermaid
graph TD
  A[Push Event on main branch] -->|Ignore specific paths| B
  B[Run utils-updated job] -->|Checkout repository| C
  C[Check if utils are updated] -->|Determine changes in git_diff_tree.txt| D
  D[Process git_diff_tree.txt] -->|Check if utils changed| E
  E[No changes detected] -->|Skip creating release| END
  E[Changes detected] -->|Create intermediate release| F
  F[Run create-intermediate-release job] -->|Checkout repository| G
  G[Determine bump level] -->|Process git_diff_tree.txt| H
  H[Determine version bump] -->|Check changes in file structure| J
  J[Changes in file structure?] -->|Bump minor version| K
  K[Set version_bump to minor] -->|End| L
  J[Changes in file structure?] -->|Bump patch version| M
  M[Set version_bump to patch] -->|End| L
  L[Echo the bump level] -->|Get latest version tag| N
  N[Get latest tag] -->|Bump semver| O
  O[Bump semver] -->|Push new tag| P
  P[Push new tag] -->|Create Release| Q
  Q[Create Release] -->|Finish workflow| END
```

## Workflow: Create Major Release

```mermaid
graph TD
  A[Manual Workflow Dispatch] -->|Provide inputs| B
  B[Create Major Release job] -->|Checkout repository| C
  C[Get latest version tag] -->|Bump version to major| D
  D[Push new tag] -->|Create Release| E
  E[Use inputs for release body] -->|Finish workflow| F
  F[Create Release] -->|Finish workflow| END
```