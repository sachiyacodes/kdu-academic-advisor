# Release readiness

This is an academic prototype, not an official KDU advising service. Recommendations use illustrative curriculum and grading rules. Preserve Group 22 attribution and the methodology disclosures.

## Reproducible build

Run `npm run build` from the repository root. It installs the exact frontend lockfile with `npm ci` before building. Python development checks use `requirements-dev-lock.txt`; the serverless runtime uses the separate `requirements.txt`. Do not retrain or replace the committed models during a release build.

The private root package's `1.0.0` and frontend scaffold's `0.0.0` are component metadata, not evidence that a public release or npm package exists. Neither package is intended for registry publication.

## Evidence

On November 16, 2026, the root build, frontend grade-preview test, and lint command completed. npm reported zero dependency vulnerabilities. Lint still reports five pre-existing warnings in `frontend/src/useAdvisorState.js`; they are not presented as a clean lint result. Backend code and locked dependencies are unchanged from the published 196-test repair. Hosted CI must confirm checks for each new published commit.

`screenshots/advisor.png` shows the live prototype's initial academic profile screen, captured on November 16, 2026. It contains demonstration options, not a real student's record. The live demo may change independently of this image.

## Distribution gate

No project license has been selected. Contributors must agree on reuse and distribution rights before an open-source license or distributable release is granted. This maintenance change does not grant rights on their behalf. Do not create a placeholder release or publish an npm/Python package to imply readiness.

Release notes should identify the tested source commit, deployed URL, model/data version, illustrative academic rules, known limitations, and contributor-approved licensing. Keep secrets and student data out of screenshots and release assets.
