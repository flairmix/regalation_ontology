import subprocess
from pathlib import Path

def test_add_requirement_r002():
    json_file = Path("src/requirements/data/requirement_R002.json")
    owl_output = json_file.parent / "requirement_R002.owl"
    html_output = json_file.parent / "requirement_R002.html"

    # Очистим предыдущие результаты
    if owl_output.exists():
        owl_output.unlink()
    if html_output.exists():
        html_output.unlink()

    # Убедимся, что .venv существует
    venv_python = Path(".venv/Scripts/python.exe").resolve()
    assert venv_python.exists(), "[ error ] .venv не существует. Выполни: uv venv .venv"

    result = subprocess.run(
        [str(venv_python), "-m", "src.cli.main", "add-requirement", str(json_file)],
        capture_output=True,
        text=True
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    assert result.returncode == 0, f"add-requirement failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert owl_output.exists(), f"[ error ] OWL-файл не создан: {owl_output}"
    assert html_output.exists(), f"[ error ] HTML-файл не создан: {html_output}"
