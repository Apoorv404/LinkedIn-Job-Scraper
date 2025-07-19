import streamlit as st
import subprocess
import sys

st.set_page_config(page_title="LinkedIn Job Automation", layout="centered")
st.title("LinkedIn Job Scraper")

st.write("Enter the job role and location to start the automation process.")

role = st.text_input("Job Role", "Python Developer")
location = st.text_input("Location", "India")

if st.button("Run Automation"):
    st.info(f"Starting automation for Role: '{role}', Location: '{location}'...")
    
    # Display a spinner while the process is running
    with st.spinner("Running job automation... This may take a while."):
        try:
            # Run main.py as a subprocess, passing role and location as arguments
            # We'll need to modify main.py to accept these arguments
            process = subprocess.Popen(
                [sys.executable, "main.py", role, location],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1, # Line-buffered output
                universal_newlines=True # Ensure cross-platform newline handling
            )

            # Display output in real-time
            st.subheader("Automation Output:")
            output_container = st.empty()
            full_output = []

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    full_output.append(output)
                    output_container.code("".join(full_output), language='bash') # Use 'bash' for general console output

            stderr_output = process.stderr.read()
            if stderr_output:
                st.error("Errors during automation:")
                st.code(stderr_output, language='bash')

            if process.returncode == 0:
                st.success("Automation completed successfully!")
            else:
                st.error(f"Automation failed with exit code {process.returncode}.")

        except FileNotFoundError:
            st.error("Error: main.py not found. Make sure it's in the same directory.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- View Jobs Button ---
if st.button("View Jobs"):
    st.subheader("All Scraped Jobs:")
    try:
        import pandas as pd
        jobs_df = pd.read_csv("jobs.csv")
        if not jobs_df.empty:
            st.dataframe(jobs_df[['Role', 'Company', 'Location']])
        else:
            st.info("No jobs found in jobs.csv. Run the automation first.")
    except FileNotFoundError:
        st.info("jobs.csv not found. Run the automation to create it.")
    except Exception as e:
        st.error(f"Error loading jobs data: {e}")

# --- Job Frequency Visualization ---
st.markdown("### Job Frequency by Company")

try:
    import pandas as pd
    jobs_df = pd.read_csv("jobs.csv")
    if not jobs_df.empty:
        company_counts = jobs_df['Company'].value_counts().reset_index()
        company_counts.columns = ['Company', 'Job Count']
        st.bar_chart(company_counts.set_index('Company'))
    else:
        st.info("No job data available to visualize. Run the automation first.")
except FileNotFoundError:
    st.info("jobs.csv not found. Run the automation to create it.")
except Exception as e:
    st.error(f"Error loading or visualizing data: {e}")

st.markdown("---")
st.write("Developed by Apoorv")
