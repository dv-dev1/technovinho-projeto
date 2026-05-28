import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
ARTIFACTS = DOCS / "validation-artifacts" / "minuciosa"


def load_json(name: str) -> dict:
    with (ARTIFACTS / name).open(encoding="utf-8") as file:
        return json.load(file)


def test_minuciosa_required_artifacts_are_versioned():
    expected_files = [
        DOCS / "RELATORIO_VALIDACAO_MINUCIOSA_TECHNOVINHO.docx",
        ARTIFACTS / "README.md",
        ARTIFACTS / "api-results.json",
        ARTIFACTS / "ui-results.json",
        ARTIFACTS / "resumo-rodada.md",
        ARTIFACTS / "evidencias-aprovacao-falhas-lacunas.md",
        ARTIFACTS / "bugs-linkados.md",
        ARTIFACTS / "docx-render" / "RELATORIO_VALIDACAO_MINUCIOSA_TECHNOVINHO.pdf",
        ARTIFACTS / "docx-render" / "page-1.png",
        ARTIFACTS / "docx-render" / "page-2.png",
    ]

    missing = [str(path.relative_to(ROOT)) for path in expected_files if not path.exists()]

    assert missing == []


def test_minuciosa_api_summary_matches_acceptance_criteria():
    api_results = load_json("api-results.json")

    assert api_results["summary"]["total"] == 61
    assert api_results["summary"]["passed"] == 61
    assert api_results["summary"]["failed"] == 0
    assert api_results["summary"]["pass_rate"] == "100%"


def test_minuciosa_ui_summary_matches_acceptance_criteria():
    ui_results = load_json("ui-results.json")

    assert ui_results["summary"]["total"] == 13
    assert ui_results["summary"]["passed"] == 13
    assert ui_results["summary"]["failed"] == 0
    assert ui_results["summary"]["pass_rate"] == "100%"


def test_minuciosa_bugs_and_known_gaps_are_tracked():
    api_results = load_json("api-results.json")
    ui_results = load_json("ui-results.json")

    api_bug_ids = {bug["id"] for bug in api_results["bugs"]}
    ui_bug_ids = {bug["id"] for bug in ui_results["bugs"]}
    gap_ids = {gap["id"] for gap in api_results["known_gaps"]}

    assert {"BUG-001", "BUG-002"}.issubset(api_bug_ids)
    assert "BUG-002" in ui_bug_ids
    assert {"GAP-001", "GAP-002"}.issubset(gap_ids)
