"""
IDF Footballers Dataset Explorer

Interactive Streamlit app to explore the Île-de-France footballers dataset.

Run with: streamlit run app/app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="IDF Footballers Dataset",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache the dataset."""
    data_path = Path(__file__).parent.parent / "data" / "huggingface" / "idf_footballers.csv"
    df = pd.read_csv(data_path)

    # Parse nationalities from string representation
    df['nationalities'] = df['nationalities'].apply(lambda x: eval(x) if pd.notna(x) else [])
    df['diaspora_countries'] = df['diaspora_countries'].apply(lambda x: eval(x) if pd.notna(x) and x != '[]' else [])

    # Fill NaN values
    df['diaspora_region'] = df['diaspora_region'].fillna('None')
    df['birth_city'] = df['birth_city'].fillna('Unknown')

    return df


# Department coordinates for map (approximate centroids)
DEPT_COORDS = {
    "75": {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    "77": {"name": "Seine-et-Marne", "lat": 48.6200, "lon": 2.9800},
    "78": {"name": "Yvelines", "lat": 48.8000, "lon": 1.8500},
    "91": {"name": "Essonne", "lat": 48.5200, "lon": 2.2400},
    "92": {"name": "Hauts-de-Seine", "lat": 48.8400, "lon": 2.2500},
    "93": {"name": "Seine-Saint-Denis", "lat": 48.9100, "lon": 2.4800},
    "94": {"name": "Val-de-Marne", "lat": 48.7800, "lon": 2.4700},
    "95": {"name": "Val-d'Oise", "lat": 49.0500, "lon": 2.1700},
}


def main():
    # Load data
    df = load_data()

    # Header
    st.markdown('<p class="main-header">⚽ IDF Footballers Dataset</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Exploring 1,165 professional footballers born in Île-de-France (1980-2006)</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Department filter
    departments = ["All"] + sorted(df['birth_department'].unique().tolist())
    dept_names = {str(d): DEPT_COORDS.get(str(d), {}).get("name", str(d)) for d in departments if d != "All"}
    dept_options = ["All"] + [f"{d} - {dept_names.get(str(d), d)}" for d in departments if d != "All"]
    selected_dept_display = st.sidebar.selectbox("Department", dept_options)
    selected_dept = "All" if selected_dept_display == "All" else selected_dept_display.split(" - ")[0]

    # Diaspora filter
    diaspora_regions = ["All"] + sorted([r for r in df['diaspora_region'].unique() if r != 'None'])
    selected_diaspora = st.sidebar.selectbox("Diaspora Region", diaspora_regions)

    # Birth year range
    min_year, max_year = int(df['birth_year'].min()), int(df['birth_year'].max())
    year_range = st.sidebar.slider("Birth Year Range", min_year, max_year, (min_year, max_year))

    # Dual nationality filter
    dual_national_filter = st.sidebar.radio("Nationality", ["All", "Dual nationals only", "Single nationality only"])

    # Apply filters
    filtered_df = df.copy()

    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df['birth_department'] == int(selected_dept)]

    if selected_diaspora != "All":
        filtered_df = filtered_df[filtered_df['diaspora_region'] == selected_diaspora]

    filtered_df = filtered_df[(filtered_df['birth_year'] >= year_range[0]) & (filtered_df['birth_year'] <= year_range[1])]

    if dual_national_filter == "Dual nationals only":
        filtered_df = filtered_df[filtered_df['is_dual_national'] == True]
    elif dual_national_filter == "Single nationality only":
        filtered_df = filtered_df[filtered_df['is_dual_national'] == False]

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Players", f"{len(filtered_df):,}")

    with col2:
        dual_pct = (filtered_df['is_dual_national'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Dual Nationals", f"{dual_pct:.1f}%")

    with col3:
        diaspora_count = len(filtered_df[filtered_df['diaspora_region'] != 'None'])
        diaspora_pct = (diaspora_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("African Diaspora", f"{diaspora_pct:.1f}%")

    with col4:
        top_dept = filtered_df['birth_department'].mode().iloc[0] if len(filtered_df) > 0 else "N/A"
        top_dept_name = DEPT_COORDS.get(str(top_dept), {}).get("name", str(top_dept))
        st.metric("Top Department", top_dept_name)

    st.markdown("---")

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Players by Department")
        dept_counts = filtered_df['birth_department'].value_counts().reset_index()
        dept_counts.columns = ['department', 'count']
        dept_counts['name'] = dept_counts['department'].apply(
            lambda x: f"{x} - {DEPT_COORDS.get(str(x), {}).get('name', str(x))}"
        )

        fig = px.bar(
            dept_counts.sort_values('count', ascending=True),
            x='count',
            y='name',
            orientation='h',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="Number of Players",
            yaxis_title="",
            coloraxis_showscale=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🌍 Diaspora Regions")
        diaspora_counts = filtered_df[filtered_df['diaspora_region'] != 'None']['diaspora_region'].value_counts()

        if len(diaspora_counts) > 0:
            fig = px.pie(
                values=diaspora_counts.values,
                names=diaspora_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No diaspora data for current filters")

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Birth Year Distribution")
        year_counts = filtered_df['birth_year'].value_counts().sort_index()

        fig = px.area(
            x=year_counts.index,
            y=year_counts.values,
            labels={'x': 'Birth Year', 'y': 'Number of Players'}
        )
        fig.update_layout(height=350)
        fig.update_traces(fill='tozeroy', line_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🏆 Top Origin Countries")
        # Flatten diaspora countries
        all_countries = []
        for countries in filtered_df['diaspora_countries']:
            all_countries.extend(countries)

        if all_countries:
            country_counts = pd.Series(all_countries).value_counts().head(10)

            fig = px.bar(
                x=country_counts.values,
                y=country_counts.index,
                orientation='h',
                color=country_counts.values,
                color_continuous_scale='Oranges'
            )
            fig.update_layout(
                xaxis_title="Number of Players",
                yaxis_title="",
                coloraxis_showscale=False,
                height=350,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No origin country data for current filters")

    st.markdown("---")

    # Map
    st.subheader("🗺️ Geographic Distribution")

    # Prepare map data
    map_data = []
    for dept, info in DEPT_COORDS.items():
        count = len(filtered_df[filtered_df['birth_department'] == int(dept)])
        if count > 0:
            map_data.append({
                'department': dept,
                'name': info['name'],
                'lat': info['lat'],
                'lon': info['lon'],
                'count': count
            })

    if map_data:
        map_df = pd.DataFrame(map_data)

        fig = px.scatter_mapbox(
            map_df,
            lat='lat',
            lon='lon',
            size='count',
            color='count',
            hover_name='name',
            hover_data={'count': True, 'lat': False, 'lon': False},
            color_continuous_scale='Viridis',
            size_max=50,
            zoom=9,
            center={'lat': 48.85, 'lon': 2.35}
        )
        fig.update_layout(
            mapbox_style='carto-positron',
            height=500,
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Data table
    st.subheader("📋 Player Data")

    # Search
    search = st.text_input("🔎 Search by name", "")

    display_df = filtered_df.copy()
    if search:
        display_df = display_df[display_df['name'].str.contains(search, case=False, na=False)]

    # Format for display
    display_cols = ['name', 'birth_year', 'birth_city', 'birth_department', 'diaspora_region', 'is_dual_national']
    display_df_show = display_df[display_cols].copy()
    display_df_show.columns = ['Name', 'Birth Year', 'Birth City', 'Department', 'Diaspora Region', 'Dual National']
    display_df_show['Department'] = display_df_show['Department'].apply(
        lambda x: f"{x} - {DEPT_COORDS.get(str(x), {}).get('name', str(x))}"
    )
    display_df_show['Dual National'] = display_df_show['Dual National'].apply(lambda x: '✓' if x else '')
    display_df_show['Diaspora Region'] = display_df_show['Diaspora Region'].apply(lambda x: x if x != 'None' else '-')

    st.dataframe(
        display_df_show.sort_values('Name'),
        use_container_width=True,
        height=400
    )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Data source: <a href="https://www.wikidata.org" target="_blank">Wikidata</a> |
        Dataset: <a href="https://huggingface.co/datasets/ldiaby/idf-footballers" target="_blank">HuggingFace</a> |
        Code: <a href="https://github.com/ldiaby/psg-diaspora-dataset" target="_blank">GitHub</a></p>
        <p>Built by Lamine DIABY</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
