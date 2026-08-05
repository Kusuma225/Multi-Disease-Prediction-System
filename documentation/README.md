# Project Documentation

This directory contains all project documentation.

## Contents

### Reports (`reports/`)
- `project_report.md` - Complete project report in Markdown format
- `model_comparison.csv` - Detailed model performance comparison
- `model_comparison.md` - Model comparison in Markdown format

### Diagrams (`diagrams/`)
- `system_architecture.txt` - System architecture diagram
- `workflow_flowchart.txt` - Training and prediction workflow diagrams

## Generating Documentation

### Generate All Reports
```bash
python src/visualization/report_generator.py
```

### Generate Diagrams
```bash
python scripts/generate_diagrams.py
```

### Generate Visualizations
```bash
python src/visualization/visualizer.py
```

## Project Report Structure

The complete project report includes:

1. **Abstract**
2. **Introduction**
   - Background
2026-01-07 20:31:32 - dataset_download - INFO - ✓ Saved stroke dataset: (5110, 11)
2026-01-07 20:31:32 - dataset_download - INFO - ✓ Saved hypertension dataset: (1000, 12)
2026-01-07 20:31:32 - dataset_download - INFO - ✓ Saved anemia dataset: (800, 12)
2026-01-07 20:31:32 - dataset_download - INFO - ✓ Saved thyroid dataset: (7200, 8)
2026-01-07 20:31:32 - dataset_download - INFO - ✓ All datasets created successfully

   - Objectives
   - Diseases Covered
3. **Methodology**
   - System Architecture
   - Data Preprocessing
   - Machine Learning Models
   - Evaluation Metrics
   - Explainable AI Techniques
4. **Results and Analysis**
   - Model Performance Summary
   - Average Performance
5. **Discussion**
   - Key Findings
   - Challenges and Solutions
   - Limitations
6. **Conclusion**
   - Future Work
7. **References**
8. **Appendix**
   - System Requirements
   - Installation Instructions

## IEEE Format

For submission, convert the Markdown report to IEEE format using:
- Pandoc
- LaTeX
- Online Markdown to PDF converters

## Additional Resources

- See `README.md` in project root for overview
- See `data/README.md` for dataset information
- See individual module documentation in `src/` directories

## Citation

If using this project for research:

```
Multi-Disease Prediction System using Explainable AI
B.Tech Final Year Project
Department of Computer Science
2026
```
