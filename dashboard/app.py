import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import re

# Configuración de la página
st.set_page_config(
    page_title="Remote Jobs Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: white;
    }
    .stMetric {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)


def parse_salary(salary_str):
    """Extrae valores numéricos del string de salario."""
    if pd.isna(salary_str) or salary_str == "":
        return None, None
    
    # Limpiar el string
    salary_str = str(salary_str).lower().replace(",", "").replace(" ", "")
    
    # Buscar valores con k (miles)
    numbers = re.findall(r'\$?(\d+)k?', salary_str)
    
    if not numbers:
        return None, None
    
    values = []
    for num in numbers:
        val = int(num)
        # Si el número es pequeño, probablemente está en miles
        if val < 1000 and 'k' in salary_str:
            val = val * 1000
        elif val < 500:  # Asumimos que está en K
            val = val * 1000
        values.append(val)
    
    if len(values) >= 2:
        return min(values), max(values)
    elif len(values) == 1:
        return values[0], values[0]
    
    return None, None


@st.cache_data(ttl=60)
def load_data():
    """Carga los datos del CSV."""
    # Rutas posibles (Docker y local)
    paths = [
        Path("/app/data/jobs.csv"),  # Docker
        Path("../dags/data/processed/jobs.csv"),  # Local relativo
        Path("dags/data/processed/jobs.csv"),  # Local desde raíz
        Path("/opt/airflow/dags/data/processed/jobs.csv"),  # Airflow container
    ]
    
    for path in paths:
        if path.exists():
            df = pd.read_csv(path)
            break
    else:
        # Datos de ejemplo si no encuentra el archivo
        st.warning("⚠️ No se encontró el archivo de datos. Mostrando datos de ejemplo.")
        df = pd.DataFrame({
            'title': ['Data Engineer', 'Python Developer', 'DevOps Engineer'],
            'company': ['TechCorp', 'StartupABC', 'CloudInc'],
            'category': ['Software Development', 'Software Development', 'DevOps'],
            'salary': ['$80k-$120k', '$60k-$90k', '$70k-$100k'],
            'url': ['https://example.com'] * 3,
            'pub_date': ['2025-01-01', '2025-01-02', '2025-01-03']
        })
    
    # Procesar datos
    df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce')
    df['has_salary'] = df['salary'].notna() & (df['salary'] != '')
    
    # Extraer salarios
    salary_data = df['salary'].apply(lambda x: pd.Series(parse_salary(x)))
    df['salary_min'] = salary_data[0]
    df['salary_max'] = salary_data[1]
    df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
    
    return df


def main():
    # Header
    st.markdown('<p class="main-header">💼 Remote Jobs Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Análisis de ofertas de trabajo remoto extraídas por Airflow ETL</p>', unsafe_allow_html=True)
    
    # Cargar datos
    df = load_data()
    
    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por categoría
    categories = ['Todas'] + sorted(df['category'].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Categoría", categories)
    
    # Filtro por empresa
    companies = ['Todas'] + sorted(df['company'].dropna().unique().tolist())
    selected_company = st.sidebar.selectbox("Empresa", companies)
    
    # Filtro por salario
    show_with_salary = st.sidebar.checkbox("Solo con salario publicado", False)
    
    # Aplicar filtros
    df_filtered = df.copy()
    if selected_category != 'Todas':
        df_filtered = df_filtered[df_filtered['category'] == selected_category]
    if selected_company != 'Todas':
        df_filtered = df_filtered[df_filtered['company'] == selected_company]
    if show_with_salary:
        df_filtered = df_filtered[df_filtered['has_salary']]
    
    # Métricas principales
    st.markdown("### 📊 Métricas Generales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Trabajos",
            value=len(df_filtered),
            delta=f"de {len(df)} total" if len(df_filtered) != len(df) else None
        )
    
    with col2:
        with_salary = df_filtered['has_salary'].sum()
        pct = (with_salary / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.metric(
            label="Con Salario",
            value=with_salary,
            delta=f"{pct:.0f}%"
        )
    
    with col3:
        st.metric(
            label="Empresas",
            value=df_filtered['company'].nunique()
        )
    
    with col4:
        avg_salary = df_filtered['salary_avg'].mean()
        if pd.notna(avg_salary):
            st.metric(
                label="Salario Promedio",
                value=f"${avg_salary/1000:.0f}k"
            )
        else:
            st.metric(label="Salario Promedio", value="N/A")
    
    st.markdown("---")
    
    # Gráficos
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📁 Trabajos por Categoría")
        category_counts = df_filtered['category'].value_counts().reset_index()
        category_counts.columns = ['Categoría', 'Cantidad']
        
        fig_cat = px.bar(
            category_counts,
            x='Cantidad',
            y='Categoría',
            orientation='h',
            color='Cantidad',
            color_continuous_scale='Viridis'
        )
        fig_cat.update_layout(
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col_right:
        st.markdown("### 🏢 Top 10 Empresas")
        company_counts = df_filtered['company'].value_counts().head(10).reset_index()
        company_counts.columns = ['Empresa', 'Ofertas']
        
        fig_comp = px.pie(
            company_counts,
            values='Ofertas',
            names='Empresa',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_comp.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Análisis de salarios
    st.markdown("### 💰 Análisis de Salarios")
    
    df_with_salary = df_filtered[df_filtered['salary_avg'].notna()]
    
    if len(df_with_salary) > 0:
        col_sal1, col_sal2 = st.columns(2)
        
        with col_sal1:
            fig_salary = px.histogram(
                df_with_salary,
                x='salary_avg',
                nbins=20,
                labels={'salary_avg': 'Salario Anual (USD)'},
                color_discrete_sequence=['#667eea']
            )
            fig_salary.update_layout(
                title="Distribución de Salarios",
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig_salary, use_container_width=True)
        
        with col_sal2:
            # Box plot por categoría
            fig_box = px.box(
                df_with_salary,
                x='category',
                y='salary_avg',
                color='category',
                labels={'salary_avg': 'Salario (USD)', 'category': 'Categoría'}
            )
            fig_box.update_layout(
                title="Salarios por Categoría",
                showlegend=False,
                height=350,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("No hay datos de salario disponibles para mostrar.")
    
    # Timeline de publicaciones
    st.markdown("### 📅 Timeline de Publicaciones")
    
    df_timeline = df_filtered.dropna(subset=['pub_date'])
    if len(df_timeline) > 0:
        timeline = df_timeline.groupby(df_timeline['pub_date'].dt.date).size().reset_index()
        timeline.columns = ['Fecha', 'Publicaciones']
        
        fig_time = px.area(
            timeline,
            x='Fecha',
            y='Publicaciones',
            color_discrete_sequence=['#764ba2']
        )
        fig_time.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Tabla de datos
    st.markdown("### 📋 Listado de Trabajos")
    
    # Preparar datos para mostrar
    display_df = df_filtered[['title', 'company', 'category', 'salary', 'pub_date']].copy()
    display_df.columns = ['Título', 'Empresa', 'Categoría', 'Salario', 'Fecha']
    display_df['Fecha'] = display_df['Fecha'].dt.strftime('%Y-%m-%d')
    
    # Búsqueda
    search = st.text_input("🔎 Buscar por título o empresa...")
    if search:
        mask = (
            display_df['Título'].str.contains(search, case=False, na=False) |
            display_df['Empresa'].str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6B7280; padding: 1rem;'>
            <p>📊 Dashboard generado con datos extraídos por Apache Airflow ETL</p>
            <p>Datos actualizados automáticamente cada ejecución del DAG</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

