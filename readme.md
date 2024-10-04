# Rapidious Backend

This project is the backend component of the Rapidious application, built with Python Flask and OpenSearch. It uses Docker to simplify the deployment and management of OpenSearch and other service dependencies.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)

## Setup Instructions

1. **Install Docker Desktop**

   Download and install Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. **Clone the Backend Repository**

   Clone the repository to your local machine using the following command:

    ``` git clone https://github.com/your-username/rapidious_backend.git ```

3. **Navigate to the Project Directory**

    Change into the project directory:
    
    ``` cd rapidious_backend ```

4. **Set Up OpenSearch**

    In the `docker-compose.yml` file, find the `OPENSEARCH_INITIAL_ADMIN_PASSWORD` field and set your desired password.

5. **Download the Dataset**

    Download the dataset from Kaggle at the following URL: [EpiRecipes Dataset](https://www.kaggle.com/datasets/hugodarwood/epirecipes)

    You will need the `full_format_recipes.json` file from this dataset.

6. **Copy the Dataset**

    Copy the `full_format_recipes.json` file into the project working directory.

7. **Run Docker Compose**

    Initialize and start the OpenSearch service by running:

    ``` docker-compose up ```
    
    Sit back and relax while Docker sets up the containers.

8. **Environment Variables**

    Create a `.env` file in the root directory of the project and populate it with the fields shown in `.env.example`. The default admin username will be `admin`, and the password will be the one you set up in the `docker-compose.yml`.

9. **Install Dependencies**

    Install all Python dependencies required for the backend:

    ``` pip install-r requirments.txt ```


10. **Start the Backend Server**

    Start the backend server by running:

    ```
    python app.py
    ```

    The server will start on port 80.

11. **Verify Server Running**

    Go to [http://localhost](http://localhost) to check if the server is running correctly.

12. **Clone the Frontend**

    Clone the frontend repository from: https://github.com/Akhil4264/rapidious_frontend






