import streamlit as st
st.set_page_config(page_title='Global Surgery and Anesthesia Workforce Mapping Project', page_icon=':earth_americas:', layout='centered', initial_sidebar_state='collapsed')
st.title('The Global Surgery and Anesthesia Workforce Mapping Project')
st.subheader('👋 Welcome')
st.markdown('''
            In the world of global surgery and anesthesia, human resources are key. Several different groups have engaged in mapping projects to help understand the number and distribution of surgeons, anesthesiologists, and other healthcare workers. 
            
            This project aims to bring together these different mapping projects in one place. 
            
            **Have a look at our maps:** ''')

st.page_link('app.py',label='🏠 Home')
st.page_link('pages/1_gaws.py',label='🌍 Global Anesthesia Workforce')
st.page_link('pages/2_CANESCA.py',label='😷 Anesthesiologists in East, Central and Southern Africa')
st.page_link('pages/3_OHNS.py',label='👂 Global ENT/OHNS Workforce')

st.markdown('''**About the project:** This project is a collaboration between the [Center for Health Equity in Surgery and Anesthesia (CHESA)](https://globalsurgery.org/), the [Royal College of Anaesthetists and College of Anaesthesiologists of East, Central and Southern Africa (CANECSA)](https://www.rcoa.ac.uk/about-college/global-partnerships/our-global-projects/college-anaesthesiologists-east-central), and the [The Global OHNS Initiative
](https://www.globalohns.org/global-ent-ohns-workforce).''')