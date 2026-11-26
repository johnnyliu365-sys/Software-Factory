# Release runbook: a version is never published twice

## The rule

A version number is never published twice. Once tag `plugin-vX.Y.Z` is pushed to the publication repository, any change to the published plugin tree ships as a new version. Before a publish, run `git ls-remote --tags https://github.com/johnnyliu365-sys/software-factory-plugin.git "refs/tags/plugin-v*"`: it must list no `refs/tags/plugin-vX.Y.Z` for the new version, and the new version must be greater, in semantic-version order, than every version it lists. If either check fails, HALT before the push. Tags are immutable as `doc/adr/ADR-20260823-018-version-specific-publication-tag-payloads.md` decides.

## The order

The steps of a release are in `modules/tickets/workflow-governance/71-publication-0-5.md`, in the paragraph that begins "**The release, after review approval**" (steps 1 to 9). This runbook copies none of them.

The publication commit of a release is the one the released ticket's 正式環境移植 SOP names, in place of ticket 71's, as ticket 80's SOP first did. The rule above is checked before step 3. Each push waits for the owner's confirmation.

## Before release

While the check above lists no tag for the version, the local candidate may be rebuilt under the same version. Every rebuild is reinstalled, and its cached copies are checked, as ticket 80 item 5 says (`modules/tickets/workflow-governance/80-lookup-through-the-index.md`).
