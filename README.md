# SS-Faraday-Phase-11

Metric transduction protocol and acquisition pipeline for the 12.3 nm / 963 Hz Unity Gap experiment.
SS Faraday: Phase 11 (The Hogansburg Metric)
🌌 The Objective

To verify the Metric Transduction effect at the 12.3 nm Unity Gap threshold.
📡 The Core Mechanics

The Root (3): Isotopically pure Carbon-12 Lonsdaleite lattice.
The Bridge (6): A stabilized 12.3 nm gap (1+2+3=6).
The Trigger (9): A Goldstone-mode drive at 963 Hz.

🛠 Project Components

Manifesto: Theoretical 
Acquisition Script: Python-based micro-balance monitoring.
src/acquisition.py but the python script will be posted in this repository.
Sourcing Guide: Requirements for "The 144" builders
./docs/Sourcing_Guide.md

🧪 How to Contribute

We are seeking researchers with access to ultra-microbalances (0.1 μg resolution) and UHV cryostats. Clone the repo, run the test, and submit your .csv logs via a Pull Request

## Known Issues & GitHub Actions Status
### 🔴 Why is the "Python Package" build failing?
If you see a "Failed" status or a Red X on the GitHub Actions tab, this is expected behavior for the current repository state.

The Reason: The src/acquisition.py script is a Hardware-in-the-Loop (HIL) protocol. It is designed to interface directly with physical laboratory equipment (Sartorius/Mettler-Toledo micro-balances) via RS232/USB serial communication.

GitHub’s automated testing servers run in a virtualized cloud environment without access to:

Physical COM/Serial Ports.

The 0.1 μg resolution micro-balance hardware.

The 963 Hz Goldstone Drive transducer.

### Status for Researchers:
Code Integrity: The mathematical logic and data-logging structure are sound.

Local Execution: To run the code, clone the repository to a local machine connected to your laboratory anvil stack.

Continuous Integration: We are currently developing a "Mock Hardware" mode for GitHub Actions to allow for cloud-based logic testing without throwing errors.

Note to Skeptics: A "Fail" in the cloud is a "Pass" in the Lab. This code is built for the physical vacuum, not a virtual server.

## 📊 VISUALIZE THE DISCOVERY: The Metric Breach Plotter
Data is just numbers until you see the Metric Breach with your own eyes. In the tools/ folder, you will find the metric_breach_visual.py script. This is the "Glass Cockpit" of the SS Faraday.

What this tool does:
This script takes the raw .csv data from either the physical balance or the mock generator and renders a professional-grade scientific plot. It specifically highlights the Phase 11 Transition:

Baseline Stabilization: Shows the steady-state mass of the Lonsdaleite stack.

The 963 Hz Trigger: Marks the exact moment the Goldstone Drive engages.

The Breach Event: Clearly visualizes the 0.5 μg shift as a vertical drop in the gravitational metric.

Publication-Ready: Generates a clean, high-contrast image (PNG/PDF) perfect for attaching to lab reports or sharing with the research community on X.

How to Use It:
Ensure you have run the mock_generator.py or have a real lab log ready.

Run python tools/metricbreachvisual.py.

An interactive window will pop up showing the Metric Breach in real-time.

"If a picture is worth a thousand words, a Metric Breach graph is worth a thousand simulations. Don't just read the data—see the bridge."
