import pytest

from app.models.workflow_cell import Cell
from app.services.containerizers.r_containerizer import RContainerizer


def test_map_r_dependency():
    cell = Cell(
        title='test-r-containerizer',
        base_container_image={},
        dependencies=[{'name': 'TempSED'}],
        kernel='IRkernel',
        original_source='',
    )

    module_name_mapping = {
        "pip": {
        },
        "conda": {
        },
        "r": {
        }
    }

    containerizer = RContainerizer(cell)
    mapped_dependencies = containerizer.map_dependencies(
        dependencies=cell.dependencies,
        module_name_mapping=module_name_mapping
    )

    assert mapped_dependencies == {
        'conda_dependencies': {'r-TempSED'},
        'pip_dependencies': set(),
    }


def test_ignore_pip_dependencies():
    cell = Cell(
        title='test-r-containerizer',
        base_container_image={},
        dependencies=[{'name': 'TempSED'}],
        kernel='IRkernel',
        original_source='',
    )

    module_name_mapping = {
        "pip": {
            "r-TempSED": "some-pip-package"
        },
        "conda": {
        },
        "r": {
        }
    }

    containerizer = RContainerizer(cell)
    mapped_dependencies = containerizer.map_dependencies(
        dependencies=cell.dependencies,
        module_name_mapping=module_name_mapping
    )

    assert mapped_dependencies == {
        'conda_dependencies': {'r-TempSED'},
        'pip_dependencies': set(),
    }


@pytest.mark.parametrize(
    'mapping_name',
    ['r-TempSED', 'r-tempsed', 'TempSED', 'tempsed'],
)
def test_map_dependencies_matches_r_mapping_case_and_prefix(mapping_name):
    cell = Cell(
        title='test-r-containerizer',
        base_container_image={},
        dependencies=[{'name': 'TempSED'}],
        kernel='IRkernel',
        original_source='',
    )
    containerizer = RContainerizer(cell)

    mapped_dependencies = containerizer.map_dependencies(
        dependencies=cell.dependencies,
        module_name_mapping={'r': {mapping_name: None}},
    )

    assert mapped_dependencies == {
        'conda_dependencies': set(),
        'pip_dependencies': set(),
    }


def test_conda_mapping_tempsed():
    cell = Cell(
        title='test-r-containerizer',
        base_container_image={},
        dependencies=[{'name': 'cli'}, {'name': 'data.table'},
                      {'name': 'devtools'}, {'name': 'dplyr'},
                      {'name': 'fasttime'}, {'name': 'generics'},
                      {'name': 'ggplot2'}, {'name': 'ggrepel'},
                      {'name': 'lubridate'}, {'name': 'pak'},
                      {'name': 'purrr'}, {'name': 'Rcpp'},
                      {'name': 'RcppArmadillo'}, {'name': 'RcppRoll'},
                      {'name': 'sf'}, {'name': 'terra'},
                      {'name': 'tidyr'}, {'name': 'zoo'}],
        kernel='IRkernel',
        original_source='',
    )
    module_name_mapping = {
        "pip": {
        },
        "conda": {
        },
        "r": {
        }
    }

    containerizer = RContainerizer(cell)

    mapped_dependencies = containerizer.map_dependencies(
        dependencies=cell.dependencies,
        module_name_mapping=module_name_mapping
    )

    assert mapped_dependencies == {
        'conda_dependencies': {'r-cli', 'r-data.table', 'r-devtools',
                               'r-dplyr', 'r-fasttime', 'r-generics',
                               'r-ggplot2', 'r-ggrepel', 'r-lubridate',
                               'r-pak', 'r-purrr', 'r-Rcpp',
                               'r-RcppArmadillo', 'r-RcppRoll', 'r-sf',
                               'r-terra', 'r-tidyr', 'r-zoo'},
        'pip_dependencies': set(),
    }
