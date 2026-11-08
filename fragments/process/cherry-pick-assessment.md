## Cherry-pick Assessment

Selective commit transfer between long-diverged branches is assessed before
it is executed; Git conflicts and a successful build do not prove dependency
completeness or semantic compatibility.

- A cherry-pick assessment resolves what to transfer — task ids, a merge
  request, a source branch, a range, explicit SHAs, or a mix — into an exact
  ordered SHA list itself, presents the resolved list with the target HEAD,
  and proceeds only after the user confirms it; silent truncation or widening
  of the candidate set is forbidden.
- The assessment is read-only: it never performs a recorded cherry-pick,
  resolves conflicts into the target, pushes, merges, rebases, or resets,
  and never modifies the user's working tree or remote systems; trial
  application only in a safe isolated throwaway tree.
- A verdict binds to the confirmed SHA set, its order, and the target HEAD;
  any change to those invalidates it. PASS admits to a controlled transfer,
  not a release; STOP and REVIEW are never downgraded to finish a task.
- When the `cherry-pick-assessment` skill is deployed, an assessment request
  goes through its selector resolution, confirmation, analyses A–F, and
  mandatory report shape.
