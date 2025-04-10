# Git Commit Message Standards

- **Type:** Describes the nature of the change (e.g., `feat`, `fix`, etc.).
- **Scope (Optional):** Provides additional context by indicating what part of the codebase is affected (e.g., `api`, `auth`, `build`).
- **Description:** A short, imperative, and present-tense summary of the change.
- **Body (Optional):** A more detailed explanation of the change.
- **Footer (Optional):** Additional metadata (for example, issue references or a breaking change notice).

---

## Commit Types

Below are the commit types we follow:

- **feat:** A new feature or enhancement.
  - *Example:* `feat(auth): add two-factor authentication`
  - *Impact:* Generally triggers a minor version bump.

- **fix:** A bug fix.
  - *Example:* `fix(api): resolve null pointer exception in response handler`
  - *Impact:* Associated with patch releases.

- **docs:** Documentation-only changes.
  - *Example:* `docs: update installation instructions in README`

- **style:** Code style or formatting changes that do not affect functionality.
  - *Example:* `style: reformat code with Prettier`

- **refactor:** Changes that improve code structure or clarity without altering external behavior.
  - *Example:* `refactor(utils): simplify date formatting function`

- **perf:** Performance improvements.
  - *Example:* `perf: optimize database query in user service`

- **test:** Adding or updating tests.
  - *Example:* `test(auth): add unit tests for token validation`

- **build:** Changes affecting the build system or external dependencies.
  - *Example:* `build(deps): update dependency versions`

- **ci:** Updates to Continuous Integration configurations or scripts.
  - *Example:* `ci: update GitHub Actions workflow`

- **chore:** Routine tasks or maintenance changes that do not modify source code.
  - *Example:* `chore(version): bump project version to 1.2.3`

- **revert:** Reverting a previous commit.
  - *Example:* `revert: revert "feat(auth): add two-factor authentication"`