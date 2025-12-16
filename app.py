import streamlit as st
import pandas as pd

# ---------------- APP CONFIG ----------------
st.set_page_config(
    page_title="RetailSenseAgent AI",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/ui_sample_data.csv")

# ---------------- ADD DEFAULT ML COLUMNS ----------------
# These will be replaced by ML later
if "Predicted_Demand" not in df.columns:
    df["Predicted_Demand"] = df["Daily_Sales"]  # temporary placeholder
if "Overstock_Days" not in df.columns:
    df["Overstock_Days"] = 0  # temporary placeholder
if "Action" not in df.columns:
    df["Action"] = "No action"  # temporary placeholder
if "Priority" not in df.columns:
    df["Priority"] = "Medium"  # temporary placeholder

# ---------------- DERIVED UI SIGNALS ----------------
df["Demand_Spike"] = df.apply(
    lambda r: "Yes" if r["Predicted_Demand"] >= (r["Stock"] * 1.5 if r["Stock"] > 0 else r["Predicted_Demand"]) else "No",
    axis=1
)

df["Long_Overstock"] = df["Overstock_Days"].apply(lambda x: "Yes" if x >= 30 else "No")

# ---------------- SIDEBAR ----------------
st.sidebar.title("RetailSenseAgent")
st.sidebar.caption("Intelligent Inventory Agent")
page = st.sidebar.radio("Navigation", ["Overview", "Inventory", "Action Center"])

# ---------------- HEADER ----------------
st.title("RetailSenseAgent AI")
st.caption("Action-Driven Retail Intelligence Platform")

# ---------------- OVERVIEW ----------------
if page == "Overview":
    st.subheader("System Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", len(df))
    col2.metric("High Priority Alerts", (df["Priority"] == "High").sum())
    col3.metric("Demand Spikes", (df["Demand_Spike"] == "Yes").sum())
    col4.metric("Long Overstock Items", (df["Long_Overstock"] == "Yes").sum())
    st.markdown("### Priority Snapshot")
    st.dataframe(df[["Product","Category","Sub_Category","Action","Priority"]], use_container_width=True)

# ---------------- INVENTORY ----------------
elif page == "Inventory":
    st.subheader("Inventory Status")
    st.dataframe(
        df[
            [
                "Product","Category","Sub_Category","Stock","Predicted_Demand",
                "Demand_Spike","Overstock_Days","Expiry_Date"
            ]
        ],
        use_container_width=True
    )

# ---------------- ACTION CENTER ----------------
else:
    st.subheader("Action Center")
    st.caption("Agent-detected issues requiring human decision")
    actionable = df[df["Priority"] != "Low"]

    for _, row in actionable.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['Product']}")
            st.write(f"Category: {row['Category']} | Sub-Category: {row['Sub_Category']}")
            st.write(f"Recommended Action: **{row['Action']}** | Priority: **{row['Priority']}**")

            if row["Demand_Spike"] == "Yes":
                st.warning("Demand spike detected. Reorder recommended.")

            if row["Long_Overstock"] == "Yes":
                st.warning(f"Overstocked for {row['Overstock_Days']} days. Clearance action recommended.")
                st.markdown("**Choose Discount Strategy**")
                discount_option = st.radio(
                    "Discount Plan",
                    [
                        "10% for 30 days",
                        "20% for 20 days",
                        "40% for 10 days (fast clearance)"
                    ],
                    key=f"discount_{row['ID']}"
                )

            col1, col2, col3 = st.columns(3)
            with col1:
                owner_email = st.text_input("Owner Email", placeholder="owner@company.com", key=f"owner_email_{row['ID']}")
            with col2:
                supervisor_email = st.text_input("Supervisor Email", placeholder="supervisor@company.com", key=f"supervisor_email_{row['ID']}")
            with col3:
                whatsapp_group = st.text_input("WhatsApp Group ID", placeholder="Retail_Staff_Group", key=f"group_{row['ID']}")

            if st.button("Confirm & Trigger Notification", key=f"send_{row['ID']}"):
                st.success("Decision recorded. Notifications will trigger after ML/backend integration.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Note: Demand prediction, overstock duration, and notifications will be handled by ML/backend once integrated.")
