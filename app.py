
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ChemSafe Storage Matrix",
    page_icon="🧪",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.title{
    font-size:40px;
    font-weight:bold;
    color:#1f2937;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    text-align:center;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE CHEMICAL
# =====================================================

chemical_db = {

    "Nitric Acid": {
        "group": "Oxidizing Acid",
        "cas": "7697-37-2",
        "nfpa": "3-0-2",
        "incompatible": [
            "Ethanol",
            "Methanol",
            "Acetone",
            "Hydrogen Peroxide"
        ]
    },

    "Sulfuric Acid": {
        "group": "Strong Acid",
        "cas": "7664-93-9",
        "nfpa": "3-0-2",
        "incompatible": [
            "Sodium Hydroxide",
            "Potassium Hydroxide"
        ]
    },

    "Ethanol": {
        "group": "Flammable Solvent",
        "cas": "64-17-5",
        "nfpa": "3-0-0",
        "incompatible": [
            "Nitric Acid"
        ]
    },

    "Methanol": {
        "group": "Flammable Solvent",
        "cas": "67-56-1",
        "nfpa": "3-1-0",
        "incompatible": [
            "Nitric Acid"
        ]
    },

    "Hydrogen Peroxide": {
        "group": "Oxidizer",
        "cas": "7722-84-1",
        "nfpa": "2-0-1",
        "incompatible": [
            "Nitric Acid",
            "Methanol",
            "Ethanol"
        ]
    },

    "Sodium Hydroxide": {
        "group": "Strong Base",
        "cas": "1310-73-2",
        "nfpa": "3-0-1",
        "incompatible": [
            "Sulfuric Acid"
        ]
    }

}

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2784/2784487.png",
    width=120
)

st.sidebar.title("🧪 ChemSafe")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Compatibility Checker",
        "Chemical Database"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.markdown(
        "<div class='title'>🧪 ChemSafe Storage Matrix</div>",
        unsafe_allow_html=True
    )

    st.write("")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric(
            "Chemical Database",
            len(chemical_db)
        )

    with col2:
        st.metric(
            "Compatibility Rules",
            12
        )

    with col3:
        st.metric(
            "System Status",
            "Online"
        )

    st.divider()

    chart_data = pd.DataFrame({
        "Group":[
            "Acid",
            "Oxidizer",
            "Solvent",
            "Base"
        ],
        "Count":[
            2,
            1,
            2,
            1
        ]
    })

    fig = px.pie(
        chart_data,
        values="Count",
        names="Group",
        title="Chemical Categories"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info("""
    ChemSafe membantu melakukan audit kompatibilitas
    penyimpanan bahan kimia berdasarkan prinsip
    Chemical Segregation Matrix.
    """)

# =====================================================
# COMPATIBILITY CHECKER
# =====================================================

elif menu == "Compatibility Checker":

    st.title("🔍 Chemical Compatibility Checker")

    chemicals = sorted(
        list(chemical_db.keys())
    )

    col1,col2 = st.columns(2)

    with col1:
        chem_a = st.selectbox(
            "Chemical A",
            chemicals
        )

    with col2:
        chem_b = st.selectbox(
            "Chemical B",
            chemicals
        )

    if st.button(
        "🚀 Analyze Compatibility",
        use_container_width=True
    ):

        if chem_a == chem_b:

            st.success("""
            ✅ SAME CHEMICAL

            Tidak terdapat konflik kompatibilitas.
            Tetap ikuti SDS dan SOP penyimpanan.
            """)

        else:

            incompatible = (
                chem_b
                in
                chemical_db[chem_a]["incompatible"]
            )

            if incompatible:

                st.error("""
                ❌ NOT COMPATIBLE
                """)

                st.markdown("""
                ### ⚠️ Potential Hazards

                - Violent Chemical Reaction
                - Fire Risk
                - Explosion Risk
                - Toxic Gas Release
                """)

                st.markdown("""
                ### 📌 Recommendation

                - Store separately
                - Use dedicated cabinet
                - Follow SDS guidance
                - Segregate by hazard class
                """)

            else:

                st.success("""
                ✅ COMPATIBLE
                """)

                st.markdown("""
                ### Safe Storage Recommendation

                - Can be stored in same area
                - Follow secondary containment
                - Maintain ventilation
                - Follow SDS requirements
                """)

        st.divider()

        result = pd.DataFrame({
            "Parameter":[
                "Chemical A",
                "Chemical B",
                "Analysis Date"
            ],
            "Value":[
                chem_a,
                chem_b,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
            ]
        })

        st.dataframe(
            result,
            use_container_width=True
        )

# =====================================================
# CHEMICAL DATABASE
# =====================================================

elif menu == "Chemical Database":

    st.title("📚 Chemical Database")

    search = st.selectbox(
        "Select Chemical",
        sorted(
            list(
                chemical_db.keys()
            )
        )
    )

    chem = chemical_db[search]

    col1,col2 = st.columns(2)

    with col1:

        st.info(f"""
        Chemical Name

        {search}
        """)

        st.write("### CAS Number")
        st.write(chem["cas"])

        st.write("### Storage Group")
        st.write(chem["group"])

    with col2:

        st.write("### NFPA Rating")
        st.code(chem["nfpa"])

        st.write("### Incompatible With")

        for item in chem["incompatible"]:
            st.error(item)

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class='footer'>
ChemSafe Storage Matrix v1.0
<br>
Chemical Compatibility Audit System
</div>
""", unsafe_allow_html=True)
