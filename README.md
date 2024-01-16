# My REST API

This API allows you to interact with our service to fetch and analyze GitHub repository events. Below you'll find basic instructions on how to set up and use the API.

## Getting Started

### Prerequisites

- Python 3.6 or higher is required.
- Refer to `requirements.txt` for necessary packages.

### Installation

1. Clone the repository to your local machine:
git clone [URL of the repository]

css
Copy code

2. Navigate to the cloned repository:
cd [repository name]

markdown
Copy code

3. Install the required dependencies:
pip install -r requirements.txt

bash
Copy code

### Running the Application

To run the application, execute the following command in the root directory of the project:
python main.py

markdown
Copy code
This will start the Flask server, and the API will be accessible at `http://localhost:5000/api`.

### Optional Authentication

To increase the number of possible API requests, you can create a file named auth_config.txt in the application directory and copy your GitHub token into this file. This token will be used to authenticate API requests. Ensure to keep this token secure to prevent unauthorized access.

## API Endpoints

### `/api/statistics`

- **Method**: GET
- **Description**: Fetches event statistics for a specified GitHub repository.
- **Query Parameters**:
  - `repository_name`: The name of the GitHub repository.
- **Example Request**:
curl http://localhost:5000/api/statistics?repository_name=[repository name]

markdown
Copy code
- **Response**: A JSON object containing the statistics of the requested repository.

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of an API request:

- `200 OK`: The request was successful.
- `400 Bad Request`: The request was invalid or cannot be served. Check the message for details.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: The server encountered an error processing your request.
