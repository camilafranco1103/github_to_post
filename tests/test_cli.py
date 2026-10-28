from github_to_post.cli import main


def test_cli_lists_configured_repositories(capsys) -> None:
    main()

    assert capsys.readouterr().out == (
        "GitHub to Post ETL scaffold\n"
        "Configured repositories:\n"
        "- coin-or/pulp\n"
        "Analysis pipeline implementation is in progress.\n"
    )
