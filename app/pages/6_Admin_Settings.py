#!/usr/bin/env python3
"""⚙️ Admin & Settings — SolarYield Dashboard"""

import streamlit as st

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------

PAGE_TITLE = "Admin & Settings — SolarYield"
PAGE_ICON = "⚙️"

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------

st.markdown("""
<style>
    .amber-divider {
        border: none;
        border-top: 3px solid #F4A836;
        margin: 2rem 0;
    }
    .section-header {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    .navy-banner {
        background: linear-gradient(135deg, #1E3A5F 0%, #0d2137 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .navy-banner .title {
        color: #F4A836;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .navy-banner .subtitle {
        color: #FFFFFF;
        font-size: 1.1rem;
    }
    .profile-card {
        background: #FFFFFF;
        border: 3px solid #F4A836;
        border-radius: 12px;
        padding: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #1E3A5F;
        color: #F4A836;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    .profile-info h3 {
        margin: 0 0 0.25rem 0;
        color: #1E3A5F;
    }
    .profile-info p {
        margin: 0.2rem 0;
        color: #666;
    }
    .role-badge {
        display: inline-block;
        background: #22C55E;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .api-key-box {
        background: #FFF9E6;
        border: 1px solid #F4A836;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        font-size: 1rem;
        color: #1E3A5F;
        margin: 1rem 0;
    }
    .billing-card {
        background: #FFF9E6;
        border: 2px solid #F4A836;
        border-radius: 12px;
        padding: 1.5rem;
    }
    .billing-card .plan-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .billing-card .plan-price {
        font-size: 1.2rem;
        color: #F4A836;
        font-weight: 600;
    }
    .billing-card .detail {
        color: #666;
        margin: 0.3rem 0;
    }
    .info-card {
        background: #FFFFFF;
        border: 2px solid #F4A836;
        border-radius: 10px;
        padding: 1.25rem;
        height: 100%;
    }
    .info-card h4 {
        color: #1E3A5F;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .info-card p {
        color: #666;
        font-size: 0.9rem;
        margin: 0;
    }
    .danger-zone {
        background: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 1.5rem;
    }
    .danger-zone h4 {
        color: #EF4444;
        margin-top: 0;
    }
    .toggle-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #E5E7EB;
    }
    .toggle-row:last-child {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# ------------------------------------------------------------------
# Navy gradient banner header
# ------------------------------------------------------------------

st.markdown("""
<div class="navy-banner">
    <div class="title">⚙️ Admin & Settings</div>
    <div class="subtitle">Account management, API access, and billing configuration</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 2: User Profile Card
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>👤 User Profile</div>", unsafe_allow_html=True)

st.markdown("""
<div class="profile-card">
    <div class="avatar">NS</div>
    <div class="profile-info">
        <h3>Nadya Salsabila</h3>
        <p><span class="role-badge">Admin</span></p>
        <p>📧 nadya@solaryield.io</p>
        <p>🏢 SolarYield Pte. Ltd.</p>
        <p>📅 Member since: April 2026</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 3: API Access
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>🔑 API Access</div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="api-key-box">sk-sy-••••••••••••••••••••••3f8a</div>', unsafe_allow_html=True)

with col2:
    st.write("")
    st.write("")
    copy_clicked = st.button("📋 Copy API Key", width='stretch')

if copy_clicked:
    st.success("API key copied to clipboard")

col1, col2 = st.columns(2)

with col1:
    regen_clicked = st.button("🔄 Regenerate Key", width='stretch')

if regen_clicked:
    st.warning("Are you sure? This will invalidate your current key.")

st.markdown(
    "<div style='background: #F0F9FF; border-left: 4px solid #1E3A5F; padding: 0.75rem 1rem; border-radius: 0 6px 6px 0; color: #374151; font-size: 0.9rem;'>"
    "ℹ️ Use this key to integrate SolarYield forecasts into your SCADA system or trading platform. "
    "Rate limit: 1,000 calls/day on Professional plan."
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 4: Billing and Plan
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>💳 Billing & Plan</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="billing-card">
        <div class="plan-name">Professional</div>
        <div class="plan-price">USD 499/month</div>
        <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 1rem 0;">
        <div class="detail">📍 Sites: <strong>5 of 5 used</strong></div>
        <div class="detail">📊 API calls this month: <strong>342 of 1,000</strong></div>
        <div class="detail">📅 Next billing date: <strong>May 28, 2026</strong></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.write("")
    st.write("")
    upgrade_clicked = st.button("⬆️ Upgrade to Enterprise", width='stretch', type="primary")
    st.write("")
    invoice_clicked = st.button("📄 Download Invoice", width='stretch')

if upgrade_clicked:
    st.info("Enterprise plan includes unlimited sites, custom ML model, white-label option, and dedicated support. Contact sales@solaryield.io")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 5: Notification Preferences
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>🔔 Notification Preferences</div>", unsafe_allow_html=True)

# Toggle states (default True)
if "toggle_anomaly" not in st.session_state:
    st.session_state.toggle_anomaly = True
if "toggle_daily" not in st.session_state:
    st.session_state.toggle_daily = True
if "toggle_weekly" not in st.session_state:
    st.session_state.toggle_weekly = True
if "toggle_grid" not in st.session_state:
    st.session_state.toggle_grid = True

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**Alert Type**", unsafe_allow_html=True)

    toggle_anomaly = st.toggle("Email alerts when anomaly detected", value=st.session_state.toggle_anomaly, key="toggle_anomaly")
    toggle_daily = st.toggle("Daily forecast summary at 7am SGT", value=st.session_state.toggle_daily, key="toggle_daily")
    toggle_weekly = st.toggle("Weekly performance report (Mondays)", value=st.session_state.toggle_weekly, key="toggle_weekly")
    toggle_grid = st.toggle("Grid penalty risk alerts (>20% below forecast)", value=st.session_state.toggle_grid, key="toggle_grid")

with col2:
    st.write("")
    st.write("")
    alert_email = st.text_input("Alert email address", value="nadya@solaryield.io")

saved_prefs = st.button("💾 Save Preferences", type="primary")

if saved_prefs:
    st.success("Notification preferences saved.")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 6: Data Governance
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>🔒 Data Governance & Compliance</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>📋 PDPA Compliant</h4>
        <p>All metering data stored in AWS ap-southeast-1 Singapore. Data processing agreements available on request.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🔐 ISO 27001 Roadmap</h4>
        <p>Security certification targeted for Month 6. Current controls: encryption at rest, TLS 1.3, role-based access.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>🤖 AI Governance</h4>
        <p>Model decisions logged with SHAP explanations. Audit trail exportable. Aligned with Singapore AI Verify framework.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
dpa_clicked = st.button("📥 Download Data Processing Agreement (PDF)")

if dpa_clicked:
    st.info("DPA document will be emailed to nadya@solaryield.io within 24 hours.")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SECTION 7: Danger Zone
# ------------------------------------------------------------------

st.markdown("<div class='section-header'>⚠️ Danger Zone</div>", unsafe_allow_html=True)

st.markdown("""
<div class="danger-zone">
    <h4>⚠️ Irreversible Actions</h4>
    <p style="color: #666; margin-bottom: 1rem;">These actions cannot be undone. Please proceed with caution.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    delete_clicked = st.button("🗑️ Delete Account", width='stretch', type="secondary")
    if delete_clicked:
        st.error("Account deletion requires confirmation from admin@solaryield.io. This action cannot be undone.")

with col2:
    export_clicked = st.button("📤 Export All Data", width='stretch', type="secondary")
    if export_clicked:
        st.success("Data export initiated. You will receive a download link at nadya@solaryield.io within 1 hour.")

st.markdown("<hr class='amber-divider'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------

st.caption("☀️ SolarYield Admin & Settings · SolarYield Pte. Ltd. · Singapore")
