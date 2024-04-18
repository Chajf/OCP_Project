# 4Chan Sentiment Analysis Application

This application is a **multi-container** web application designed to scrape posts from the popular online platform, **4Chan**, and perform sentiment analysis on the replies to these posts. The primary goal of the application is to predict and categorize the sentiments of the replies as either **positive** or **negative**.

## Application Components

The application is composed of several interconnected containers, each serving a specific purpose:

1. **Page Scraping Container**: This container is responsible for scraping posts from 4Chan. It navigates through the site's pages, identifies posts, and extracts the necessary data.

2. **UI Container**: This container manages the user interface of the application. It presents the scraped data and sentiment analysis results in a user-friendly and intuitive manner.

3. **Database Container**: This container handles data storage and retrieval. It stores the scraped posts and the results of the sentiment analysis for future reference and analysis.

4. **Sentiment Model Container**: This container houses the sentiment analysis model. It takes the scraped posts as input and predicts the sentiment of the replies, categorizing them as either positive or negative.

5. **FastAPI Container**: This is the main container that handles communication between all other containers. It uses the FastAPI framework to ensure efficient and reliable communication.

## Application Diagram

<p align="center">
    <img src="/images/OCP_diagram.png" height="500">
</p>

This is the application diagram that shows the architecture of the application and how the different containers interact with each other.

## Application Interface

### Initial UI

<p align="center">
    <img src="/images/ui_nodata.png" height="700">
</p>

This is how the user interface looks like when the application is started. It's clean and ready for the user to interact with.

### Wordcloud from Scraped Text

<p align="center">
    <img src="/images/ui_scrape.png" height="700">
</p>

After scraping the posts, a wordcloud is generated to visually represent the most frequently used words in the scraped threads.

### Sentiment Barplot

<p align="center">
    <img src="/images/ui_bar.png">
</p>

This barplot shows the sentiment analysis results for the entire database. It categorizes the sentiments as either positive or negative and displays the count of each.

## Local Deployment and Running Instructions

This application is containerized using Docker, which makes it easy to deploy and run locally. Here are the steps to do so:

1. **Prerequisites**: Ensure that you have Docker and Docker Compose installed on your system. If not, you can download them from the Docker official website.

2. **Clone the Repository**: Clone this repository to your local machine using the following command in your terminal:
    ```
    git clone github.com/Chajf/OCP_Project
    ```

3. **Navigate to the Project Directory**: Change your current directory to the project's root directory with:
    ```
    cd OCP_Project
    ```

4. **Build the Docker Images**: Build the Docker images for each container using Docker Compose with the following command:
    ```
    docker-compose build
    ```

5. **Run the Application**: Finally, you can run the application with:
    ```
    docker-compose up
    ```

## Conclusion

By integrating these containers, the application provides a comprehensive solution for analyzing sentiments on 4Chan. It not only identifies and categorizes sentiments but also presents the data in a way that can be easily understood and utilized. This makes it a valuable tool for understanding public opinion trends on 4Chan. 