from github_to_post.sources import SOURCE_REPOSITORIES


def test_source_repositories_contains_public_fixture() -> None:
    assert SOURCE_REPOSITORIES == ["coin-or/pulp"]
