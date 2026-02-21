Integrated GRC Risk Governance Dashboard (COBIT + NIST + CVE)
This repository contains a governance-oriented cyber risk decision-support dashboard that integrates:
•	COBIT 2019 governance intent (risk optimisation / governance objectives)
•	NIST SP 800-53 control context (control mapping for operational relevance)
•	Public vulnerability intelligence (CVE/NVD) to generate explainable, governance-ready risk signals
The artefact is designed for governance visibility and decision support (human-in-the-loop), not as an operational security monitoring platform.
What this project demonstrates
•	A working dashboard that summarises cyber risk at a governance level (e.g., high/medium/low)
•	A traceable pipeline from vulnerability data to risk evaluation to governance-level outputs
•	An integrated risk register that supports explainability and auditability
•	Reproducible execution steps to run locally for presentations
Tech Stack
•	Python 3.10+ (recommended)
•	Streamlit (dashboard UI)
•	Pandas (data handling)

Known Limitations
•	The dashboard provides governance-level insight, not asset-level exposure or live monitoring.
•	Risk signals are derived from public vulnerability intelligence and mappings; they do not confirm exploitation in a specific environment.
•	Outputs should be interpreted as decision support and require human judgement.

Author
Developed as part of an MSc project.

