"""
IDF Footballers Dataset Explorer

Interactive Streamlit app to explore the Île-de-France footballers dataset.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datasets import load_dataset

# Page config
st.set_page_config(
    page_title="IDF Footballers Dataset",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Department info with correct coordinates
DEPARTMENTS = {
    75: {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    77: {"name": "Seine-et-Marne", "lat": 48.8400, "lon": 2.9900},
    78: {"name": "Yvelines", "lat": 48.7800, "lon": 1.9900},
    91: {"name": "Essonne", "lat": 48.5300, "lon": 2.2300},
    92: {"name": "Hauts-de-Seine", "lat": 48.8500, "lon": 2.2200},
    93: {"name": "Seine-Saint-Denis", "lat": 48.9200, "lon": 2.4500},
    94: {"name": "Val-de-Marne", "lat": 48.7900, "lon": 2.4700},
    95: {"name": "Val-d'Oise", "lat": 49.0700, "lon": 2.1500},
}


@st.cache_data(ttl=3600)  # Cache for 1 hour max
def load_data():
    """Load and cache the dataset from HuggingFace."""
    dataset = load_dataset("ironlam/idf-footballers", split="train", download_mode="force_redownload")
    df = dataset.to_pandas()

    # Drop rows with missing department (can't map them)
    df = df.dropna(subset=['birth_department'])

    # Ensure department is integer
    df['birth_department'] = df['birth_department'].astype(int)

    # Parse list fields - handle string, list, and numpy array formats
    def parse_list_field(x):
        if x is None:
            return []
        if isinstance(x, list):
            return x
        if isinstance(x, str):
            if x == '[]' or x == '':
                return []
            try:
                result = eval(x)
                return result if isinstance(result, list) else []
            except:
                return []
        # Handle numpy arrays or other iterables
        try:
            return list(x)
        except:
            return []

    df['nationalities'] = df['nationalities'].apply(parse_list_field)
    df['diaspora_countries'] = df['diaspora_countries'].apply(parse_list_field)

    # Fill NaN values
    df['diaspora_region'] = df['diaspora_region'].fillna('None')
    df['birth_city'] = df['birth_city'].fillna('Unknown')

    return df


def get_dept_label(dept_code):
    """Get department label like '93 - Seine-Saint-Denis'"""
    dept_int = int(dept_code)
    name = DEPARTMENTS.get(dept_int, {}).get("name", "")
    return f"{dept_int} - {name}" if name else str(dept_int)


def main():
    # Load data
    df = load_data()

    # Header
    st.title("⚽ IDF Footballers Dataset")
    st.markdown("*Exploring professional footballers born in Île-de-France (1980-2006)*")

    # Debug info (temporary)
    with st.expander("🔧 Debug Info"):
        st.write(f"**Total rows loaded:** {len(df)}")
        st.write(f"**birth_department dtype:** {df['birth_department'].dtype}")
        dept_vc = df['birth_department'].value_counts()
        st.write(f"**Department counts:** {dict(zip([int(x) for x in dept_vc.index], [int(x) for x in dept_vc.values]))}")
        dias_vc = df['diaspora_region'].value_counts(dropna=False)
        st.write(f"**Diaspora counts:** {dict(zip([str(x) for x in dias_vc.index], [int(x) for x in dias_vc.values]))}")

    # Methodology expander
    with st.expander("ℹ️ About this data & methodology"):
        st.markdown("""
        ### Data Source
        This dataset was collected from **Wikidata** using SPARQL queries. It includes professional footballers
        (association football players) born in Île-de-France between 1980 and 2006.

        ### Key Definitions

        | Term | Definition |
        |------|------------|
        | **Dual National** | Player with **2+ citizenships recorded** in Wikidata. This is based on legal nationality, not ancestry. |
        | **African Diaspora** | Player holding citizenship from an African country (not just French). Does NOT capture heritage if player only has French citizenship. |
        | **Birthplace** | Where the player was **born** (often a hospital), not necessarily where they grew up. |

        ### Important Limitations

        ⚠️ **Citizenship ≠ Heritage**: A player like Paul Pogba (parents from Guinea) appears as "French only" because
        he doesn't hold Guinean citizenship. Kylian Mbappé shows France + Cameroon (father's nationality) but not Algeria (mother's origin).

        ⚠️ **Birthplace ≠ Childhood**: Mbappé is listed as born in Paris 19e, but grew up in Bondy (93).

        ⚠️ **Wikidata coverage**: Only players notable enough to have a Wikipedia/Wikidata entry are included.

        ⚠️ **~90 players** have unknown departments (birthplace couldn't be mapped to a département).

        ### What this data CAN tell us
        - Geographic distribution of professional footballers across IDF
        - Minimum bounds on diaspora representation (actual heritage is higher)
        - Trends over time (birth years)

        ### What this data CANNOT tell us
        - Full ancestral/heritage backgrounds
        - Where players actually grew up or trained
        - Career success levels (all pros counted equally)
        """)

    st.divider()

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Department filter
    dept_options = ["All"] + [get_dept_label(d) for d in sorted(DEPARTMENTS.keys())]
    selected_dept_display = st.sidebar.selectbox("Department", dept_options)

    if selected_dept_display == "All":
        selected_dept = "All"
    else:
        selected_dept = int(selected_dept_display.split(" - ")[0])

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
        filtered_df = filtered_df[filtered_df['birth_department'] == selected_dept]

    if selected_diaspora != "All":
        filtered_df = filtered_df[filtered_df['diaspora_region'] == selected_diaspora]

    filtered_df = filtered_df[
        (filtered_df['birth_year'] >= year_range[0]) &
        (filtered_df['birth_year'] <= year_range[1])
    ]

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
        st.metric("Dual Nationals", f"{dual_pct:.1f}%", help="Players with 2+ citizenships recorded in Wikidata.")

    with col3:
        african_regions = ['Sub-Saharan Africa', 'Maghreb', 'Comoros']
        african_diaspora_count = len(filtered_df[filtered_df['diaspora_region'].isin(african_regions)])
        african_diaspora_pct = (african_diaspora_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("African Diaspora*", f"{african_diaspora_pct:.1f}%", help="Includes Sub-Saharan Africa, Maghreb, Comoros. Based on citizenship only.")

    with col4:
        if len(filtered_df) > 0:
            top_dept = filtered_df['birth_department'].mode().iloc[0]
            top_dept_name = DEPARTMENTS.get(int(top_dept), {}).get("name", str(top_dept))
        else:
            top_dept_name = "N/A"
        st.metric("Top Department", top_dept_name)

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Players by Department")

        # Use value_counts directly on the filtered data
        dept_counts = filtered_df['birth_department'].value_counts()

        if len(dept_counts) > 0:
            labels = [get_dept_label(int(d)) for d in dept_counts.index]
            counts = [int(c) for c in dept_counts.values]

            fig = go.Figure(data=[
                go.Bar(y=labels, x=counts, orientation='h', marker_color='steelblue', text=counts, textposition='outside')
            ])
            fig.update_layout(
                xaxis_title="Number of Players",
                yaxis_title="",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(categoryorder='total ascending')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data for current filters")

    with col2:
        st.subheader("🌍 Diaspora Regions")
        # Filter out None/NaN values and count
        diaspora_df = filtered_df[filtered_df['diaspora_region'].notna() & (filtered_df['diaspora_region'] != 'None')]
        diaspora_counts = diaspora_df['diaspora_region'].value_counts()

        if len(diaspora_counts) > 0:
            names = diaspora_counts.index.tolist()
            values = [int(v) for v in diaspora_counts.values]

            fig = go.Figure(data=[
                go.Pie(labels=names, values=values, hole=0.4, textinfo='percent+label', textposition='inside')
            ])
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No diaspora data for current filters")

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Birth Year Distribution")
        year_counts = filtered_df['birth_year'].value_counts().sort_index()

        if len(year_counts) > 0:
            years = [int(y) for y in year_counts.index]
            counts = [int(c) for c in year_counts.values]

            fig = go.Figure(data=[
                go.Bar(x=years, y=counts, marker_color='green')
            ])
            fig.update_layout(
                xaxis_title='Birth Year',
                yaxis_title='Number of Players',
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(tickmode='linear', dtick=5)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No birth year data for current filters")

    with col2:
        st.subheader("🏆 Top Origin Countries")
        # Flatten diaspora countries
        all_countries = []
        for countries in filtered_df['diaspora_countries']:
            if isinstance(countries, list):
                all_countries.extend(countries)

        if all_countries:
            country_counts = pd.Series(all_countries).value_counts().head(10)
            names = country_counts.index.tolist()
            values = [int(v) for v in country_counts.values]

            fig = go.Figure(data=[
                go.Bar(y=names, x=values, orientation='h', marker_color='orange', text=values, textposition='outside')
            ])
            fig.update_layout(
                xaxis_title="Number of Players",
                yaxis_title="",
                height=350,
                yaxis=dict(categoryorder='total ascending'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No origin country data for current filters")

    st.divider()

    # Map
    st.subheader("🗺️ Geographic Distribution")

    # Prepare map data
    map_data = []
    for dept_code, info in DEPARTMENTS.items():
        count = len(filtered_df[filtered_df['birth_department'] == dept_code])
        if count > 0:
            map_data.append({
                'department': str(dept_code),
                'name': f"{dept_code} - {info['name']}",
                'lat': info['lat'],
                'lon': info['lon'],
                'count': count
            })

    if map_data:
        map_df = pd.DataFrame(map_data)

        # Scale marker sizes (min 15, max 60)
        max_count = map_df['count'].max()
        sizes = [max(15, int(40 * c / max_count) + 15) for c in map_df['count']]

        fig = go.Figure(go.Scattermapbox(
            lat=map_df['lat'].tolist(),
            lon=map_df['lon'].tolist(),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=sizes,
                color=map_df['count'].tolist(),
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title='Players')
            ),
            text=map_df['name'].tolist(),
            hoverinfo='text+name',
            customdata=map_df['count'].tolist(),
            hovertemplate='%{text}<br>Players: %{customdata}<extra></extra>'
        ))

        fig.update_layout(
            mapbox=dict(
                style='carto-positron',
                center=dict(lat=48.85, lon=2.35),
                zoom=9
            ),
            height=500,
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No geographic data for current filters")

    st.divider()

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
    display_df_show['Department'] = display_df_show['Department'].apply(lambda x: get_dept_label(x))
    display_df_show['Dual National'] = display_df_show['Dual National'].apply(lambda x: '✓' if x else '')
    display_df_show['Diaspora Region'] = display_df_show['Diaspora Region'].apply(lambda x: x if x != 'None' else '-')

    st.dataframe(
        display_df_show.sort_values('Name'),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download filtered data (CSV)",
        data=csv,
        file_name="idf_footballers_filtered.csv",
        mime="text/csv"
    )

    # Footer
    st.divider()
    st.markdown("""
    **Data source:** [Wikidata](https://www.wikidata.org) |
    **Dataset:** [HuggingFace](https://huggingface.co/datasets/ironlam/idf-footballers) |
    **Code:** [GitHub](https://github.com/ironlam/psg-diaspora-dataset) |
    **Article:** [Medium](https://medium.com/@diaby.lamine)

    *Built by Lamine DIABY*
    """)


if __name__ == "__main__":
    main()
