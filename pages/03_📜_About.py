import streamlit as st

st.set_page_config(
     page_title="ELRO Gameboard",
     page_icon="🎲",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "# Weekly games. Answer questions and compete against other grades"
     }
)



with open('./database/about.txt', 'r') as f:
    about = f.read()
    st.markdown(about)


# Show extra buttons for admin users.
ADMIN_USERS = st.secrets["admin_users"]
if st.experimental_user.email in ADMIN_USERS:

    # Edit about form
    with st.form("Add contributor"):
        about_update = st.text_area("Update", value=about)
        submit_button = st.form_submit_button("Update")
    if submit_button:
        with open("./database/about.txt", "w") as f:
            f.write(about_update)
        st.success("About updated!")
        st.experimental_rerun()