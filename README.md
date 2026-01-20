# Tommy John Surgery Research

- A data-driven analysis exploring the relationship between pitching characteristics and Tommy John surgery outcomes using Bayesian statistical methods and machine learning.

## Overview

- This research project investigates potential correlating factors between pitches thrown and pitchers who undergo Tommy John surgery (ulnar collateral ligament reconstruction). The study employs Bayesian statistical methods to identify  correlations and develop predictive models for surgery risk assessment.

**Research Presentation:** 
- Preliminary findings were presented at the Consortium for the Science of Sociotechnical Systems (CSAS) 2025 at Yale University.

## Features

- **Data Collection & Processing**: Automated web scraping and data cleaning pipelines using BaseballR
- **Statistical Modeling**: Multiple analytical approaches including:
  - Logistic Regression
  - Decision Trees
  - Random Forest
  - Bayesian Hierarchical Models (RStan)
- **Interactive Visualization**: Python-based dashboard for exploring pitching data and patterns

## Repository Structure

```
├── Baseball_Basics.R          # Data gathering and cleaning scripts
├── BayesianModelTesting.ipynb # Bayesian model development and testing
├── pitch_testing.ipynb        # Pitch analysis and experimentation
├── Dash.py                    # Interactive dashboard application
├── data_complete.parquet      # Processed dataset
├── requirements.txt           # Python dependencies
└── assets/                    # Dashboard assets and resources
```

## Technologies Used

### R Environment
- **BaseballR**: MLB data acquisition and processing
- **RStan**: Bayesian statistical modeling and inference
- **tidyverse**: Data manipulation and visualization

### Python Environment
- **Plotly Dash**: Interactive web-based dashboards
- **pandas**: Data analysis and manipulation
- **scikit-learn**: Machine learning models

## Getting Started

### Prerequisites

**R Requirements:**
```r
install.packages(c("baseballr", "rstan", "tidyverse"))
```

**Python Requirements:**
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
python Dash.py
```

The dashboard will launch locally and provide interactive visualizations of pitching data and model predictions.

### Running Statistical Analysis

Open and execute the R files in RStudio or your preferred R environment:
1. Start with `Baseball_Basics.R` for data preparation
2. Explore `BayesianModelTesting.ipynb` for model development

## Methodology

The research pipeline consists of:

1. **Data Collection**: Aggregating pitcher statistics and Tommy John surgery records using BaseballR
2. **Feature Engineering**: Extracting relevant pitching metrics and temporal patterns
3. **Model Development**: Building and comparing multiple statistical and machine learning models
4. **Bayesian Inference**: Implementing hierarchical models to account for individual pitcher variability
5. **Validation**: Cross-validation and prediction accuracy assessment
6. **Visualization**: Interactive exploration of patterns and predictions

## Key Findings

The project identifies correlations between specific pitching patterns and Tommy John surgery risk, with the Bayesian hierarchical model providing probabilistic predictions that account for individual pitcher characteristics and uncertainty in the data.

## Contact

www.linkedin.com/in/brady-pinter


