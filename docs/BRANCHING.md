# Git and GitHub branching guide

Keep `main` deployable and use `develop` for integrated work. Create short-lived branches from `develop` using `feature/<topic>`, `fix/<topic>`, or `docs/<topic>`. Open a pull request back to `develop`, request review, and require the Jenkins verification stage before merging. Periodically merge `develop` to `main` for a reviewed release.

```sh
git switch -c develop
git push -u origin develop
git switch develop
git pull --ff-only
git switch -c feature/report-search
# implement a focused change
git add src
git commit -m "Add report search filters"
git push -u origin feature/report-search
```

Use pull requests for review and keep each commit focused. Protect `main` and `develop` with required status checks where the GitHub plan permits. Resolve conflicts locally, rerun `mvn clean verify`, then update the branch. Never commit `.env`, passwords, personal item data, or database volumes.
