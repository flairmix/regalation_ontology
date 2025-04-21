import subprocess
from pathlib import Path

def test_build_base():
    output_owl = Path("ontology_base.owl")
    output_html = Path("ontology_base.html")

    if output_owl.exists():
        output_owl.unlink()
    if output_html.exists():
        output_html.unlink()

    venv_python = Path(".venv/Scripts/python.exe").resolve()
    assert venv_python.exists(), "[ error ] .venv не существует или не создан. Выполни: uv venv .venv"

    result = subprocess.run(
        [str(venv_python), "-m", "src.cli.main", "build-base"],
        capture_output=True,
        text=True
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    assert result.returncode == 0, f"build-base failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert output_owl.exists(), "[ error ] OWL-файл не создан"
    assert output_html.exists(), "[ error ] HTML-файл не создан"
