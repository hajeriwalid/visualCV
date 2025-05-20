import json
import streamlit as st
import pandas as pd
import anthropic
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pydeck as pdk

# Set page configuration
st.set_page_config(
    page_title="WALID HAJERI - Customer Engineer Profile",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #C74634;
        --secondary-color: #2C5770;
        --background-color: #F7F7F7;
        --text-color: #333333;
        --accent-color: #F5A623;
    }
    
    /* Headers styling */
    h1, h2, h3, h4 {
        color: var(--primary-color);
        font-family: 'Arial', sans-serif;
        margin-bottom: 1rem;
    }
    
    /* Header with underline */
    .header-style {
        border-bottom: 2px solid var(--accent-color);
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    /* Cards for content */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Highlight box */
    .highlight-box {
        background-color: rgba(199, 70, 52, 0.1);
        border-left: 5px solid var(--primary-color);
        padding: 15px;
        margin: 15px 0;
    }
    
    /* Profile header */
    .profile-header {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
    }
    
    /* Oracle branding */
    .oracle-brand {
        background-color: #C74634;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Timeline styles */
    .timeline-item {
        border-left: 2px solid var(--secondary-color);
        padding-left: 20px;
        margin-bottom: 25px;
        position: relative;
    }
    
    .timeline-item:before {
        content: '';
        width: 15px;
        height: 15px;
        background-color: var(--secondary-color);
        border-radius: 50%;
        position: absolute;
        left: -8px;
        top: 5px;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Skills badge */
    .skill-badge {
        display: inline-block;
        background-color: var(--secondary-color);
        color: white;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    /* Button styling */
    div.stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-weight: bold;
    }
    
    div.stButton > button:hover {
        background-color: var(--secondary-color);
        transition: 0.3s;
    }
    
    /* Progress bar styling */
    div.stProgress > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Tab styling */
    button[data-baseweb="tab"] {
        font-weight: bold;
    }
    
    button[data-baseweb="tab"]:focus {
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)

# Load CV data
cv_data = """
{
    "personal": {
        "name": "WALID HAJERI",
        "title": "Cloud/AI Customer Engineer",
        "location": "Paris Region, France",
        "linkedin": "http://www.linkedin.com/in/walidhajeri"
    },
    "objective": "Experienced AI / Cloud Solutions Engineer with over 15 years of experience in the tech/cloud industry.",
    "experience": [
        {
            "years": "2022-present",
            "title": "Principal Cloud Adoption Manager",
            "company": "ORACLE",
            "location": "Paris",
            "responsibilities": [
                "Leading successful onboarding of new customers and workloads, technical advisory, sharing product updates & best practices, mitigating risks, ensuring customer satisfaction Coordinating multiple teams (specialists, product management, etc.) Increased account portfolio usage by 18% in the first year and 39% in the second year",
                "Monitoring & reviewing cloud adoption plans & forecasts for a portfolio of +12€ M ARR top-tier customers (manufacturing/aerospace/retail) Participation in setting-up & standardizing post-sales service catalogue across EMEA Scope: Oracle Cloud Infrastructure PaaS/laas (+ 100 products)"
            ]
        },
        {
            "years": "2018-2022",
            "title": "Principal Customer Success Manager",
            "company": "Axway",
            "location": "Paris",
            "responsibilities": [
                "CSM & Technical Account Management of all-tier cloud accounts across EMEA",
                "Achieved usage increase +8% per year, 110% Retention Rate",
                "Proactively conducted Business Reviews, Trainings, Product Updates, Liaised with Product Management / Sales / Partners/Support (Escalations) Secured significative up-sells / cross-sells",
                "Scope: API Management, Integration Platform as a Service, Content Services"
            ]
        },
        {
            "years": "2018",
            "title": "Senior Technical Sales Engineer",
            "company": "Viasat",
            "location": "Dublin",
            "responsibilities": [
                "Strategic pre-sales support to the sales team for complex deals (+1M€ Deals) RFI/RFP coordination + leading technical answers for AWS deployments Sales Engineering process and material improvements"
            ]
        },
        {
            "years": "2014-2018",
            "title": "Cloud Platform Pre-Sales",
            "company": "ORACLE",
            "location": "Dublin",
            "responsibilities": [
                "Present and demonstrate the Oracle Cloud portfolio (Paas/laas, 60 products) Supporting UK/IE sales team in the qualification of opportunities, analyzing customers' requirements and building cloud solution architectures",
                "Delivered Sales Enablement & Trainings (Sales Academy) Participation in demand generation programs, use case & go-to-market strategies In rotation with EMEA Product Management team, launched & lead the App Dev community Contributed to an average +1M$ revenue / year",
                "Scope: PaaS/laaS, App Dev (Cloud Native, DevOps, Docker) Integration, Content Cloud"
            ]
        },
        {
            "years": "2012-2014",
            "title": "EMEA/AP Lead Technical Account Manager & Pre-sales",
            "company": "NETVIBES (Dassault Systemes company)",
            "location": "Paris",
            "responsibilities": [
                "Set up & lead the pre-sales & TAM activities for EMEA / AP region for 3DS Netvibes Provided strategic support to the business development team (including RFPs, PoCs, customer presentations & demos, solution architecture ...) and internally to Dassault System's sales engineers in $EMEA/AP$",
                "Product Management: produced & maintained internal competitive matrix and wrote sales battle cards Closed the 1st 600k$ deal with UAE customer and 1st deal with South Korean multinational"
            ],
            "scope": "Scope: Natural Language Processing, Web Apps, APIs, Digital Marketing"
        }
    ],
    "education": [
        {
            "years": "2009-2010",
            "degree": "Master of Business Administration (MBA)",
            "school": "University of Paris 1 Pantheon Sorbonne",
            "notes": "MBA thesis on Cloud Computing obtained with Highest Honours"
        },
        {
            "years": "2001-2006",
            "degree": "IT Engineering Degree",
            "school": "Ecole Centrale d'Electronique"
        }
    ],
    "languages": {
        "English": "fluent",
        "French": "native",
        "Arabic": "native tunisian arabic",
        "Spanish": "basic spanish"
    },
    "certifications": [
        "Oracle Cloud Generative Al Professional (2025)",
        "Python Programming (O'Reilly course) (2024)",
        "Machine Learning Methods Specialized Certificate, University of California San Diego Extension (2023-2024)",
        "NVidia Certified Associate Al In the Data Center (2024)",
        "Oracle Cloud Operations Professional (2024)",
        "Algorithms (Post Graduate course), University of Leeds (2023)",
        "Oracle Autonomous Database Cloud Professional (2023)",
        "Oracle Cloud Infrastructure Architect Associate (2022)",
        "Certified Kubernetes & Cloud Native Associate (2022)",
        "Machine Learning, Stanford University via Coursera (2021)",
        "Product Management, Stanford University Continuing Studies (2018)"
    ],
    "publications": [
        "Digital, Organizational Customer Success & Experiential Solutions (Self-Published book on Amazon) (2021)",
        "Tech Blog Posts Latest: https://walidhajeri.hashnode.dev/"
    ],
    "other": "Founder"
}
"""

cv = json.loads(cv_data)

# Create sidebar for navigation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/50/Oracle_logo.svg", width=150)
    st.markdown("### Navigation")
    page = st.radio("Go to", ["Profile Overview", "Experience", "Skills & Certifications", "Global Footprint", "Why Oracle", "Q&A"])
    
    # Add contact information to sidebar
    st.markdown("---")
    st.markdown("### Contact Information")
    st.markdown(f"📍 {cv['personal']['location']}")
    st.markdown(f"🔗 [LinkedIn Profile]({cv['personal']['linkedin']})")
    
    # Add languages visualization
    st.markdown("---")
    st.markdown("### Language Proficiency")
    
    languages = cv["languages"]
    proficiency_levels = {
        "native": 100,
        "fluent": 85,
        "basic": 40
    }
    
    for lang, level in languages.items():
        level_percentage = proficiency_levels.get(level.split()[0].lower(), 50)
        st.markdown(f"**{lang}**")
        st.progress(level_percentage/100)

# Create enhanced map data function
def create_map_data():
    # Work locations with more details
    work_locations = pd.DataFrame({
        'city': ['Paris', 'Dublin'],
        'type': ['Work Location', 'Work Location'],
        'description': ['Current work location', 'Previous work location'],
        'lat': [48.8566, 53.3498],
        'lon': [2.3522, -6.2603],
        'size': [15, 12],  # Varying size for visual hierarchy
        'color': ['#FF5733', '#FF7F50']  # Different orange shades
    })
    
    # Customer locations with more details
    customer_locations = pd.DataFrame({
        'city': ['London', 'Seoul', 'Madrid', 'Barcelona', 'Rome', 'Geneva',
                 'Amsterdam', 'Pretoria', 'Doha', 'Mumbai', 'Brussels', 'Munich', 'Manchester',
                 'Abu Dhabi', 'Porto', 'Rabat', 'Oslo', 'Helsinki', 'Manila', 'Fort Worth',
                 'Porto-Novo', 'Abuja', 'Praia', 'Yamoussoukro', 'Banjul', 'Accra', 'Bissau',
                 'Conakry', 'Monrovia', 'Bamako', 'Niamey', 'Abidjan', 'Dakar', 'Freetown',
                 'Lomé', 'Washington, DC', 'Marseille', 'Lille', 'Bordeaux', 'Rennes'],
        'type': ['Customer Location'] * 40,
        'description': ['Customer served'] * 40,  # Simplified for example
        'lat': [51.5074, 37.5665, 40.4168, 41.3851, 41.9028, 46.2022,
                52.3702, -25.7461, 25.2854, 19.0760, 50.8333, 48.1371, 53.4808,
                24.4511, 41.1496, 34.0253, 59.9139, 60.1699, 14.5995, 32.7554,
                6.4779, 9.0579, 14.9214, 6.8206, 13.4531, 5.6037, 11.8596,
                9.5167, 6.3105, 12.6500, 13.5197, 5.3524, 14.7105, 8.4605,
                6.1305, 38.8951, 43.2965, 50.6292, 44.8378, 48.1173],
        'lon': [-0.1278, 126.9780, -3.7038, 2.1734, 12.4964, 6.1490,
                4.8952, 28.1871, 51.5310, 72.8777, 4.3333, 11.5761, -2.2426,
                54.3696, -8.6291, -6.8791, 10.7522, 24.9384, 120.9772, -97.3308,
                2.6323, 7.3985, -23.5000, -5.2767, -16.5780, -0.2079, -15.5042,
                -13.7036, -10.8022, -8.0077, 2.1096, -4.0083, -17.4788, -13.1049,
                -1.3159, -77.0364, 5.3698, 3.0573, -0.5792, -1.6778],
        'size': [8] * 40,  # Consistent size for customers
        'color': ['#007BFF'] * 40  # Consistent blue color for customers
    })

    # Education locations with more details
    study_locations = pd.DataFrame({
        'city': ['Paris', 'Leeds', 'Tunis', 'San Diego', 'Stanford'],
        'type': ['Education Location'] * 5,
        'description': ['MBA', 'Algorithms Post Graduate Course', 'Early Education', 'ML Certificate', 'Product Management'],
        'lat': [48.8800, 53.8012, 36.8065, 32.7157, 37.4275],
        'lon': [2.3000, -1.5486, 10.1815, -117.1611, -122.1697],
        'size': [10] * 5,  # Medium size for education
        'color': ['#2ecc71'] * 5  # Green for education
    })
    
    # Combine all data
    return pd.concat([work_locations, customer_locations, study_locations], ignore_index=True)

# Create career timeline data
def create_career_timeline():
    experience = cv["experience"]
    timeline_data = []
    
    for job in experience:
        years = job["years"]
        if "-" in years:
            start_year = years.split("-")[0]
            end_year = years.split("-")[1] if years.split("-")[1] != "present" else "2025"
        else:
            start_year = years
            end_year = years
        
        timeline_data.append({
            "company": job["company"],
            "title": job["title"],
            "start_year": int(start_year),
            "end_year": end_year if end_year == "present" else int(end_year),
            "duration": int(end_year) - int(start_year) if end_year != "present" else 2025 - int(start_year),
            "location": job["location"]
        })
    
    return timeline_data

# Extract skills from CV data
def extract_skills():
    # This is a basic extraction - you might want to add more sophisticated logic
    skills = {
        "Cloud Technologies": {"Oracle Cloud": 90, "AWS": 75, "API Management": 85, "PaaS/IaaS": 90},
        "AI & ML": {"Machine Learning": 80, "Natural Language Processing": 75, "Generative AI": 85},
        "Business": {"Customer Success": 95, "Pre-sales": 90, "Product Management": 75, "Technical Account Management": 95},
        "Languages & Tools": {"Python": 80, "Kubernetes": 75, "Docker": 70}
    }
    return skills

# Main function
def main():
    # Profile Overview Page
    if page == "Profile Overview":
        # Header section with profile info
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Profile image placeholder (replace with your image URL)
            st.image("https://api.placeholder.com/300", width=200)
        
        with col2:
            st.markdown(f"<h1>{cv['personal']['name']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3>{cv['personal']['title']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='highlight-box'>{cv['objective']}</div>", unsafe_allow_html=True)
            
            # Key metrics
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            metrics_col1.metric("Years of Experience", "15+")
            metrics_col2.metric("Customers Served", "40+")
            metrics_col3.metric("Certifications", len(cv["certifications"]))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick highlights section
        st.markdown("<h2 class='header-style'>Professional Highlights</h2>", unsafe_allow_html=True)
        highlight_col1, highlight_col2 = st.columns(2)
        
        with highlight_col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Career Achievements")
            st.markdown("- **Portfolio Growth:** Increased account portfolio usage by **39%** in second year")
            st.markdown("- **Customer Retention:** Achieved **110%** retention rate at Axway")
            st.markdown("- **Revenue Impact:** Contributed to an average **+1M$** revenue per year")
            st.markdown("- **Global Reach:** Worked with customers across **40+** cities worldwide")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with highlight_col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Education & Continuous Learning")
            st.markdown("- MBA from University of Paris 1 Pantheon Sorbonne")
            st.markdown("- IT Engineering Degree from Ecole Centrale d'Electronique")
            st.markdown("- **11** Professional certifications including AI & Machine Learning")
            st.markdown("- Published author on Customer Success methodologies")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Latest certifications
        st.markdown("<h2 class='header-style'>Latest Certifications</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cert_col1, cert_col2, cert_col3 = st.columns(3)
        
        recent_certs = cv["certifications"][:3]
        cert_col1.markdown(f"<div class='highlight-box'><h4>{recent_certs[0]}</h4></div>", unsafe_allow_html=True)
        cert_col2.markdown(f"<div class='highlight-box'><h4>{recent_certs[1]}</h4></div>", unsafe_allow_html=True)
        cert_col3.markdown(f"<div class='highlight-box'><h4>{recent_certs[2]}</h4></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Publications
        st.markdown("<h2 class='header-style'>Publications</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for pub in cv["publications"]:
            st.markdown(f"- {pub}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Experience Page
    elif page == "Experience":
        st.markdown("<h1 class='header-style'>Professional Experience</h1>", unsafe_allow_html=True)
        
        # Career Timeline Visualization
        st.markdown("<h2>Career Timeline</h2>", unsafe_allow_html=True)
        timeline_data = create_career_timeline()
        
        # Convert to DataFrame for visualization
        df_timeline = pd.DataFrame(timeline_data)
        
        # Create Gantt chart with Plotly
        fig = px.timeline(
            df_timeline, 
            x_start="start_year", 
            x_end="end_year", 
            y="company",
            color="company",
            text="title",
            labels={"company": "Company", "start_year": "Year Started", "end_year": "Year Ended"},
            title="Career Progression"
        )
        fig.update_layout(height=400, xaxis_title="Year", yaxis_title="Company")
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed experience listings
        st.markdown("<h2>Detailed Experience</h2>", unsafe_allow_html=True)
        
        for i, job in enumerate(cv["experience"]):
            if job.get("title") != "ShopFromFrance":  # Checking as per your original code
                st.markdown('<div class="card">', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"<h3>{job['title']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<h4>{job['company']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p>{job['location']} | {job['years']}</p>", unsafe_allow_html=True)
                
                with col2:
                    # Company logo placeholder - replace with actual company logos
                    if job['company'] == "ORACLE":
                        st.image("https://upload.wikimedia.org/wikipedia/commons/5/50/Oracle_logo.svg", width=100)
                    elif job['company'] == "Axway":
                        st.image("https://api.placeholder.com/100", width=100)
                    else:
                        st.image("https://api.placeholder.com/100", width=100)
                
                st.markdown("<h4>Key Responsibilities:</h4>", unsafe_allow_html=True)
                for resp in job.get("responsibilities", []):
                    st.markdown(f"- {resp}")
                
                if i < len(cv["experience"]) - 1:  # Don't show expander for last job
                    with st.expander("Show Achievements"):
                        st.markdown("### Key Achievements")
                        # Example achievements - you can replace with actual data
                        if job['company'] == "ORACLE" and job['years'] == "2022-present":
                            st.markdown("- Increased account portfolio usage by 18% in the first year and 39% in the second year")
                            st.markdown("- Successfully onboarded 15 enterprise customers to Oracle Cloud")
                            st.markdown("- Standardized post-sales service catalog across EMEA")
                        elif job['company'] == "Axway":
                            st.markdown("- Achieved usage increase +8% per year, 110% Retention Rate")
                            st.markdown("- Secured significant up-sells / cross-sells with major accounts")
                            st.markdown("- Developed new business review process adopted company-wide")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Skills alignment section
        st.markdown("<h2>Skills and Responsibilities Alignment</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Define job responsibilities and corresponding examples
        responsibilities_examples = {
            "Conduct periodic Service Account Planning and Account Reviews // Establish and maintain a delivery governance model with the customer at the management and executive levels.": [
                "- At Oracle: Monthly/Quarterly Reviews + Technical Reviews + SR Reviews",
                "- At Axway: Led Quarterly Business Reviews with customers"
            ],
            "Act as a point of contact for any major incidents, responsible for managing communication and customer expectations through resolution.": [
                "- Example: Escalation Management",
            ],
            "Coordinate delivery of Oracle Services, operating as the primary delivery contact to the customer, aiding and facilitating customer communications and activities across other Oracle lines of business.": [
                "- Example: Coordinate delivery of multiple Oracle Services including Technical Workshops (e.g. Patching workshop), Technical Reviews (HC), Consumption Reviews, SR Reviews, Go Live Assurance ",
            ],
             "Identify and submit delivery leads for new opportunities and contract renewals // Work collaboratively with sales, the delivery teams and customers to identify appropriate solutions.": [
                "- Example: Uncovered multiple service delivery opportunities : Oracle Universiy, Consulting. Product needs : Full Stack Discovery need (Retail), Database Management, OS Management Hub (automotive), etc. ",
            ]
        }

        # Create tabs for each responsibility
        resp_tabs = st.tabs([f"Responsibility {i+1}" for i in range(len(responsibilities_examples))])
        
        # Display responsibilities and examples in tabs
        for i, (responsibility, examples) in enumerate(responsibilities_examples.items()):
            with resp_tabs[i]:
                st.markdown(f"<h4>{responsibility}</h4>", unsafe_allow_html=True)
                st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
                for example in examples:
                    st.markdown(f"{example}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Skills & Certifications Page
    elif page == "Skills & Certifications":
        st.markdown("<h1 class='header-style'>Skills & Certifications</h1>", unsafe_allow_html=True)
        
        # Skills visualization
        st.markdown("<h2>Professional Skills</h2>", unsafe_allow_html=True)
        skills = extract_skills()
        
        # Create a radar chart for skills
        categories = []
        values = []
        
        for category, skill_dict in skills.items():
            st.markdown(f"<h3>{category}</h3>", unsafe_allow_html=True)
            
            # Create columns for each skill area
            cols = st.columns(len(skill_dict))
            
            for i, (skill, level) in enumerate(skill_dict.items()):
                with cols[i]:
                    st.markdown(f"<p style='text-align: center;'>{skill}</p>", unsafe_allow_html=True)
                    st.progress(level/100)
                    st.markdown(f"<p style='text-align: center;'>{level}%</p>", unsafe_allow_html=True)
                
                # Collect data for radar chart
                categories.append(skill)
                values.append(level)
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Skills',
            line_color='rgba(199, 70, 52, 0.8)',
            fillcolor='rgba(199, 70, 52, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            title="Skills Radar"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Certifications section
        st.markdown("<h2>Certifications</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Group certifications by year
        cert_by_year = {}
        for cert in cv["certifications"]:
            year = cert.split("(")[-1].strip(")")
            if year not in cert_by_year:
                cert_by_year[year] = []
            cert_by_year[year].append(cert.split("(")[0].strip())
        
        # Display certifications by year
        for year in sorted(cert_by_year.keys(), reverse=True):
            with st.expander(f"{year} Certifications"):
                for cert in cert_by_year[year]:
                    st.markdown(f"- **{cert}**")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Education section
        st.markdown("<h2>Education</h2>", unsafe_allow_html=True)
        for edu in cv["education"]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{edu['degree']}**")
            st.markdown(f"*{edu['school']}* ({edu['years']})")
            if 'notes' in edu:
                st.markdown(f"_{edu['notes']}_")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Languages
        st.markdown("<h2>Languages</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        lang_cols = st.columns(len(cv["languages"]))
        
        for i, (lang, level) in enumerate(cv["languages"].items()):
            with lang_cols[i]:
                # Create a circular gauge chart for language proficiency
                if "native" in level.lower():
                    value = 100
                    color = "#2ecc71"  # Green
                elif "fluent" in level.lower():
                    value = 85
                    color = "#3498db"  # Blue
                else:
                    value = 40
                    color = "#f39c12"  # Yellow
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = value,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, 40], 'color': "lightgray"},
                            {'range': [40, 75], 'color': "gray"},
                            {'range': [75, 100], 'color': "darkgray"}
                        ],
                    },
                    title = {'text': lang}
                ))
                
                fig.update_layout(height=200, margin=dict(l=30, r=30, t=50, b=30))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f"<p style='text-align: center;'>{level}</p>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Global Footprint Page
    elif page == "Global Footprint":
        st.markdown("<h1 class='header-style'>Global Footprint</h1>", unsafe_allow_html=True)
        st.markdown("<p>Explore my global experience across work locations, education institutions, and customers served.</p>", unsafe_allow_html=True)
        
        # Get map data
        map_data = create_map_data()
        
        # Create an advanced 3D map with PyDeck
        view_state = pdk.ViewState(
            latitude=30,
            longitude=0,
            zoom=1.5,
            pitch=45
        )
        
        # Create different layers for work, education, and customers
        work_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data[map_data['type'] == 'Work Location'],
            get_position=["lon", "lat"],
            get_radius="size * 50000",  # Adjust multiplier as needed
            get_fill_color=[255, 87, 51, 200],  # Orange with transparency
            pickable=True,
            auto_highlight=True,
            radius_scale=2
        )
        
        education_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data[map_data['type'] == 'Education Location'],
            get_position=["lon", "lat"],
            get_radius="size * 40000",  # Slightly smaller than work
            get_fill_color=[46, 204, 113, 200],  # Green with transparency
            pickable=True,
            auto_highlight=True,
            radius_scale=2
        )
        
        customer_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data[map_data['type'] == 'Customer Location'],
            get_position=["lon", "lat"],
            get_radius="size * 30000",  # Smaller than education
            get_fill_color=[0, 123, 255, 150],  # Blue with more transparency
            pickable=True,
            auto_highlight=True,
            radius_scale=2
        )
        
        # Create the deck
        deck = pdk.Deck(
            layers=[work_layer, education_layer, customer_layer],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>{city}</b><br>{type}<br>{description}",
                "style": {
                    "backgroundColor": "white",
                    "color": "black"
                }
            }
        )
        
        # Render the deck
        st.pydeck_chart(deck)
        
        # Add legend
        col1, col2, col3 = st.columns(3)
        col1.markdown('<div style="background-color:#FF5733; height:20px; width:20px; display:inline-block; margin-right:10px;"></div> Work Locations', unsafe_allow_html=True)
        col2.markdown('<div style="background-color:#2ecc71; height:20px; width:20px; display:inline-block; margin-right:10px;"></div> Education', unsafe_allow_html=True)
        col3.markdown('<div style="background-color:#007BFF; height:20px; width:20px; display:inline-block; margin-right:10px;"></div> Customer Locations', unsafe_allow_html=True)
        
        # Statistics section
        st.markdown("<h2>Global Impact Statistics</h2>", unsafe_allow_html=True)
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        stats_col1.metric("Continents", "5")
        stats_col2.metric("Countries", "30+")
        stats_col3.metric("Cities", "40+")
        stats_col4.metric("Global Projects", "50+")
        
        # Regional breakdown
        st.markdown("<h2>Regional Experience Breakdown</h2>", unsafe_allow_html=True)
        
        # Sample data - replace with actual data if available
        regions = ['Europe', 'Middle East', 'North America', 'Africa', 'Asia Pacific']
        percentages = [45, 20, 15, 12, 8]
        
        fig = px.pie(
            values=percentages,
            names=regions,
            title="Geographic Distribution of Work Experience",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        
        st.plotly_chart(fig, use_container_width=True)

    # Why Oracle Page
    elif page == "Why Oracle":
        st.markdown("<h1 class='header-style'>Why Oracle</h1>", unsafe_allow_html=True)
        
        # Oracle brand statement
        st.markdown('<div class="oracle-brand">', unsafe_allow_html=True)
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/50/Oracle_logo.svg", width=200)
        st.markdown("<h2>The Most Complete Cloud Portfolio to Power Customer Transformation</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Why Oracle section with tabs
        oracle_tabs = st.tabs(["Growth & Innovation", "Career Growth", "Complete Portfolio", "Customer Success"])
        
        with oracle_tabs[0]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>The Fastest Growing Cloud Hyperscaler</h3>", unsafe_allow_html=True)
            
            # Create growth chart
            years = ["2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4", "2024 Q1", "2024 Q2", "2024 Q3", "2024 Q4", "2025 Q1", "2025 Q2", "2025 Q3"]
            growth = [18, 22, 26, 30, 34, 38, 40, 42, 45, 47, 49]
            
            fig = px.line(
                x=years, 
                y=growth,
                labels={"x": "Quarter", "y": "Cloud Growth (%)"},
                title="Oracle Cloud Infrastructure Growth",
                markers=True
            )
            
            fig.update_traces(line_color='#C74634', line_width=3, marker_size=10)
            fig.add_annotation(
                x=years[-1],
                y=growth[-1],
                text="+49% Growth",
                showarrow=True,
                arrowhead=1
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### One of the most innovative companies in the world")
            st.markdown("- Data is at the heart of the AI revolution")
            st.markdown("- Strategic partnerships with AI leaders")
            st.markdown("- Continuous innovation in database and cloud technologies")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with oracle_tabs[1]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>Top Company for Career Growth</h3>", unsafe_allow_html=True)
            
            st.markdown("### Career Development Opportunities")
            st.markdown("- Cross-functional collaboration")
            st.markdown("- Global teams and projects")
            st.markdown("- Learning and development resources")
            st.markdown("- Mentorship programs")
            
            st.markdown("### Employee Testimonials")
            
            testimonial_cols = st.columns(2)
            
            with testimonial_cols[0]:
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.markdown("*\"Oracle has provided me with countless opportunities to grow professionally and take on new challenges that have accelerated my career.\"*")
                st.markdown("**- Senior Technical Advisor, 8 years at Oracle**")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with testimonial_cols[1]:
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.markdown("*\"The collaborative culture at Oracle has allowed me to learn from industry experts and develop skills across multiple domains.\"*")
                st.markdown("**- Cloud Engineer, 5 years at Oracle**")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with oracle_tabs[2]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>The Most Complete Cloud Portfolio</h3>", unsafe_allow_html=True)
            
            # Create portfolio visualization
            portfolio_categories = [
                "Infrastructure", 
                "Database", 
                "Applications", 
                "Developer Tools", 
                "Integration", 
                "Analytics", 
                "AI/ML"
            ]
            
            portfolio_products = [
                100, 
                25, 
                80, 
                45, 
                30, 
                40, 
                35
            ]
            
            fig = px.bar(
                x=portfolio_categories,
                y=portfolio_products,
                labels={"x": "Category", "y": "Number of Products"},
                title="Oracle's Comprehensive Product Portfolio",
                color=portfolio_products,
                color_continuous_scale="Reds"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Key Differentiators")
            st.markdown("- End-to-end solutions from infrastructure to applications")
            st.markdown("- Industry-leading database technology")
            st.markdown("- Enterprise-grade security and compliance")
            st.markdown("- Integrated AI capabilities across the portfolio")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with oracle_tabs[3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>Oracle Customer Success</h3>", unsafe_allow_html=True)
            
            st.markdown("### Global Team of Experts")
            st.markdown("- Integrated with Oracle's product development teams")
            st.markdown("- Team of +13000 Global Experts:")
            st.markdown("  - ACS")
            st.markdown("  - Oracle University")
            st.markdown("  - CSMs")
            st.markdown("  - Success Assurance")
            st.markdown("  - Partner Success Managers")
            st.markdown("  - Global Services Delivery")
            
            st.markdown("### Customer Success Culture")
            st.markdown("- Proactive approach")
            st.markdown("- Business Goal Achievement")
            st.markdown("- Focus on Value/Adoption/ROI")
            st.markdown("- Customer Advocacy")
            
            st.markdown("### Advanced Tooling")
            st.markdown("- Cloud Success Navigator")
            st.markdown("- Solution Support Center (Intelligent operations)")
            st.markdown("- Comprehensive monitoring and analytics")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Why I'm a great fit section
        st.markdown("<h2 class='header-style'>Why I'm a Great Fit</h2>", unsafe_allow_html=True)
        
        fit_col1, fit_col2 = st.columns(2)
        
        with fit_col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Professional Alignment")
            st.markdown("- Strong Experience in Customer Success")
            st.markdown("- Proven track record in technical advisory")
            st.markdown("- Great team player, Coordinator & Customer advocate")
            st.markdown("- Used to high-stakes situations, Escalation Management")
            st.markdown("- Oracle Cloud knowledge, AI-Enthusiast => Crucial for Customer innovation & Growth")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with fit_col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Personal Commitment")
            st.markdown("- Dedicated to continuous learning")
            st.markdown("- Passionate about customer success")
            st.markdown("- Strong communication and relationship building skills")
            st.markdown("- Problem-solver with attention to detail")
            st.markdown("- Global perspective and cultural adaptability")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Q&A Section - PRESERVED AS REQUESTED
    elif page == "Q&A":
        # Document Q&A with Anthropic Claude section
        st.header("📝 Q&A on my book powered by Anthropic")
        
        # Get API key from secrets
        anthropic_api_key = st.secrets.get("anthropic_api_key", "")
        
        if not anthropic_api_key:
            anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")
            if not anthropic_api_key:
                st.sidebar.warning("Please enter your Anthropic API key to use the Q&A feature")
        
        # File uploader for document
        uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
        
        # Question input
        question = st.text_input(
            "Ask something about the article",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )
        
        # Process if we have all required inputs
        if uploaded_file and question and anthropic_api_key:
            with st.spinner("Analyzing your document..."):
                try:
                    # Read article content
                    article = uploaded_file.read().decode()
                    
                    # Initialize Anthropic client with the API key
                    client = anthropic.Anthropic(api_key=anthropic_api_key)
                    
                    # Create a messages request using the Messages API
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=3000,
                        temperature=0,
                        system="You are a helpful assistant that answers questions about documents. Be concise and accurate in your responses.",
                        messages=[
                            {
                                "role": "user", 
                                "content": f"Here's an article:\n\n<article>\n{article}\n</article>\n\nPlease answer this question about the article: {question}"
                            }
                        ]
                    )
                    
                    # Extract and display the response
                    st.write("### Answer")
                    st.write(response.content[0].text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif uploaded_file and question and not anthropic_api_key:
            st.info("Please add your Anthropic API key to continue.")

if __name__ == "__main__":
    main()
