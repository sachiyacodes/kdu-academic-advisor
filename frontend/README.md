# KDU Academic Advisor frontend

React and Vite interface for the Group 22 academic advising prototype. The [root README](../README.md) describes the backend, illustrative academic rules, setup, and licensing limits.

Use Node.js 24. From this directory:

```sh
npm ci
npm run dev
npm test
npm run lint
npm run build
```

The development server runs at `http://localhost:5173`. Start the Python backend using the root instructions. The root `npm run build` and Vercel both use the committed frontend lockfile. Build output is generated in `dist/`.

The frontend package is private. Its scaffold version is not a public application release. See [release readiness](../docs/release-readiness.md) for verification evidence and remaining distribution gates.
