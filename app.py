import streamlit as st
import pandas as pd

from expense_manager import initialize_csv, save_expense, load_expenses, delete_expense, update_expense
from predictor import predict_category
from analytics import monthly_summary
import matplotlib.pyplot as plt
from analytics import predict_next_month_budget

st.title('Smart Expense Tracker')

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Expense",
    "📋 History",
    "📊 Analytics",
    "💰 Budget"
])

initialize_csv()

with tab1:
    st.subheader("Add Expense")

    with st.form("expense_form"):

        description = st.text_input("Description")

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        submitted = st.form_submit_button("Save Expense")

        if submitted:

            predicted_category = predict_category(description)

            save_expense(
                description,
                amount,
                predicted_category
            )

            st.success(
                f"Saved under {predicted_category}"
            )

            st.rerun()

with tab2:
    st.subheader("Expense History")

    df = load_expenses()

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(
        by="date",
        ascending=False
    )

    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([4, 2, 4, 2, 2])

        with col1:
            st.write(f"{row['description']} - {row['category']}")

        with col2:
            st.write(f"Rs. {row['amount']}")
            
        with col3:
            st.write(f"{row['date'].strftime('%d %b %Y %I:%M %p')}")

        with col4:
            if st.button("Edit", key=f"edit_{row['id']}"):
                st.session_state["edit_id"] = row["id"]
                st.session_state["edit_description"] = row["description"]
                st.session_state["edit_amount"] = row["amount"]

        with col5:
            if st.button("Delete", key=f"del_{row['id']}"):
                delete_expense(row["id"])
                st.rerun()

    if "edit_id" in st.session_state:

        st.subheader("✏️ Edit Expense")

        new_description = st.text_input(
            "Description",
            value=st.session_state["edit_description"]
        )

        new_amount = st.number_input(
            "Amount",
            value=float(st.session_state["edit_amount"])
        )

        if st.button("Update Expense"):
            update_expense(
                st.session_state["edit_id"],
                new_description,
                new_amount,
                predict_category(new_description)
            )

            st.success("Expense updated!")

            # clear edit state
            del st.session_state["edit_id"]
            del st.session_state["edit_description"]
            del st.session_state["edit_amount"]

            st.rerun()

with tab3:
    st.subheader("Monthly Summary")

    summary = monthly_summary()

    if summary is not None:
        st.write(summary)

    df = load_expenses()

    if not df.empty:
        st.subheader("Category Chart")

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        df.groupby("category")["amount"].sum().plot(kind="bar", ax=ax)

        st.pyplot(fig)

with tab4:
    st.subheader("Budget Prediction")

    prediction = predict_next_month_budget()

    st.info(f"Predicted next month spending: Rs. {prediction}")