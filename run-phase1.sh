#!/usr/bin/env bash
set -euo pipefail

echo "Starting Phase 1 reproduction..."
date

# Main data and matching
echo "Rendering DataCollection.Rmd"
Rscript -e "rmarkdown::render('notebooks/DataCollection.Rmd')"

echo "Rendering PropensityScoreMatching.Rmd"
Rscript -e "rmarkdown::render('notebooks/PropensityScoreMatching.Rmd')"

# Main causal results
echo "Rendering DiffInDiffBorusyak.Rmd"
Rscript -e "rmarkdown::render('notebooks/DiffInDiffBorusyak.Rmd')"

echo "Rendering DynamicPanel.Rmd"
Rscript -e "rmarkdown::render('notebooks/DynamicPanel.Rmd')"

# Robustness checks
echo "Rendering DiffInDiffAll.Rmd"
Rscript -e "rmarkdown::render('notebooks/DiffInDiffAll.Rmd')"

echo "Rendering DiffInDiffTWFE.Rmd"
Rscript -e "rmarkdown::render('notebooks/DiffInDiffTWFE.Rmd')"

echo "Rendering DiffInDiffCallaway.Rmd"
Rscript -e "rmarkdown::render('notebooks/DiffInDiffCallaway.Rmd')"

# Quality details and auxiliary analyses
echo "Rendering AnalyzeSonarQubeWarnings.Rmd"
Rscript -e "rmarkdown::render('notebooks/AnalyzeSonarQubeWarnings.Rmd')"

echo "Rendering NonCausalMethods.Rmd"
Rscript -e "rmarkdown::render('notebooks/NonCausalMethods.Rmd')"

echo "Rendering DiffInDiffPosterFigures.Rmd"
Rscript -e "rmarkdown::render('notebooks/DiffInDiffPosterFigures.Rmd')"

echo "Phase 1 reproduction completed."
date
