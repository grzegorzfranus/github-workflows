# Release Template

This template defines the standard structure for all GitHub Releases in this project.
When drafting a new release, copy the contents of this template, fill in the placeholders, and use it as the release description.

---

# v[X.Y.Z]
Release v[X.Y.Z] — [One-line summary of the main feature/theme]

**Date:** [YYYY-MM-DD]  
**Scope:** [Affected workflows, e.g. github-workflows/ci]  
**Release type:** [Major / Minor / Patch] ([brief reason, e.g., security hardening, bug fixes])  

## 🧭 Summary
[Provide a brief 1-2 paragraph description of the release, the motivation behind it, any major architectural changes, and key highlights.]

## 🌟 Highlights
- **[Feature Name]** — [Key detail about the feature and why it matters.]

## ✨ Added
- [New check or parameter added]
- [New template or component introduced]

## 🐛 Fixed
- [Description of the bug, root cause, and how it was fixed]

## 🔄 Changed
- [Details of internal changes, refactorings, or updates to dependencies]

## ⚠️ Behavior changes and migration
- [Describe any breaking changes, deprecations, or updates that require user action]
- [If there are no behavior changes, state: "None. Caller workflows are unaffected."]

## 🧪 Validation checklist
- [ ] **yamllint**: [e.g., clean — 0 errors]
- [ ] **actionlint**: [e.g., clean — 0 failures]

## ℹ️ Known issues
- [Description of any known issues or limitations in this release. State "None" if there are none.]

## 📚 References
- **CHANGELOG:** [Link to CHANGELOG.md entry]
- **README:** [Link to README.md]
