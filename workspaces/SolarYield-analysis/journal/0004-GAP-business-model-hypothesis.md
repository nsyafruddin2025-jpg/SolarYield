# GAP: pyproject.toml is a generic template

**What**: `pyproject.toml` still contains placeholder values:

- `name = "my-kailash-project"`
- `description = "A Kailash SDK project (Rust-backed)"`
- Author: "Your Name <your.email@example.com>"

**Why it matters**: This repo is being used as a SolarYield project but has zero solar-specific metadata. Any package built from this would have a misleading name and description.

**What is needed**: Either rename the project properly (SolarYield) or fork a fresh Python project template with correct metadata.
