from types import SimpleNamespace
from unittest.mock import MagicMock

import github
import pytest

from app.services.repositories.github_service import GithubService


def _make_service():
    service = GithubService.__new__(GithubService)
    service.registry = MagicMock()
    service.gh_repository = MagicMock()
    return service


def _commit_payload():
    return [{
        "contents": "print('hello')\n",
        "path": "sample-cell",
        "file_name": "task.py",
    }]


def test_commit_retries_non_fast_forward_and_succeeds():
    service = _make_service()
    service.registry.query_registry_for_image.return_value = {"exists": True}
    service.gh_repository.get_contents.return_value = SimpleNamespace(
        sha="remote-sha")
    service.gh_repository.create_git_blob.return_value = SimpleNamespace(
        sha="blob-sha")
    service.gh_repository.get_git_tree.return_value = SimpleNamespace(
        sha="tree-sha")
    service.gh_repository.create_git_tree.return_value = SimpleNamespace(
        sha="new-tree-sha")
    service.gh_repository.get_branch.return_value = SimpleNamespace(
        commit=SimpleNamespace(sha="parent-sha"))
    service.gh_repository.get_git_commit.return_value = SimpleNamespace(
        sha="parent-sha")
    service.gh_repository.create_git_commit.side_effect = [
        SimpleNamespace(sha="new-commit-sha-1"),
        SimpleNamespace(sha="new-commit-sha-2"),
    ]

    main_ref = MagicMock()
    main_ref.edit.side_effect = [
        github.GithubException(
            422, {"message": "Reference update failed"}, None),
        None,
    ]
    service.gh_repository.get_git_ref.return_value = main_ref

    result = service.commit(commit_list=_commit_payload())

    assert result["content_updated"] is True
    assert result["commit_sha"] == "new-commit-sha-2"
    assert service.gh_repository.create_git_commit.call_count == 2
    assert main_ref.edit.call_count == 2


def test_commit_raises_on_non_retryable_branch_update_error():
    service = _make_service()
    service.registry.query_registry_for_image.return_value = {"exists": True}
    service.gh_repository.get_contents.return_value = SimpleNamespace(
        sha="remote-sha")
    service.gh_repository.create_git_blob.return_value = SimpleNamespace(
        sha="blob-sha")
    service.gh_repository.get_git_tree.return_value = SimpleNamespace(
        sha="tree-sha")
    service.gh_repository.create_git_tree.return_value = SimpleNamespace(
        sha="new-tree-sha")
    service.gh_repository.get_branch.return_value = SimpleNamespace(
        commit=SimpleNamespace(sha="parent-sha"))
    service.gh_repository.get_git_commit.return_value = SimpleNamespace(
        sha="parent-sha")
    service.gh_repository.create_git_commit.return_value = SimpleNamespace(
        sha="new-commit-sha-1")

    main_ref = MagicMock()
    main_ref.edit.side_effect = github.GithubException(
        500, {"message": "Server error"}, None)
    service.gh_repository.get_git_ref.return_value = main_ref

    with pytest.raises(Exception, match="Update failed after retrying"):
        service.commit(commit_list=_commit_payload())

