#!/usr/bin/env python3
"""
Fetch a sample of SonarQube warnings before and after treatment for treatment repos.

This script:
1. Reads panel data to identify treatment repositories and their adoption times
2. Queries SonarQube API for issues/warnings at time points before and after treatment
3. Saves a sample of warnings for qualitative analysis
"""

import logging
import os
import random
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_HOST = os.getenv("SONAR_HOST")

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

ISSUE_TYPES = ["BUG", "VULNERABILITY", "CODE_SMELL"]
SAMPLE_SIZE_PER_REPO_PERIOD = 500
MAX_PERIODS = 6
RANDOM_SEED = 114514


def get_all_issues_for_version(project_key: str, version: str) -> list[dict]:
    """
    Fetch all issues from SonarQube for a specific project version.

    Args:
        project_key: SonarQube project key
        version: Version identifier (e.g., "2024-08")

    Returns:
        List of all issue dictionaries
    """
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    all_issues = []

    for issue_type in ISSUE_TYPES:
        url = f"{SONAR_HOST}/api/issues/search"
        page = 1
        page_size = 500

        while True:
            params = {
                "componentKeys": project_key,
                "types": issue_type,
                "ps": page_size,
                "p": page,
                "resolved": "false",
            }

            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                issues = data.get("issues", [])
                for issue in issues:
                    all_issues.append(
                        {
                            "issue_key": issue.get("key"),
                            "type": issue.get("type"),
                            "severity": issue.get("severity"),
                            "message": issue.get("message"),
                            "component": issue.get("component"),
                            "line": issue.get("line"),
                            "rule": issue.get("rule"),
                            "effort": issue.get("effort"),
                            "creation_date": issue.get("creationDate"),
                        }
                    )

                if len(issues) < page_size:
                    break
                page += 1

            except requests.exceptions.RequestException as e:
                logging.warning(
                    "Failed to fetch issues for %s: %s", project_key, str(e)
                )
                break

    return all_issues


def get_issues_for_version(
    project_key: str, version: str, max_issues: int = 100
) -> list[dict]:
    """
    Fetch and randomly sample issues from a specific project version.

    Args:
        project_key: SonarQube project key
        version: Version identifier (e.g., "2024-08")
        max_issues: Maximum number of issues to sample

    Returns:
        Randomly sampled list of issue dictionaries
    """
    all_issues = get_all_issues_for_version(project_key, version)
    logging.info(
        "Found %d issues for %s at version %s", len(all_issues), project_key, version
    )

    if len(all_issues) <= max_issues:
        return all_issues

    return random.sample(all_issues, max_issues)


def get_analysis_versions(project_key: str) -> list[dict]:
    """
    Get all analysis versions for a project.

    Args:
        project_key: SonarQube project key

    Returns:
        List of analysis info with version and date
    """
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    analyses = []
    page = 1

    while True:
        url = f"{SONAR_HOST}/api/project_analyses/search"
        params = {"project": project_key, "category": "VERSION", "p": page, "ps": 100}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if not data.get("analyses"):
                break

            for analysis in data["analyses"]:
                if analysis.get("projectVersion"):
                    analyses.append(
                        {
                            "version": analysis["projectVersion"],
                            "date": analysis["date"],
                        }
                    )

            if len(data["analyses"]) < 100:
                break
            page += 1

        except requests.exceptions.RequestException as e:
            logging.warning("Failed to fetch analyses for %s: %s", project_key, str(e))
            break

    return analyses


def add_months(yyyymm: int, months: int) -> int:
    """Add months to a YYYYMM integer, returning the new YYYYMM."""
    year = yyyymm // 100
    month = yyyymm % 100
    total_months = year * 12 + (month - 1) + months
    new_year = total_months // 12
    new_month = (total_months % 12) + 1
    return new_year * 100 + new_month


def find_version_for_month(analyses: list[dict], target_month: int) -> Optional[str]:
    """
    Find an analysis version matching the target month exactly.

    Args:
        analyses: List of analysis dicts with version and date
        target_month: Target month in YYYYMM format (e.g., 202408)

    Returns:
        Version string or None if not found
    """
    target_str = str(target_month)
    target_with_dash = "%s-%s" % (target_str[:4], target_str[4:])

    for a in analyses:
        version = a["version"]
        version_normalized = version.replace("-", "")
        if version_normalized == target_str or version == target_with_dash:
            return version

    return None


def collect_warnings_for_repo(
    repo_name: str, event_time: int, sample_size: int = SAMPLE_SIZE_PER_REPO_PERIOD
) -> list[dict]:
    """
    Collect warnings for periods -6 to +6 relative to treatment.

    Args:
        repo_name: Repository name (e.g., "owner/repo")
        event_time: Treatment time in YYYYMM format
        sample_size: Max issues to collect per period

    Returns:
        List of all collected issues with relative_period metadata
    """
    project_key = repo_name.replace("/", "_")

    analyses = get_analysis_versions(project_key)
    if not analyses:
        logging.warning("No analyses found for %s", repo_name)
        return []

    all_issues = []
    periods_found = 0

    for offset in range(-MAX_PERIODS, MAX_PERIODS + 1):
        target_month = add_months(event_time, offset)
        version = find_version_for_month(analyses, target_month)

        if version is None:
            logging.debug(
                "No version for %s at period %+d (month %d)",
                repo_name,
                offset,
                target_month,
            )
            continue

        all_version_issues = get_all_issues_for_version(project_key, version)
        total_issues = len(all_version_issues)

        if total_issues <= sample_size:
            issues = all_version_issues
        else:
            issues = random.sample(all_version_issues, sample_size)

        logging.info(
            "Period %+d for %s: sampled %d/%d issues (version %s)",
            offset,
            repo_name,
            len(issues),
            total_issues,
            version,
        )
        periods_found += 1

        for issue in issues:
            issue["repo_name"] = repo_name
            issue["month"] = target_month
            issue["event_time"] = event_time
            issue["relative_period"] = offset

        all_issues.extend(issues)

    logging.info("Found %d periods with data for %s", periods_found, repo_name)
    return all_issues


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    random.seed(RANDOM_SEED)

    if not SONAR_TOKEN or not SONAR_HOST:
        logging.error("SONAR_TOKEN and SONAR_HOST must be set in .env file")
        return

    panel_file = DATA_DIR / "panel_event_monthly.csv"
    if not panel_file.exists():
        logging.error("Panel data file not found: %s", panel_file)
        return

    panel_df = pd.read_csv(panel_file)

    treatment_df = panel_df[
        panel_df["event"].notna() & (panel_df["event"] != "")
    ].copy()
    treatment_df["event"] = treatment_df["event"].astype(str).str.replace("-", "")
    treatment_df = treatment_df[treatment_df["event"].str.match(r"^\d{6}$")]
    treatment_df["event"] = treatment_df["event"].astype(int)

    treatment_df = treatment_df[
        (treatment_df["event"] > 202407) & (treatment_df["event"] <= 202503)
    ]

    treatment_repos = treatment_df.groupby("repo_name")["event"].first().reset_index()
    logging.info("Found %d treatment repositories", len(treatment_repos))

    all_issues = []

    for _, row in treatment_repos.iterrows():
        repo_name = row["repo_name"]
        event_time = row["event"]

        logging.info("Processing %s (treatment at %d)", repo_name, event_time)
        issues = collect_warnings_for_repo(repo_name, event_time)
        all_issues.extend(issues)

    if all_issues:
        output_df = pd.DataFrame(all_issues)

        key_cols = ["repo_name", "month", "event_time", "relative_period"]
        other_cols = [c for c in output_df.columns if c not in key_cols]
        output_df = output_df[key_cols + other_cols]

        definition_cols = ["rule", "type", "severity", "message", "effort"]
        definitions_df = output_df[definition_cols].drop_duplicates()
        definitions_df = definitions_df.sort_values("rule").reset_index(drop=True)

        definitions_file = DATA_DIR / "sonarqube_warning_definitions.csv"
        definitions_df.to_csv(definitions_file, index=False)
        logging.info(
            "Saved %d unique rule definitions to %s",
            len(definitions_df),
            definitions_file,
        )

        cols_to_drop = ["type", "severity", "message", "effort"]
        output_df = output_df.drop(columns=cols_to_drop)

        output_file = DATA_DIR / "sonarqube_warnings.csv"
        output_df.to_csv(output_file, index=False)
        logging.info("Saved %d issues to %s", len(output_df), output_file)

        summary = definitions_df.groupby(["type"]).size()
        logging.info("Rule definitions by type:\n%s", summary)

        period_counts = output_df.groupby("relative_period").size()
        logging.info("Issues per relative period:\n%s", period_counts)
    else:
        logging.warning("No issues collected")


if __name__ == "__main__":
    main()
