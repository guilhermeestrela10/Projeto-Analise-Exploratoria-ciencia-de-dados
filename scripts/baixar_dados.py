"""Baixa somente os cinco CSVs autorizados do pacote público Olist."""
# [IA] registro 3
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
FILES = ['orders', 'order_items', 'products', 'sellers', 'order_reviews']
URL = 'https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce'


def main():
    target = ROOT / 'data/raw'
    target.mkdir(parents=True, exist_ok=True)
    names = [f'olist_{name}_dataset.csv' for name in FILES]
    existing = [name for name in names if (target / name).exists()]
    if existing:
        raise SystemExit('Arquivos já presentes; preservados: ' + ', '.join(existing))
    try:
        with urlopen(URL, timeout=120) as response:
            archive = ZipFile(io.BytesIO(response.read()))
        content = {name: archive.read(name) for name in names}
    except Exception as error:
        raise SystemExit(f'Não foi possível baixar: {error}. Baixe os cinco CSVs pelo Kaggle e coloque em data/raw.') from error
    records = []
    for name, value in content.items():
        (target / name).write_bytes(value)
        records.append({'file': name, 'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()})
    (target / 'proveniencia.json').write_text(json.dumps({
        'url': URL, 'download_date': datetime.now(timezone.utc).isoformat(), 'files': records
    }, indent=2), encoding='utf-8')
    print('Cinco CSVs extraídos; geolocalização não extraída.')


if __name__ == '__main__':
    main()
