# How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects

Replication package

> MSR '26 https://doi.org/10.1145/3793302.3793349, https://doi.org/10.5281/zenodo.18368661

---

## Current reproduction status

This has been updated to reflect the Phase 1 reproduction completed on the Ubuntu server using the existing `data/` directory.

Phase 1 means:

```text
Use the already prepared data files in data/
Render the R Markdown notebooks in notebooks/
Reproduce the main paper tables, figures, and robustness outputs
Do not rerun live data collection yet
```

Current status:

```text
Environment setup:                         done
R 4.3.3 installed:                          done
Python 3.11.4 available:                    done
Core R packages installed:                  done
Plot/table R packages installed:            done

DataCollection.Rmd rendered:                done
PropensityScoreMatching.Rmd rendered:       done
DiffInDiffBorusyak.Rmd rendered:            done
Figure 3 PDF created:                       done
DynamicPanel.Rmd rendered:                  done
Table 3 reproduced:                         done

DiffInDiffAll.Rmd rendered:                 done
DiffInDiffTWFE.Rmd rendered:                done
DiffInDiffCallaway.Rmd rendered:            done
AnalyzeSonarQubeWarnings.Rmd rendered:      done
NonCausalMethods.Rmd rendered:              done
DiffInDiffPosterFigures.Rmd rendered:       done

Full data collection rerun:                 not yet
```

The main Phase 1 reproduction script is:

```text
run-phase1.sh
```

Run it from the repository root after activating the `cursorstudy` conda environment.

---

## Recommended reproduction workflow

There are two different workflows.

### Phase 1: Reproduce the paper results from existing data

This is the recommended workflow for exact reproduction.

```bash
conda activate cursorstudy
./run-phase1.sh
```

This phase reads the existing CSV files from:

```text
data/
```

and renders the R Markdown notebooks from:

```text
notebooks/
```

This is the workflow used for the successful checkpoint documented in this README.

### Phase 2: Rerun data collection from live sources

This is optional and not recommended for exact reproduction.

Phase 2 would rerun GitHub search, repository cloning, GHArchive/BigQuery collection, and SonarQube analysis. Because these steps depend on live systems, rerunning them later may not produce the exact same dataset used in the paper. GitHub repositories may be deleted or updated, API behavior may change, and SonarQube rules may evolve.

Do not run Phase 2 unless the goal is to rebuild or extend the dataset rather than exactly reproduce the paper outputs.

---

## Repository organization

### `data/`

The `data/` folder contains the dataset used for the paper. Some files may be `.gitignore`d in the GitHub repository but are available from Zenodo.

Important files include:

```text
repos.csv
cursor_commits.csv
cursor_files.csv
repo_events.csv
repo_events_control.csv
matching.csv
panel_event_monthly.csv
ts_repos_monthly.csv
ts_repos_control_monthly.csv
repo_metrics.csv
sonarqube_warnings.csv
sonarqube_warning_definitions.csv
control_repo_candidates_*.csv
```

Key roles:

| File | Purpose |
|---|---|
| `repos.csv` | Metadata for Cursor-adopting treatment repositories |
| `cursor_commits.csv` | Commits that modify Cursor configuration files |
| `cursor_files.csv` | Cursor configuration files found in repositories |
| `repo_events.csv` / `repo_events_control.csv` | GitHub event data for treatment/control repositories |
| `matching.csv` | Propensity score matching results |
| `panel_event_monthly.csv` | Main monthly panel dataset for DiD and dynamic panel analysis |
| `ts_repos_monthly.csv` / `ts_repos_control_monthly.csv` | Monthly time series data for treatment/control repositories |
| `repo_metrics.csv` | Additional repository-level metrics |
| `sonarqube_warnings.csv` | SonarQube static analysis warnings |
| `sonarqube_warning_definitions.csv` | SonarQube warning metadata and categories |
| `control_repo_candidates_*.csv` | Monthly candidate control repository snapshots |

### `notebooks/`

The `notebooks/` folder contains the R Markdown notebooks used to reproduce the paper results.

| Notebook | Role in reproduction |
|---|---|
| `DataCollection.Rmd` | Dataset overview, descriptive statistics, and collection summary |
| `PropensityScoreMatching.Rmd` | Propensity score matching and balance diagnostics |
| `DiffInDiffBorusyak.Rmd` | Main Borusyak et al. DiD results, including Figure 3 |
| `DynamicPanel.Rmd` | Dynamic panel GMM results, corresponding to Table 3 |
| `DiffInDiffAll.Rmd` | Comparison across DiD estimators |
| `DiffInDiffTWFE.Rmd` | Two-way fixed effects DiD robustness analysis |
| `DiffInDiffCallaway.Rmd` | Callaway and Sant'Anna DiD robustness analysis |
| `AnalyzeSonarQubeWarnings.Rmd` | SonarQube warning severity/type analysis |
| `NonCausalMethods.Rmd` | Descriptive and correlational auxiliary analysis |
| `DiffInDiffPosterFigures.Rmd` | Poster-oriented versions of selected figures |

### `plots/`

The `plots/` folder stores generated figures. Some plot files may be `.gitignore`d in the GitHub repository but available from Zenodo.

Important reproduced files include:

```text
plots/dynamic_effects_borusyak.pdf
plots/dynamic_effects_activity_all.pdf
plots/dynamic_effects_agent_cohort_all.pdf
```

The file:

```text
plots/dynamic_effects_borusyak.pdf
```

corresponds to the paper's Figure 3.

### `scripts/`

The `scripts/` folder contains Python scripts for data collection and preparation. These scripts are mainly for Phase 2.

They include scripts for:

```text
GitHub repository search
repository cloning
Git history analysis
GHArchive/BigQuery collection
propensity score matching
SonarQube scanning
panel dataset preparation
```

These scripts are useful for understanding or extending the pipeline, but they should not be rerun when the goal is exact Phase 1 reproduction.

### `env_dev/`

The `env_dev/` folder stores the local environment snapshot used for reproduction.

Expected files include:

```text
env_dev/conda-list.txt
env_dev/cursorstudy-explicit-linux-64.txt
env_dev/cursorstudy-full-no-prefix.yml
env_dev/cursorstudy-full.yml
env_dev/export-date.txt
env_dev/pip-freeze.txt
env_dev/r-installed-packages.csv
env_dev/r-session-info.txt
env_dev/system-uname.txt
```

Use `cursorstudy-full-no-prefix.yml` for normal environment recreation.

---

## Development environment

The successful Phase 1 reproduction used:

```text
Conda environment: cursorstudy
Python: 3.11.4
R: 4.3.3
Operating system: Ubuntu 22.04.5 LTS
Platform: Linux x86_64
```

The working R executable path was:

```text
{HOME-PATH}/miniconda3/envs/cursorstudy/bin/R
```

The working Rscript path was:

```text
{HOME-PATH}/miniconda3/envs/cursorstudy/bin/Rscript
```

Check your environment with:

```bash
which python
python --version

which R
R --version

which Rscript
Rscript --version
```

Expected versions:

```text
Python 3.11.4
R version 4.3.3
```

---

## Recreate the environment

### Option A: Recreate from the portable conda YAML

This is the recommended method.

```bash
conda env create -f env_dev/cursorstudy-full-no-prefix.yml
conda activate cursorstudy
```

If the environment name already exists, create a separate environment:

```bash
conda env create -n cursorstudy-rebuild -f env_dev/cursorstudy-full-no-prefix.yml
conda activate cursorstudy-rebuild
```

### Option B: Recreate exactly on Linux x86_64

This is more exact but less portable.

```bash
conda create -n cursorstudy-rebuild --file env_dev/cursorstudy-explicit-linux-64.txt
conda activate cursorstudy-rebuild
```

### If `conda activate` fails

Run:

```bash
conda init bash
exec bash
conda activate cursorstudy
```

For shell scripts or VS Code Remote SSH terminals, this form is often safer:

```bash
source {HOME-PATH}/miniconda3/etc/profile.d/conda.sh
conda activate cursorstudy
```

Adjust the miniconda path if your system uses a different location.

---

## Verify required packages

### Verify Python packages

```bash
python --version
pip --version
pip freeze | grep -E "pandas|numpy|requests|GitPython|PyGithub|google-cloud-bigquery|scikit-learn|semver|node-semver|gql|aiohttp"
```

Important Python packages include:

```text
pandas
numpy
requests
python-dotenv
GitPython
PyGithub
google-cloud-bigquery
scikit-learn
semver
node-semver
gql
aiohttp
```

These are mainly needed for Phase 2 data collection scripts.

### Verify core R packages

```bash
Rscript -e "pkgs <- c('tidyverse','did','DRDID','didimputation','fixest','plm','modelsummary','rmarkdown','languageserver'); print(setNames(sapply(pkgs, requireNamespace, quietly=TRUE), pkgs))"
```

Expected result:

```text
tidyverse       TRUE
did             TRUE
DRDID           TRUE
didimputation   TRUE
fixest          TRUE
plm             TRUE
modelsummary    TRUE
rmarkdown       TRUE
languageserver  TRUE
```

### Verify plotting and table packages

```bash
Rscript -e "pkgs <- c('systemfonts','magick','Cairo','svglite','ggfx','kableExtra'); print(setNames(sapply(pkgs, requireNamespace, quietly=TRUE), pkgs))"
```

Expected result:

```text
systemfonts TRUE
magick      TRUE
Cairo       TRUE
svglite     TRUE
ggfx        TRUE
kableExtra  TRUE
```

---

## Install missing R packages

For conda-based reproduction, prefer conda-forge for large R packages and system-dependent graphics packages.

```bash
conda install -c conda-forge   r-base=4.3.3   r-tidyverse   r-rmarkdown   r-knitr   r-data.table   r-fixest   r-did   r-drdid   r-fastglm   r-plm   r-modelsummary   r-kableextra   r-gridextra   r-cowplot   r-corrplot   r-rcolorbrewer   r-cairo   r-showtext   r-ggfx   r-languageserver   -y
```

If plotting packages are missing:

```bash
conda install -c conda-forge   r-systemfonts   r-magick   r-cairo   r-svglite   r-ggfx   r-kableextra   -y
```

If smaller R packages are still missing, install them from R:

```r
options(repos = c(CRAN = "https://cloud.r-project.org"))

install.packages(c(
  "didimputation",
  "bacondecomp"
))
```

If an R package installation fails and leaves a lock directory, remove stale locks:

```bash
find "$CONDA_PREFIX/lib/R/library" -maxdepth 1 -name "00LOCK*" -type d -print -exec rm -rf {} +
```

---

## Run Phase 1 reproduction

Use the provided script:

```bash
conda activate cursorstudy
./run-phase1.sh
```

Recommended `run-phase1.sh` content:

```bash
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
```

If your current `run-phase1.sh` does not contain the shebang and safety options, update it:

```bash
chmod +x run-phase1.sh
```

The line:

```bash
set -euo pipefail
```

makes the script stop immediately if a notebook fails.

---

## Expected Phase 1 HTML outputs

After a successful Phase 1 run, the following files should exist:

```text
notebooks/DataCollection.html
notebooks/PropensityScoreMatching.html
notebooks/DiffInDiffBorusyak.html
notebooks/DynamicPanel.html
notebooks/DiffInDiffAll.html
notebooks/DiffInDiffTWFE.html
notebooks/DiffInDiffCallaway.html
notebooks/AnalyzeSonarQubeWarnings.html
notebooks/NonCausalMethods.html
notebooks/DiffInDiffPosterFigures.html
```

Check with:

```bash
ls -lh notebooks/*html
```

---

## Main reproduced results

### Figure 3

The main reproduced Figure 3 file is:

```text
plots/dynamic_effects_borusyak.pdf
```

It contains five panels:

```text
1. Commits
2. Lines Added
3. Static Analysis Warnings
4. Duplicated Lines Density
5. Code Complexity
```

Interpretation:

```text
Cursor adoption produces a large but short-lived increase in development velocity,
especially lines added, while static analysis warnings and code complexity increase
more persistently.
```

In short:

```text
Cursor makes projects faster at first,
but the code also becomes more warning-heavy and complex over time.
```

The x-axis is months relative to Cursor adoption:

```text
-6 to -2   months before Cursor adoption
0          adoption month
1 to 6     months after adoption
```

Filled and hollow points indicate statistical significance:

```text
Filled point: statistically significant, p < 0.05
Hollow point: not statistically significant, p >= 0.05
```

### Dynamic panel / Table 3

The dynamic panel results are reproduced by:

```text
notebooks/DynamicPanel.html
```

This notebook examines whether accumulated code quality burden is associated with later development velocity.

Core interpretation:

```text
Cursor adoption is associated with short-term velocity gains.
Warnings and complexity accumulate after adoption.
Accumulated warnings and complexity are associated with lower future velocity.
```

This supports the paper's main story:

```text
short-term speed gain
longer-term quality and complexity cost
```

### Robustness notebooks

The following notebooks were also rendered successfully:

```text
notebooks/DiffInDiffAll.html
notebooks/DiffInDiffTWFE.html
notebooks/DiffInDiffCallaway.html
```

These check whether the DiD findings are consistent across alternative DiD estimators.

### SonarQube warning detail analysis

The warning detail analysis is reproduced by:

```text
notebooks/AnalyzeSonarQubeWarnings.html
```

This notebook examines the composition of SonarQube warnings before and after Cursor adoption, including severity and warning categories.

### Auxiliary notebooks

The following auxiliary outputs were also rendered successfully:

```text
notebooks/NonCausalMethods.html
notebooks/DiffInDiffPosterFigures.html
```

---

## Notes about local patching

During Phase 1 reproduction, several notebooks required small compatibility patches for the local R/ggplot2/grid environment.

These patches affected plot rendering only. They did not change the data, model estimates, confidence intervals, or statistical interpretation.

### `DiffInDiffBorusyak.Rmd`

Possible errors:

```text
object 'significant' not found
invalid hex digit in 'color' or 'lty'
```

Cause:

```text
Fragile ggplot aesthetics involving after_scale(), significance mapping, or linetype mapping.
```

Safe fix:

```text
Draw significant and non-significant error bars as separate layers.
Use simpler point shapes for significant/non-significant results.
```

### `DiffInDiffAll.Rmd`

Possible error:

```text
object 'significant' not found
```

Cause:

```text
Same ggplot after_scale/significance aesthetic compatibility issue.
```

Safe fix:

```text
Use separate plotting layers for significant and non-significant intervals.
```

### `DiffInDiffPosterFigures.Rmd`

Possible error:

```text
Error in element_line(): unused argument (alpha = 0.25)
```

Cause:

```text
The installed ggplot2 version does not support alpha inside element_line().
```

Safe fix:

```text
Remove the unsupported alpha argument from element_line()/theme() calls.
```

Again, these are plot-style compatibility fixes only.

---

## VS Code Remote SSH setup

This project can be reproduced using VS Code with Remote SSH.

Recommended workflow:

```text
Local machine:
- VS Code UI
- Remote SSH connection

Remote Ubuntu server:
- conda environment
- R execution
- R Markdown rendering
- data files
- generated plots
```

Install the VS Code R extension on the remote SSH target.

Recommended `.vscode/settings.json`:

```json
{
  "r.rpath.linux": "{HOME-PATH}/miniconda3/envs/cursorstudy/bin/R",
  "r.rterm.linux": "{HOME-PATH}/miniconda3/envs/cursorstudy/bin/R",
  "r.bracketedPaste": true
}
```

Adjust paths if your conda environment is elsewhere.

---

## Refresh the environment snapshot

After a successful reproduction run, refresh `env_dev/`:

```bash
conda activate cursorstudy

mkdir -p env_dev

conda env export > env_dev/cursorstudy-full.yml
grep -v "^prefix:" env_dev/cursorstudy-full.yml > env_dev/cursorstudy-full-no-prefix.yml

conda list --explicit > env_dev/cursorstudy-explicit-linux-64.txt
conda list > env_dev/conda-list.txt

pip freeze > env_dev/pip-freeze.txt

Rscript -e "ip <- as.data.frame(installed.packages()[, c('Package','Version','LibPath')]); write.csv(ip, 'env_dev/r-installed-packages.csv', row.names=FALSE)"
Rscript -e "sink('env_dev/r-session-info.txt'); sessionInfo(); sink()"

date > env_dev/export-date.txt
uname -a > env_dev/system-uname.txt
```

Check:

```bash
ls -lh env_dev/
```

---

## What not to run during Phase 1

Do not run live data collection during Phase 1:

```bash
bash data-collection.sh
python -m scripts.clone_repos
python -m scripts.analyze_repos
python -m scripts.fetch_gharchive
python -m scripts.run_sonarqube
```

These commands belong to Phase 2 and may change the dataset.

---

## Optional Phase 2: rerun full data collection

Phase 2 is for rebuilding the dataset from live sources.

Before Phase 2, configure credentials and tool paths such as:

```text
GITHUB_TOKEN
SONAR_HOST
SONAR_SCANNER_PATH
SONAR_TOKEN
```

The approximate Phase 2 pipeline is:

```text
1. Search for Cursor-adopting repositories
2. Clone treatment repositories
3. Analyze treatment repository commits and lines added
4. Fetch GHArchive activity for treatment repositories
5. Run SonarQube for treatment repositories

6. Build candidate controls
7. Match treatment and control repositories
8. Clone matched control repositories
9. Analyze control repository commits and lines added
10. Fetch GHArchive activity for controls
11. Run SonarQube for controls
12. Prepare panel datasets
13. Rerun the R notebooks
```

Because this pipeline depends on live systems, results may differ from the published paper dataset.

---

## SonarQube note

The file:

```text
sonarqube-start.sh
```

is for starting/stopping a local SonarQube server.

It is not needed for Phase 1 reproduction from existing data.

It matters only if rerunning SonarQube static analysis in Phase 2.

---

## Quick verification checklist

Run:

```bash
git status
ls -lh notebooks/*html
ls -lh plots/*pdf
```

Expected core files:

```text
notebooks/DataCollection.html
notebooks/PropensityScoreMatching.html
notebooks/DiffInDiffBorusyak.html
notebooks/DynamicPanel.html
notebooks/DiffInDiffAll.html
notebooks/DiffInDiffTWFE.html
notebooks/DiffInDiffCallaway.html
notebooks/AnalyzeSonarQubeWarnings.html
notebooks/NonCausalMethods.html
notebooks/DiffInDiffPosterFigures.html
plots/dynamic_effects_borusyak.pdf
```

At this checkpoint, Phase 1 reproduction is complete.
