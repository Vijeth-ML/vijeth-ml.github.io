# Dataset availability and publishing policy

This portfolio contains original source code and report-derived visual evidence. Dataset files are handled conservatively:

- **Mental-health dissertation CSV:** intentionally not included. It may contain sensitive student-level or personal information. Publish only after checking consent, anonymisation, licence and university rules.
- **CamVid / Cam101 semantic-segmentation data:** an approximately 95 MB archive was present in the original e-portfolio. It is not copied into this GitHub repository. Check the dataset's original licence and download it from its authorised source; document the exact version and split.
- **EMNIST:** use the public dataset through `torchvision.datasets.EMNIST` (split `balanced`) so visitors can download it reproducibly rather than committing a duplicate dataset.
- **Other projects:** no separate redistributable dataset was identified in the supplied project packages. Their source code and reports are retained where available.

Do not commit personal data, access credentials, private student records, or datasets whose licence does not permit redistribution. Add a dataset URL, licence, version and checksum to the relevant project README once verified.
