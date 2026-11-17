# [IA] registro 3
import subprocess
import sys
from pypdf import PdfReader
from src.load_data import ROOT
import hashlib


def test_report_has_required_parts_and_draft_status():
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/gerar_relatorio.py')], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    pdf = PdfReader(ROOT / 'reports/relatorio_final.pdf')
    text = '\n'.join(p.extract_text() for p in pdf.pages)
    assert 'Parte A - Sumário executivo' in text
    assert 'Parte B - Relatório técnico' in text
    assert 'Parte C - Diário de decisões' in text
    assert 'AUTORAIS PENDENTES' in text


def test_unchanged_inputs_generate_identical_pdf():
    command = [sys.executable, str(ROOT / 'scripts/gerar_relatorio.py')]
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
    first = hashlib.sha256((ROOT / 'reports/relatorio_final.pdf').read_bytes()).hexdigest()
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
    assert hashlib.sha256((ROOT / 'reports/relatorio_final.pdf').read_bytes()).hexdigest() == first
