# Verification notes — scientific portfolio iteration

## This iteration
- Replaced the rocket/space-travel hero with a scientific observatory motif: host star, orbit, transiting planet and an illustrative relative-flux curve.
- Shifted palette and language towards a scientific research notebook / observatory.
- Reframed chatbot greeting and response style to be conversational and explanatory.
- Added compare-intent handling and follow-up prompts in project responses.
- Kept chatbot local and scoped to the static project knowledge base; unmatched questions point to selected relevant resources.

## Not yet verified
- The project descriptions and future-work suggestions still require source-by-source review.
- The light curve is a conceptual illustration, not measured Kepler/TESS data.
- The chatbot is keyword/rule-based, not an LLM or full semantic search system.
- The full site should be previewed in desktop and mobile browsers before publishing.
- Replace `mailto:ADD-YOUR-EMAIL` with a public contact address or remove it.
- Add exact source repository links only after each project repository has been prepared and checked.

## Research integrity
The portfolio should distinguish original coursework, group work, individual contributions, reconstructed code and independently reproduced experiments. Never infer or invent accuracy, dataset size, model architecture, authorship or performance metrics.

## Follow-up integration checks
- Confirmed all 24 evidence-image references and their linked original report paths exist in the supplied archive.
- Updated project cards to open the matching GitHub `projects/<id>` folder instead of using a disabled link.
- Added direct links from each evidence caption to its original report file.
- Improved the local portfolio guide so it searches the full project knowledge fields and can handle short follow-up questions about the last project discussed.
- Removed the placeholder email link rather than publishing an unusable `ADD-YOUR-EMAIL` address.
- Checked `app.js` syntax with Node.js (`node --check`).

## Remaining checks before public release
- The evidence gallery displays full report pages, not separately cropped chart assets. The original plots and confusion matrices remain visible on those pages.
- The portfolio chatbot remains a local, rule-based guide, not an LLM. It only knows the content in `data/projects.js` and its built-in research-direction response.
- Review the mental-health dissertation and group-project report for personal information and attribution before making the repository public.
- Test the live GitHub Pages site after upload, because repository links assume the `main` branch and the exact repository path `Vijeth-ML/vijeth-ml.github.io`.
