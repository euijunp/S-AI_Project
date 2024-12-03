# S-AI_Project  
# RAMP (Roadmap for Aspiring Professionals)  
URL: [http://220.67.145.50:5000](http://220.67.145.50:5000)  

**Project Duration:** August 28, 2024 ~ August 30, 2024 (3 days)  

## Project Overview  

This project aims to develop an AI-based career recommendation service to assist users in making career choices. By utilizing open APIs from platforms like CareerNet, Q-Net, and WorkNet, we collect data on occupations, academic programs, and certifications. This data is processed using AI language models to deliver personalized career information. Additionally, the service provides offline functionality for user convenience.  

## Project Objectives  

### Main Objective  
- **Deliver AI-driven career recommendation services** tailored to individual users.  

### Detailed Objectives  
1. **Leverage CareerNet and WorkNet APIs for data collection and preprocessing**  
   - Collect and preprocess data, including occupational encyclopedias, academic programs, and career outlooks.  
2. **Process data and provide recommendations using language models**  
   - Input the preprocessed data into the Ollama - llama3.1 language model to deliver personalized career recommendations.  
3. **Implement on-device functionality**  
   - Enable offline access to career information for users.  
4. **Integrate certification information**  
   - Use Q-Net APIs to collect certification details and incorporate them into career recommendations.  

## Models and Technologies Used  

- **Primary Models:**  
  - Ollama - phi3.5 or GPT-4o  

- **Technologies Utilized:**  
  1. **CareerNet OpenAPI**  
     - Collect occupational and academic program data for personalized recommendations.  
  2. **Q-Net OpenAPI**  
     - Gather certification data for career decision support.  
  3. **WorkNet OpenAPI**  
     - Provide detailed information on job characteristics, prospects, licenses, related roles, and tasks.  
  4. **Flask**  
     - Build the web application and implement server-client data communication.  
  5. **deep-translator**  

## Project Timeline  

### Day 1 (August 28, 2024)  
- **Data collection and preprocessing using CareerNet API**  
  - **Seonghyun Park:** Collect occupational and academic data from CareerNet.  
  - **Euijun Park:** Perform data preprocessing and apply the language model.  
  - **Jaehan Park:** Develop basic career recommendation features.  

### Day 2 (August 29, 2024)  
- **Build and test the web-based service**  
  - **Seonghyun Park:** Design and implement the user interface.  
  - **Euijun Park:** Create a web-based API using Flask.  
  - **Jaehan Park:** Test and refine career recommendation functionalities.  

### Day 3 (August 30, 2024)  
- **Integrate Q-Net API data**  
  - **Seonghyun Park & Jaehan Park:** Collect certification data and integrate it with the recommendation service. Attempt web page creation and integration.  
  - **Euijun Park:** Perform end-to-end service testing, debugging, and finalize the project output.  

## Expected Deliverables  

- **AI-based Career Recommendation Web Service**  
  - Provide customized career recommendations, including occupations, academic programs, and certifications.  
  - User-friendly web interface.  
  - On-device functionality for offline usage.  

- **Project Documentation and Report**  
  - API usage guide and code explanations.  
  - Overview of language model application and data preprocessing.  
  - Project outcomes and suggestions for future improvements.  

## Final Deliverables  

- **AI-based Career Recommendation Web Service**  
  - Tailored career recommendations with occupational and academic details.  
  - Simple and intuitive web interface.  
  - Offline capability for on-device use.  

- **Areas for Improvement**  
  - Expand data collection and model training.  
  - Enhance interface design.  
  - Optimize AI model training speed.  
  - Improve integration with web services.  
