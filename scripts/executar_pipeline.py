"""Executar: python scripts/executar_pipeline.py --input data/raw --output ."""
# [IA] registro 3
import argparse
import sys
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.load_data import load_data
from src.preprocessing import preprocessar
from src.reporting import write_outputs


def main():
    parser = argparse.ArgumentParser(description='Pré-processar os cinco CSVs originais da Olist.')
    parser.add_argument('--input', type=Path, default=ROOT / 'data/raw')
    parser.add_argument('--output', type=Path, default=ROOT)
    parser.add_argument('--sem-graficos', action='store_true')
    args = parser.parse_args()
    started = time.perf_counter()
    try:
        raw = load_data(args.input)
        d = preprocessar(*raw)
        metadata = write_outputs(d, raw, args.output, charts=not args.sem_graficos)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Pipeline não concluído: {error}\n')
    print(f'CSV gerado: {metadata["rows"]} linhas, {metadata["columns"]} colunas, {metadata["bytes"]} bytes.')
    print(f'Pedidos elegíveis: {d.eligible_dispatch.sum()}. Tempo: {time.perf_counter()-started:.1f} s.')
    print('Evidências técnicas geradas. Conclusões e justificativas humanas continuam pendentes.')


if __name__ == '__main__':
    main()
