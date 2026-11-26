import shutil
import subprocess
from pathlib import Path

import pytest


def test_generates_r_parsers_with_antlr(tmp_path):
    antlr4_cli = shutil.which('antlr4')
    if antlr4_cli is None:
        pytest.skip('antlr4 CLI is not installed')

    grammar_dir = (
        Path(__file__).resolve().parents[1]
        / 'services'
        / 'cell_extractor'
        / 'parseR'
    )
    shutil.copy2(grammar_dir / 'R.g4', tmp_path / 'R.g4')
    shutil.copy2(grammar_dir / 'RFilter.g4', tmp_path / 'RFilter.g4')

    result = subprocess.run(
        [antlr4_cli, '-Dlanguage=Python3', '-visitor', 'R.g4', 'RFilter.g4'],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f'ANTLR generation failed with exit code {result.returncode}.\n'
        f'stdout:\n{result.stdout}\n'
        f'stderr:\n{result.stderr}'
    )

    generated_files = {
        'RLexer.py',
        'RParser.py',
        'RFilter.py',
        'RListener.py',
        'RVisitor.py',
        'RFilterListener.py',
        'RFilterVisitor.py',
    }

    missing = [
        name for name in generated_files if not (tmp_path / name).is_file()
    ]
    assert not missing, f'ANTLR did not generate expected files: {missing}'
