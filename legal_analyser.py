import streamlit as st
import PyPDF2
import re
from io import BytesIO
import folium
from streamlit_folium import folium_static

# Expanded Legal Terms Database
LEGAL_TERMS = {
    'termination': {
        'keywords': ['terminate', 'cancel', 'breach', 'end', 'discontinue'],
        'explanation': 'Termination Clause Analysis',
        'detailed_explanation': '''
        This section outlines how and under what conditions the contract can be ended. Key aspects to examine:
        - Notice periods for termination
        - Conditions that allow immediate termination
        - Penalties or consequences of termination
        - Rights of both parties upon contract conclusion
        ''',
        'constitutional_reference': 'Relevant to Contract Law under Ghana\'s Civil Transactions Act',
        'red_flags': {
            'areas_to_scrutinize': [
                'Unilateral termination rights',
                'Vague termination conditions',
                'Punitive termination penalties'
            ]
        }
    },
    'payment': {
        'keywords': ['fee', 'payment', 'charge', 'cost', 'financial', 'invoice'],
        'explanation': 'Payment Terms Analysis',
        'detailed_explanation': '''
        Comprehensive review of financial obligations:
        - Exact payment amounts
        - Payment schedules and deadlines
        - Late payment consequences
        - Additional fees or potential cost escalations
        - Payment methods and currencies
        ''',
        'constitutional_reference': 'Aligned with Ghana\'s Commercial Transactions Act',
        'red_flags': {
            'areas_to_scrutinize': [
                'Hidden charges',
                'Automatic price increases',
                'Ambiguous payment terms'
            ]
        }
    },
    'data': {
        'keywords': ['data', 'privacy', 'collect', 'personal information', 'share'],
        'explanation': 'Data Protection and Privacy Analysis',
        'detailed_explanation': '''
        Comprehensive data usage and protection review:
        - Types of data collected
        - Purpose of data collection
        - Data sharing practices
        - User consent mechanisms
        - Data retention and deletion policies
        ''',
        'constitutional_reference': 'Directly aligned with Ghana\'s Data Protection Act, 2012',
        'red_flags': {
            'areas_to_scrutinize': [
                'Broad data collection clauses',
                'Third-party data sharing',
                'Lack of clear data protection mechanisms'
            ]
        }
    }
}

# Law Firms Database (Mock Data - To be expanded)
LAW_FIRMS = [
    {
        'name': 'Bentsi-Enchill, Letsa & Antwi',
        'location': {'lat': 5.6037, 'lon': -0.1870},
        'specialty': 'Corporate Law',
        'address': 'Achinko House, Labone, Accra'
    },
    {
        'name': 'Reindorf Chambers',
        'location': {'lat': 5.5957, 'lon': -0.1868},
        'specialty': 'Commercial Law',
        'address': 'Airport Residential Area, Accra'
    }
]

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
    text = "\n".join([page.extract_text() for page in pdf_reader.pages])
    return text

def split_clauses(text):
    return [p.strip() for p in re.split(r'\n\s*\n|\.\s+', text) if len(p) > 50]

def create_map(firms):
    m = folium.Map(location=[5.6037, -0.1870], zoom_start=12)
    for firm in firms:
        folium.Marker(
            location=[firm['location']['lat'], firm['location']['lon']],
            popup=f"{firm['name']}\n{firm['specialty']}\n{firm['address']}",
            tooltip=firm['name']
        ).add_to(m)
    return m

def main():
    st.set_page_config(page_title="LegalEase Ghana", page_icon="⚖️")
    
    # Introductory Section
    st.title("⚖️ LegalEase Ghana")
    st.write("""
    ### Your AI Legal Document Companion
    
    Demystifying legal documents, one clause at a time. 
    We help you understand complex legal language, 
    identify potential risks, and empower your decision-making.
    """)
    
    # Tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Document Analysis", "Legal Terms", "Nearby Law Firms"])
    
    with tab1:
        st.header("Upload Your Document")
        uploaded_file = st.file_uploader("PDF/TXT File", type=['pdf', 'txt'])
        text_input = st.text_area("Or Paste Text Here", height=300)
        
        if st.button("Analyze Document"):
            text = ""
            if uploaded_file:
                text = read_pdf(uploaded_file) if uploaded_file.name.endswith('.pdf') else uploaded_file.read().decode('utf-8')
            elif text_input:
                text = text_input
            
            if text:
                clauses = split_clauses(text)[:20]
                
                st.subheader("Key Insights")
                
                for term, data in LEGAL_TERMS.items():
                    matches = []
                    for clause in clauses:
                        if any(re.search(rf'\b{kw}\b', clause, re.I) for kw in data['keywords']):
                            matches.append(clause[:150] + "...")
                    
                    if matches:
                        with st.expander(f"{term.capitalize()} Clauses ({len(matches)})"):
                            st.write(f"**Explanation:** {data['detailed_explanation']}")
                            st.write(f"**Constitutional Reference:** {data['constitutional_reference']}")
                            
                            st.write("**Sample Clauses:**")
                            for match in matches[:3]:
                                st.write(f"- {match}")
                            
                            st.warning("Areas to Scrutinize:")
                            for area in data['red_flags']['areas_to_scrutinize']:
                                st.markdown(f"- 🚩 {area}")
    
    with tab2:
        st.header("Legal Terms Glossary")
        selected_term = st.selectbox("Choose a Term", list(LEGAL_TERMS.keys()))
        
        term_info = LEGAL_TERMS[selected_term]
        st.write(f"### {selected_term.capitalize()} Terms")
        st.write(term_info['detailed_explanation'])
        st.write(f"**Constitutional Reference:** {term_info['constitutional_reference']}")
    
    with tab3:
        st.header("Nearby Law Firms")
        location = st.text_input("Enter your area in Accra")
        
        if st.button("Show Nearby Firms"):
            m = create_map(LAW_FIRMS)
            folium_static(m)
            
            st.subheader("Law Firms")
            for firm in LAW_FIRMS:
                st.write(f"**{firm['name']}**")
                st.write(f"Specialty: {firm['specialty']}")
                st.write(f"Address: {firm['address']}")

if __name__ == "__main__":
    main()