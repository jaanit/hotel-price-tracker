# Hotel Price Tracker

## Overview
This project demonstrates a hotel price tracking system using two main components:

1. **Scraper**: Collects hotel data from Kayak and stores it locally.
2. **Frontend**: A Next.js application to display the scraped data in a user-friendly interface.

## Features
- Scrape hotel data (name, location, reviews, amenities, prices, and more).
- Paginate and extract detailed information for each hotel.
- Display results in a clean and functional UI.
- Filter hotels based on price and star ratings.

---

## Prerequisites
Ensure the following are installed on your machine:
- **Docker** and **Docker Compose**
- **Node.js** (v18 or higher) and **npm**



---

## Setup Instructions

### 1. Hotel Search Scraper
The scraper runs inside a Docker container and scrapes data from Kayak.

#### Steps:
1. Build and run the scraper:
   ```bash
   docker-compose up --build
   ```
   This starts the backend services and opens Jupyter Notebook at [http://localhost:8888](http://localhost:8888).

2. Open `scraper/notebooks/scraper_test.ipynb` in the Jupyter Notebook interface.
3. Run the cells in the notebook to execute the scraping process. The scraped data will be saved in `scraper/notebooks/data/hotel_data.json`.

---

### 2. Frontend (Next.js Application)
The frontend displays the scraped hotel data.

#### Steps:
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to view the application.

---

## Project Structure
```
.
├── scraper       # Contains scraping scripts and Jupyter notebooks
├── frontend      # Contains the Next.js application
├── docker-compose.yml
└── README.md
```

---

## Contact
For questions or suggestions, feel free to reach out

