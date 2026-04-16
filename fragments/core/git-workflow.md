## Git Workflow
- Never create commits on `main`, `master`, `develop`, or `staging` by default.
- If currently on one of those branches, warn the user and suggest creating a new branch.
- Direct commits on protected branches are allowed only when the user explicitly authorizes them for the current task, and only for small follow-up changes tightly coupled to work that has just been merged or released.
- Do not use the protected-branch exception for new feature work, broad refactors, or behavior changes that should receive their own branch lifecycle.
- Always ask the user to approve the commit message text before committing.
- Extract the SCM task id from branch names shaped as `<purpose>/<task_id>-<description>`.
- Use commit messages in the form `task_id. (commit_type) commit_message.`
