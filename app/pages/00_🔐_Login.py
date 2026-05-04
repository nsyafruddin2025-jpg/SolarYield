import streamlit as st
import pathlib

st.set_page_config(
    page_title="Client Login — SolarYield",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
.block-container {padding: 0 !important; max-width: 100% !important;}
</style>
""", unsafe_allow_html=True)

html_file = pathlib.Path("app/assets/website/login.html")
html_content = html_file.read_text(encoding="utf-8")
st.components.v1.html(html_content, height=800, scrolling=False)

st.markdown("""
<script>
window.addEventListener('message', function(e) {
    if (e.data.type === 'login_success') {
        window.parent.location.href = '/dashboard';
    }
});
</script>
""", unsafe_allow_html=True)
