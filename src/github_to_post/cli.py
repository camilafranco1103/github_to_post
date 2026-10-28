"""Command-line entry point for the project scaffold."""

from github_to_post.sources import SOURCE_REPOSITORIES


def main() -> None:
    print("GitHub to Post ETL scaffold")
    print("Configured repositories:")
    for repository in SOURCE_REPOSITORIES:
        print(f"- {repository}")
    print("Analysis pipeline implementation is in progress.")
