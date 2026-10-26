# Vijeth Balasubramaniam — ML & Research Portfolio

A responsive, interactive portfolio for documenting machine-learning projects and a developing research direction in robust ML for astronomy and exoplanet detection.

## Preview locally

Because the site loads project data from `projects.json`, run a local static server rather than opening `index.html` directly.

### Python
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`.

## Publish with GitHub Pages

1. Create a GitHub account at https://github.com if you do not already have one.
2. Create a **public** repository named exactly `YOUR-USERNAME.github.io` (replace `YOUR-USERNAME` with your GitHub username). This creates a user-site URL.
3. Upload `index.html`, `styles.css`, `app.js`, `projects.json`, this README and the `projects/` folder to the repository root.
4. Open **Settings → Pages**. Choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
5. Wait for the deployment and visit `https://YOUR-USERNAME.github.io`.

Alternatively, use a normal repository such as `ml-research-portfolio`, then enable Pages in Settings. The URL will normally be `https://YOUR-USERNAME.github.io/ml-research-portfolio/`; relative links in this site are compatible with that setup.

## What's interactive

- Project search across titles, descriptions and tags
- Category filters
- Project-detail dialog
- Dark/light theme toggle
- Responsive layout and keyboard-accessible controls

## Important before publishing

This site was drafted from an exported academic e-portfolio. It is a **portfolio starter**, not a verification of every original assignment. Before publishing, review each project card and its code/report. Replace any placeholder wording with your exact method, your own contribution, the dataset/source, reproducible commands, results, limitations and citations. Do not upload private datasets, student records, API keys, passwords, copyrighted course materials or work you are not allowed to redistribute.

For group work, identify the group context and your specific contribution. For the MSc dissertation, check that any dataset and code can be shared, especially because the subject is mental health.

## Suggested next step

Create one clean repository for your strongest project first — likely EMNIST, multi-armed bandits, or a carefully redone astronomy/ML experiment. Give each repository its own README, environment instructions, baseline, evaluation and limitations. Link it from this portfolio only when the repository is ready.

## About the green contribution graph

GitHub's contribution graph counts eligible activity under GitHub's rules. It is not a research-quality score and a daily streak is not required for PhD applications. Do not generate empty commits, backdate work, or automate meaningless activity to make the graph green. Use version control when you genuinely change code, documentation, experiments or tests. A clear project with reproducible results is more persuasive than a full contribution calendar.
