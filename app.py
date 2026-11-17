
import streamlit as st
import pandas as pd

st.title("Student Record Management System")

# Store student records
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course"]
    )

st.sidebar.title("Menu")
choice = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if choice == "Add Student":
    st.header("Add Student")

    roll = st.number_input("Roll No", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    course = st.text_input("Course")

    if st.button("Add"):
        if name and course:
            if roll not in st.session_state.students["Roll No"].values:
                new_student = {
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course
                }

                st.session_state.students.loc[len(st.session_state.students)] = new_student
                st.success("Student added successfully!")
            else:
                st.error("Roll number already exists")
        else:
            st.warning("Please enter all details")

# READ
elif choice == "View Students":
    st.header("All Student Records")
    st.dataframe(st.session_state.students)

# UPDATE
elif choice == "Update Student":
    st.header("Update Student")

    roll = st.number_input("Enter Roll No", min_value=1, step=1)

    if st.button("Search"):
        if roll in st.session_state.students["Roll No"].values:
            st.session_state.selected_roll = roll
        else:
            st.error("Student not found")

    if "selected_roll" in st.session_state:
        index = st.session_state.students[
            st.session_state.students["Roll No"] ==
            st.session_state.selected_roll
        ].index[0]

        name = st.text_input("New Name", value=st.session_state.students.loc[index, "Name"])
        age = st.number_input("New Age", min_value=1, value=int(st.session_state.students.loc[index, "Age"]))
        course = st.text_input("New Course", value=st.session_state.students.loc[index, "Course"])

        if st.button("Update"):
            st.session_state.students.loc[index, ["Name", "Age", "Course"]] = [
                name, age, course
            ]
            st.success("Record updated successfully!")
            del st.session_state.selected_roll

# DELETE
elif choice == "Delete Student":
    st.header("Delete Student")

    roll = st.number_input("Enter Roll No to Delete", min_value=1, step=1)

    if st.button("Delete"):
        if roll in st.session_state.students["Roll No"].values:
            st.session_state.students = st.session_state.students[
                st.session_state.students["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student deleted successfully!")
        else:
            st.error("Student not found")
