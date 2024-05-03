# ImpactNet

ImpactNet is a cutting-edge analytics platform that transforms publicly available Indian government data into actionable insights. Designed to streamline the decision-making process for Corporate Social Responsibility (CSR) initiatives, this system leverages advanced data visualization tools and an intuitive chatbot interface, empowering users to explore and interact with complex datasets efficiently.

## Contents
1. **Problem Description**
2. **What is ImpactNet?**
3. **Impact of this project**
   - Business Value
   - Community Value
4. **User Personas**
5. **Capabilities for each User Persona**
6. **Implementation Details**
7. **Technical Features & Capabilities**
7. **Installation & Evaluation of the Product** 
8. **How to run different modules?**
9. **Contribution**
10. **Scope Limitation**
11. **Future Scope**
12. **License**

## Problem Description
The Indian Government mandates corporations with either more than INR 5 Crores in net profit or a market capitalization exceeding INR 500 Crores to allocate at least 2% of their annual net profit to CSR activities. Currently, these corporations partner with Non-Profit organizations to fulfill this requirement. However, there lacks a streamlined solution for these stakeholders to analyze data effectively and make targeted decisions.

The necessary datasets are scattered, primarily available through data.gov.in APIs and buried in extensive PDF reports by government entities. This fragmentation requires extensive manual effort to prepare and process data for strategic decision-making.

## What is ImpactNet?
ImpactNet elegantly addresses these challenges through a robust, multi-faceted approach:
### Data Processing Layer (ETL: Extract-Transform-Load)
1. **Automated Data Aggregation:** Fetches and processes data from data.gov.in, creating structured data tables for subsequent analysis within the Metabase interface.
2. **Insight Extraction:** Converts insights from government-issued PDFs into digestible formats, ready for integration with our proprietary Retrieval Augmented Generation (RAG) system.

### Data Visualization and Insight Generation Layer
1. **Dynamic Data Visualization:** Users can interact with data through the user-friendly Metabase interface or execute SQL queries to delve deeper into the datasets. This functionality is complemented by the ability to generate comprehensive reports and dashboards.
![Flow Diagram](/Metabase.jpg)
2. **Intelligent Query Handling Chatbot:** Utilizes a state-of-the-art RAG system, powered by Gemini 1.5 Pro, to answer queries regarding government data. The system provides precise answers with relevant textual information and graphical representations.
![Flow Diagram](/chatbot.jpg)
## Impact of this project
### Business Value
The project enables Non-Profit organizations to streamline their data driven decision-making processes, enhancing efficiency and effectiveness in allocating CSR funds.
### Community Value
Facilitates more informed and faster decision-making by Non-Profits, likely leading to improved performance metrics in CSR projects. This product is expected to improve clarity, and increasing stakeholder engagement with respect to strategic decision making in CSR activites.

## User Personas
ImpactNet caters to two distinct types of users:
1. **Data-Savvy Users**: These users possess skills in data analysis and visualization, enabling them to leverage advanced tools to extract deep insights from complex datasets. Here, Metabase interface provides significant value add to this set of users. 
2. **General Users**: This group includes stakeholders who may not have technical data skills but need to understand and utilize data insights for decision-making. Here, the chatbot application fits in well.

## Capabilities for each User Persona
ImpactNet integrates several high-level functionalities to support robust data management and user interaction:
- **Interactive Data Querying for Data-Savvy Users**: Users can access and manipulate complex data efficiently via the Metabase interface.
- **Advanced Q&A System for General Users**: Employs a natural language processing interface for engaging and detailed data exploration.

## Implementation Details
ImpactNet is architectured around three core modules, each designed to streamline data processing and enhance decision-making in CSR initiatives:

### Module 1: Data Processing and Ingestion
This module automates the ingestion of government data from data.gov.in via API or directly from PDF reports provided by various government bodies. It simplifies the initial data handling, ensuring readiness for further analysis. More detailed technical work flow is mentioned in the image below:

![Flow Diagram](/system_architecture_m1.jpeg)

### Module 2: Data Visualization with Metabase
Following data ingestion, this module leverages the power of Google Cloud SQL and Metabase for advanced data analysis. It is particularly useful for users proficient in Metabase and SQL, offering dynamic visualization tools to uncover actionable insights.

![Flow Diagram](/system_architecture_m2.jpg)

### Module 3: Q&A Chatbot with Custom RAG Pipeline
![Flow Diagram](/system_architecture_m3.jpg)

This interactive chatbot utilizes a custom Retrieval Augmented Generation (RAG) system, facilitating an intuitive query experience for users. It's designed for those requiring a more guided approach to explore data insights through natural language interactions.

## Technical Features & Capabilities
- **Automated Data Schema Management**: Dynamically manages database schemas to accommodate varying API responses.
- **Cloud SQL Integration**: Ensures scalable and secure data storage and retrieval within Google Cloud SQL.
- **Metabase Utilization**: Facilitates sophisticated data analysis, enabling users to create dashboards and generate comprehensive reports.
- **Interactive Q&A Interface**: Features a Streamlit-based frontend for intuitive interaction with data using natural language queries.
- **Advanced Text Processing**: Incorporates a custom RAG system along with Gemini 1.5 Pro for effective text extraction, cleaning, summarization, and response generation.

## Installation & Evaluation of the Product

### Prerequisites

- Python 3.11 or later.
- Google Cloud account with an active Cloud postgreSQL, Metabase deployment, Cloud Storage and Firestore for Vector search.
- Set up IAM and configure the right credentials to utilize all the necessary components.
- Streamlit installed either locally or in the cloud.

### Setup
 
1. Clone the project repository from the github console
2. Install the required Python packages:
    ```bash
    python -m venv impactnet_env
    source impactnet_env/bin/activate
    pip install -r requirements.txt
    ```
3. Utilize the env file with placeholders provided in the root directory to configure your envrionment variables.
4. Process the sample PDF data and the URL available in the `sample_data` folder on the data integration module.

## How to run different modules?

### Module 1: Running the Data Integration Module

From the root folder,execute the main app file to process and load data via URL or by uploading PDFs:

```bash
python app.py
```
### Module 2: Running Metabase Analytics System

Deploy metabase application to start interacting with the advanced data anlaytics system. Ensure that you connect your cloudSQL data to metabase via the admin portal of Metabase and then access the data within Metabase for analysis.

### Module 3: Running the chatbot System

Move into backend_chatbot and launch the Streamlit application to start interacting with the chatbot system:

```bash
streamlit run chat_app.py
```
## Sample Data

To facilitate a smooth start with ImpactNet, we have included sample data in the `sample_data` directory. To get started, please follow the detailed setup instructions provided in the documentation to configure the project correctly. Once the setup is complete, you can process the sample data according to the outlined steps.

After processing, both the Metabase data visualization platform and the interactive chatbot will be fully operational. This will allow you to explore the capabilities of ImpactNet using predefined data sets, demonstrating how the system can transform complex data into actionable insights.

This guide ensures that you can quickly experience the full functionality of the application with minimal setup. 

## Contribution

We encourage you to explore the project and provide feedback on features and performance.

## Scope Limitation
ImpactNet currently focuses on data relevant to Higher Education in India. To expand its utility, additional datasets such as those from healthcare, poverty alleviation, and environmental sectors can be incorporated by providing their respective URLs or uploading their PDFs.

## Future Scope
The roadmap for ImpactNet includes several exciting enhancements:
- **Broadening Data Sources**: Incorporating a wider array of data related to CSR, including sectors like healthcare, poverty, and environmental sustainability.
- **Enhanced Interactivity**: Integrating the stream content generation capabilities of Gemini 1.5 Pro to enhance user interactions.
- **Usage Controls**: Introducing rate limits to prevent misuse and ensure fair access to all users.
- **Robust Security**: Implementing comprehensive user authentication and authorization measures to bolster security.
- **Advanced Diagnostics**: Developing sophisticated error logging mechanisms to facilitate deeper analysis of issues and provide root cause analysis.

## License
Till the completion of Google AI Hackathon, ImpactNet will be available under a special license designed to allow use and modification for hackathon moderators while restricting replication and distribution. Post-hackathon completion, the project will revert to a more restrictive licensing model, details of which will be specified in the LICENSE file.