# Dark Patterns Detection Chrome Extension

## Introduction
This repository contains a Chrome extension designed to detect dark patterns in e-commerce websites. Dark patterns are deceptive design practices intended to manipulate users into making unintended choices. This extension identifies and flags these patterns to promote transparent and user-friendly online shopping experiences.

## Features
- Detects various types of dark patterns, such as:
    - Urgency
    - Scarcity
    - Misdirection
    - Social Proof
    - Obstruction
    - Sneaking
    - Forced Action
- Provides detailed explanations for detected patterns.
- Marks and highlights the elements on the webpage that exhibit dark patterns.
- Allows users to submit feedback on the accuracy of the detection.
- Stores user feedback for further analysis and improvement of the detection algorithms.
- Offers a user-friendly interface for easy navigation and interaction.

## Technologies Used
The following technologies and programming languages are used in this project:
- **HTML**: For the extension's user interface.
- **CSS**: For styling the extension's popup and options pages.
- **JavaScript**: For webpage analysis and interaction.
- **JSON**: For configuration and data storage.

The following technologies and libraries are utilized in the backend server (`MainServer.py`) for this project:

- **Python**: The primary programming language for backend development.
    - **Flask**: A lightweight web framework used to create the backend API.
    - **Flask-CORS**: For enabling Cross-Origin Resource Sharing (CORS) to allow communication between the frontend and backend.
    - **pandas**: For handling and exporting data to CSV files.
    - **spacy**: For natural language processing, including sentence segmentation and classification.
    - **deep-translator**: For translating text into English when necessary.
    - **selenium**: For web scraping and extracting webpage content.
    - **sys**: For error logging and debugging.
- **Chrome WebDriver**: Used with Selenium for headless browser automation.
- **CSV Files**: For storing scraped data and user feedback persistently.
- **SQLite**: For storing user reports and detected patterns persistently.

## Installation
To install and set up the Chrome extension, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/ashish379soni/Dark-Patterns-Detection-Extension.git
    ```
2. Open Google Chrome and navigate to `chrome://extensions/`.
3. Enable **Developer mode** by toggling the switch at the top-right corner.
4. Click on **Load unpacked** and select the directory where the repository was cloned.
5. Start the backend server:

  - Navigate to the server directory:
    ```bash
    cd server
    ```
  - (Optional) Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
  - Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
  - Start the backend server:
    ```bash
    python MainServer.py
    ```
6. Refresh the extension in Chrome to ensure it connects to the running server.

## Usage
Once installed, the extension can be used as follows:
1. Open an e-commerce website in your browser.
2. The extension will automatically analyze the webpage and highlight detected dark patterns.
3. Click on the extension icon in the browser toolbar to view a detailed report of the detected patterns.

### Backend API Endpoints
The backend server provides the following API endpoints to support the functionality of the Dark Patterns Detection Chrome Extension:

- **`POST /`**  
  - **Description**: Accepts a JSON payload containing a URL, scrapes the webpage content, analyzes it for dark patterns, and returns the detected patterns categorized by type.  
  - **Request Body**:  
    ```json
    {
      "URL": "https://example.com"
    }
    ```
  - **Response**:  
    A JSON object containing the detected dark patterns and their categories.  
    Example:  
    ```json
    {
      "Forced Continuity": ["Example text 1", "Example text 2"],
      "Hidden Costs": ["Example text 3"]
    }
    ```

- **`GET /feedback`**  
  - **Description**: Serves the feedback form for users to provide their input on the detected patterns.

- **`GET /thankyou`**  
  - **Description**: Displays a thank-you page after the user submits feedback.

- **`POST /submit-form`**  
  - **Description**: Accepts user feedback in JSON format and appends it to the `FeedbackData.csv` file for further analysis.  
  - **Request Body**:  
    A JSON object containing user feedback.  
    Example:  
    ```json
    {
      "feedback": "The detection was accurate and helpful."
    }
    ```
  - **Response**:  
    Returns the submitted feedback as a confirmation.

These endpoints enable seamless communication between the Chrome extension and the backend server, ensuring efficient detection and reporting of dark patterns.

### Configuration
- The backend server runs on `http://127.0.0.1:5000` by default. Ensure this URL is accessible for the extension to function correctly.
- You can modify the server port in `MainServer.py` by updating the following line:
    ```python
    app.run(host='127.0.0.1', port=5000)
    ```
  Replace `5000` with your desired port number.

## Contributing
We welcome contributions to improve this project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add your meaningful commit message here"
    ```
4. Push your branch to your forked repository:
    ```bash
    git push origin feature-name
    ```
5. Submit a pull request with a clear description of your changes.

## License
This project is licensed under the [MIT License](LICENSE). Please see the `LICENSE` file for more details.

## Acknowledgments
- Inspired by the need to promote ethical design practices in e-commerce.
- Special thanks to the developers and contributors who made this project possible.
