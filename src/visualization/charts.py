"""
Visualization charts for IDF footballers dataset.
Generates static charts for the article and exports.
"""

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150


def load_analysis():
    """Load analysis results."""
    path = Path(__file__).parent.parent.parent / "data" / "processed" / "analysis_results.json"
    with open(path) as f:
        return json.load(f)


def chart_diaspora_regions(results: dict, output_dir: Path):
    """Pie chart of diaspora regions."""
    data = results["diaspora"]["by_region"]

    # Add "French only" category
    total = results["demographics"]["total_players"]
    diaspora_total = sum(data.values())
    french_only = total - diaspora_total

    labels = list(data.keys()) + ["French only"]
    sizes = list(data.values()) + [french_only]

    # Colors
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#95a5a6']

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors[:len(sizes)],
        startangle=90,
        pctdistance=0.75
    )

    ax.set_title('Origins of Île-de-France Professional Footballers\n(Born 1980-2006)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / "diaspora_regions_pie.png", bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: diaspora_regions_pie.png")


def chart_top_countries(results: dict, output_dir: Path):
    """Horizontal bar chart of top origin countries."""
    data = dict(list(results["diaspora"]["by_country"].items())[:10])

    countries = list(data.keys())[::-1]  # Reverse for horizontal bar
    counts = list(data.values())[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(countries, counts, color='#3498db')

    # Add value labels
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontsize=10)

    ax.set_xlabel('Number of Players', fontsize=12)
    ax.set_title('Top Origin Countries (besides France)\nÎle-de-France Footballers 1980-2006', fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(counts) * 1.15)

    plt.tight_layout()
    plt.savefig(output_dir / "top_countries_bar.png", bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: top_countries_bar.png")


def chart_birth_years(results: dict, output_dir: Path):
    """Line/area chart of birth years."""
    data = {int(k): v for k, v in results["temporal"]["by_5year"].items()}

    periods = [f"{k}-{k+4}" for k in sorted(data.keys())]
    counts = [data[k] for k in sorted(data.keys())]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(range(len(periods)), counts, alpha=0.3, color='#2ecc71')
    ax.plot(range(len(periods)), counts, marker='o', linewidth=2, color='#27ae60', markersize=8)

    ax.set_xticks(range(len(periods)))
    ax.set_xticklabels(periods, rotation=0)
    ax.set_xlabel('Birth Period', fontsize=12)
    ax.set_ylabel('Number of Players', fontsize=12)
    ax.set_title('Île-de-France Footballer Production by Birth Year', fontsize=14, fontweight='bold')

    # Add peak annotation
    max_idx = counts.index(max(counts))
    ax.annotate(f'Peak: {max(counts)} players',
                xy=(max_idx, max(counts)),
                xytext=(max_idx + 0.5, max(counts) + 10),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=10)

    plt.tight_layout()
    plt.savefig(output_dir / "birth_years_trend.png", bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: birth_years_trend.png")


def chart_departments(results: dict, output_dir: Path):
    """Bar chart of players by département."""
    data = results["geographic"]["by_department"]

    # Sort by count
    sorted_depts = sorted(data.items(), key=lambda x: x[1]["count"], reverse=True)

    names = [f"{v['name']} ({k})" for k, v in sorted_depts]
    counts = [v["count"] for _, v in sorted_depts]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(range(len(names)), counts, color='#e74c3c')

    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_ylabel('Number of Players', fontsize=12)
    ax.set_title('Players by Département\n(⚠️ 93 and 95 data missing due to rate limiting)', fontsize=14, fontweight='bold')

    # Add value labels
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                str(count), ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_dir / "departments_bar.png", bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: departments_bar.png")


def chart_dual_nationality(results: dict, output_dir: Path):
    """Donut chart of dual nationality."""
    dual = results["demographics"]["dual_nationals"]
    single = results["demographics"]["total_players"] - dual

    fig, ax = plt.subplots(figsize=(8, 8))

    sizes = [dual, single]
    labels = [f'Dual Nationals\n({dual})', f'Single Nationality\n({single})']
    colors = ['#3498db', '#ecf0f1']

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5)  # Donut
    )

    ax.set_title('Dual Nationality Among IDF Footballers', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / "dual_nationality_donut.png", bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: dual_nationality_donut.png")


def create_summary_infographic(results: dict, output_dir: Path):
    """Create a summary infographic."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Île-de-France Footballers: Diaspora Analysis\n(1980-2006 Birth Cohorts)',
                 fontsize=16, fontweight='bold', y=1.02)

    # 1. Total players (big number)
    ax1 = axes[0, 0]
    ax1.text(0.5, 0.5, f"{results['demographics']['total_players']}",
             fontsize=60, fontweight='bold', ha='center', va='center', color='#2c3e50')
    ax1.text(0.5, 0.15, 'Professional Footballers', fontsize=14, ha='center', va='center', color='#7f8c8d')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')

    # 2. Dual nationals percentage
    ax2 = axes[0, 1]
    ax2.text(0.5, 0.5, f"{results['demographics']['dual_national_pct']}%",
             fontsize=50, fontweight='bold', ha='center', va='center', color='#3498db')
    ax2.text(0.5, 0.15, 'Dual Nationals', fontsize=14, ha='center', va='center', color='#7f8c8d')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')

    # 3. African diaspora percentage
    ax3 = axes[0, 2]
    ax3.text(0.5, 0.5, f"{results['diaspora']['diaspora_pct']}%",
             fontsize=50, fontweight='bold', ha='center', va='center', color='#27ae60')
    ax3.text(0.5, 0.15, 'African Diaspora', fontsize=14, ha='center', va='center', color='#7f8c8d')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')

    # 4. Top countries bar
    ax4 = axes[1, 0]
    top5 = dict(list(results["diaspora"]["by_country"].items())[:5])
    countries = list(top5.keys())[::-1]
    counts = list(top5.values())[::-1]
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6'][::-1]
    ax4.barh(countries, counts, color=colors)
    ax4.set_xlabel('Players')
    ax4.set_title('Top 5 Origin Countries', fontsize=12, fontweight='bold')

    # 5. Diaspora regions pie
    ax5 = axes[1, 1]
    regions = results["diaspora"]["by_region"]
    ax5.pie(regions.values(), labels=regions.keys(), autopct='%1.0f%%',
            colors=['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c'][:len(regions)])
    ax5.set_title('Diaspora Regions', fontsize=12, fontweight='bold')

    # 6. Birth trend
    ax6 = axes[1, 2]
    data = {int(k): v for k, v in results["temporal"]["by_5year"].items()}
    periods = [f"{k}-{k+4}" for k in sorted(data.keys())]
    counts = [data[k] for k in sorted(data.keys())]
    ax6.fill_between(range(len(periods)), counts, alpha=0.3, color='#3498db')
    ax6.plot(range(len(periods)), counts, marker='o', color='#2980b9')
    ax6.set_xticks(range(len(periods)))
    ax6.set_xticklabels(periods, rotation=45, fontsize=8)
    ax6.set_title('Birth Year Trend', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / "summary_infographic.png", bbox_inches='tight', facecolor='white', dpi=150)
    plt.close()
    print(f"  Saved: summary_infographic.png")


def main():
    """Generate all charts."""
    print("=" * 60)
    print("Generating Visualizations")
    print("=" * 60)

    # Load data
    results = load_analysis()

    # Output directory
    output_dir = Path(__file__).parent.parent.parent / "docs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nOutput directory: {output_dir}")
    print("\nGenerating charts...")

    # Generate all charts
    chart_diaspora_regions(results, output_dir)
    chart_top_countries(results, output_dir)
    chart_birth_years(results, output_dir)
    chart_departments(results, output_dir)
    chart_dual_nationality(results, output_dir)
    create_summary_infographic(results, output_dir)

    print("\n" + "=" * 60)
    print("All charts generated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
