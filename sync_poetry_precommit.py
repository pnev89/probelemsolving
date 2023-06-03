"""Sync package versions from poetry.lock -> .pre-commit-config.yaml."""
import argparse

import yaml
from tomlkit.items import AoT
from tomlkit.toml_file import TOMLFile


def main(poetry_lock: str, precommit_config: str):
    """Sync package versions."""
    # load poetry lock file and get package versions to dictionary
    poetry = TOMLFile(poetry_lock)
    poetry_content = poetry.read()

    assert isinstance(poetry_content["package"], AoT)
    poetry_packages = {p["name"]: p["version"] for p in poetry_content["package"]}

    with open(precommit_config, encoding="utf-8") as stream:
        pre_commit_data = yaml.safe_load(stream)

    # Check and update versions
    for repo in pre_commit_data["repos"]:
        if "rev" in repo:
            # update primary repo
            _update_repo_rev(repo, poetry_packages)

            # we also want to do the additional dependencies
            _update_additional_dependencies(repo, poetry_packages)
        elif repo["repo"] == "local":
            pass
        else:
            raise ValueError(f"missing rev in repo {repo}")

    with open(args.precommit_config, "w", encoding="utf-8") as outstream:
        yaml.safe_dump(
            pre_commit_data,
            stream=outstream,
            sort_keys=False,
            default_flow_style=False,
        )


def _update_repo_rev(repo, poetry_packages):
    # poetry saves things under the package name, pre-commit uses the repo name
    # and then puts the package name as the hook id.
    # so we iterate over the hook ids and find the matches, if there are more
    # than one we raise an error.
    hook_versions = []
    for hook in repo["hooks"]:
        hv = poetry_packages.get(hook["id"], False)
        if hv:
            hook_versions.append(hv)

    if len(hook_versions) > 1:
        raise NotImplementedError(
            "Multiple hook versions for a single hook - please fix"
        )

    # if there is a poetry.lock version of the package in the hook
    # check to see whether the version requires a v in front of it
    if len(hook_versions) == 1:
        if "v" in repo["rev"]:
            rev = f"v{hook_versions[0]}"
        else:
            rev = str(hook_versions[0])
        repo["rev"] = rev

    # if len == 0 don't do anything


def _update_additional_dependencies(repo, poetry_packages):
    # pylint: disable=R1702
    for hook in repo["hooks"]:
        if "additional_dependencies" in hook:
            dependencies = []
            for dep in hook["additional_dependencies"]:
                # as was written could have any number of conditions - lets
                # just match to what is in poetry.
                dep_list = (
                    dep.replace("=", " ").replace(">", " ").replace("<", " ").split()
                )

                # No version in the .pre-commit-config.yaml
                if len(dep_list) == 1:
                    dep_version = poetry_packages.get(dep_list[0], False)
                    if dep_version:
                        dependencies.append(f"{dep_list[0]}=={dep_version}")
                    else:
                        dependencies.append(f"{dep_list[0]}")

                # there is a version - check a) is there a version in poetry, if so
                # check the format in the .pre-commit, else, yse what is in the .pre-commit
                elif len(dep_list) == 2:
                    dep_version = poetry_packages.get(dep_list[0], False)
                    if dep_version:
                        if "v" in dep_version:
                            dep_version = f"v{dep_version}"
                        dependencies.append(f"{dep_list[0]}=={dep_version}")
                    else:
                        # use the orignal version to get correct >=, <=  etc
                        dependencies.append(dep)

                # Uh Oh
                else:
                    raise NotImplementedError(dep)
            hook["additional_dependencies"] = dependencies


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--poetry-lock",
        type=str,
        default="poetry.lock",
        help="Path to the poetry.lock file",
    )
    parser.add_argument(
        "--precommit-config",
        type=str,
        default=".pre-commit-config.yaml",
        help="Path to the .pre-commit-config.yaml file",
    )
    args: argparse.Namespace = parser.parse_args()
    main(args.poetry_lock, args.precommit_config)
