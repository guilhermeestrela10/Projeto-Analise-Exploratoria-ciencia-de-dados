"""Gráficos descritivos sem interpretações de negócio automáticas."""
# [IA] registro 2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from .analysis import seller_metrics, review_comparison

sns.set_theme(style='whitegrid', palette=['#087F8C', '#E58F37', '#405B80'])


def ranking_chart(metrics):
    fig, ax = plt.subplots(figsize=(10, 5))
    top = metrics.head(12).iloc[::-1]
    if not top.empty:
        labels = top.seller_id.str[:10] + '…'
        ax.barh(labels, top.late_rate * 100, color='#087F8C')
    ax.set(xlabel='Despachos atrasados entre pedidos elegíveis (%)', ylabel='Vendedor (ID abreviado)', xlim=(0, 100))
    ax.set_title('Taxa de atraso por vendedor no recorte')
    fig.tight_layout()
    return fig


def review_chart(comparison):
    fig, ax = plt.subplots(figsize=(8, 4))
    if not comparison.empty:
        labels = comparison.dispatch_late.map({0: 'Sem atraso observado', 1: 'Com atraso observado'})
        ax.bar(labels, comparison.mean_score, color=['#087F8C', '#E58F37'][:len(comparison)])
        for j, row in enumerate(comparison.itertuples()):
            ax.text(j, row.mean_score + .08, f'n = {row.review_count:,}', ha='center')
    ax.set(ylabel='Nota média (1 a 5)', ylim=(0, 5.6), title='Avaliações dos pedidos elegíveis')
    fig.tight_layout()
    return fig


def save_charts(d, folder):
    folder.mkdir(parents=True, exist_ok=True)
    metrics = seller_metrics(d)
    figures = {'ranking': ranking_chart(metrics[metrics.eligible_orders.ge(30)]),
               'avaliacoes': review_chart(review_comparison(d))}
    e = d.loc[d.eligible_dispatch]
    fig, ax = plt.subplots(figsize=(9, 4))
    values = e.approval_to_carrier_days.dropna()
    if not values.empty:
        ax.hist(values, bins=60, color='#087F8C')
        ax.set_yscale('log')
    ax.set(xlabel='Dias entre aprovação e transportadora (sem corte)', ylabel='Pedidos (escala log)', title='Distribuição completa do tempo até despacho')
    fig.tight_layout()
    figures['distribuicao'] = fig
    fig, ax = plt.subplots(figsize=(10, 4))
    monthly = e.groupby('purchase_month').dispatch_late.agg(['mean', 'count'])
    if not monthly.empty:
        ax.plot(monthly.index, monthly['mean'] * 100, marker='o', color='#087F8C')
    ax.tick_params(axis='x', rotation=60)
    ax.set(ylabel='Atrasos (%)', xlabel='Mês da compra', title='Taxa mensal de atraso - pedidos elegíveis')
    fig.tight_layout()
    figures['temporal'] = fig
    fig, ax = plt.subplots(figsize=(7, 5))
    cols = ['approval_to_carrier_days', 'dispatch_delay_days', 'delivery_days', 'review_score']
    corr = e[cols].apply(lambda x: x.astype(float)).corr()
    if corr.notna().any().any():
        sns.heatmap(corr, annot=True, fmt='.2f', vmin=-1, vmax=1, cmap='BrBG', ax=ax)
    ax.set_title('Correlação de Pearson - pares completos')
    fig.tight_layout()
    figures['correlacao'] = fig
    for name, figure in figures.items():
        figure.savefig(folder / f'{name}.png', dpi=160, bbox_inches='tight')
        plt.close(figure)
    return list(figures)
