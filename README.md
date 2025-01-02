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

   ```json
   {
     "city": "Paris, France",
     "hotels": [
       {
         "hotel_name": "Lovely 1 bedroom apartment with indoor fireplace",
         "detail_url": "https://www.kayak.com/hotels/Lovely-1-bedroom-apartment-with-indoor-fireplace,Paris-p37687-h1070546032-details/2025-01-10/2025-01-14/2adults?psid=efEkT3BMXE&pm=daybase#overview",
         "location": "0.0 mi from Paris, France",
         "review_scores": {
           "rating": null,
           "count": null
         },
         "price": "$300",
         "images": [
           {
             "url": "https://content.r9cdn.net/rimg/himg/7a/31/44/expediav2-1070546032-3487064204-478543.jpg?width=1020&height=1020&xhint=540&yhint=333&crop=true&watermarkheight=28&watermarkpadding=10",
             "alt": "Bedroom view of Lovely 1 bedroom apartment with indoor fireplace",
             "type": "detail"
           },
           {
             "url": "https://content.r9cdn.net/rimg/himg/f9/8e/63/expedia_group-1070546032-16014380-858619.jpg?width=1020&height=1020&xhint=540&yhint=333&crop=true&watermarkheight=28&watermarkpadding=10",
             "alt": "Other view of Lovely 1 bedroom apartment with indoor fireplace",
             "type": "detail"
           }
         ],
         "rooms": [
           {
             "room_type": "All deals",
             "price": 300.0,
             "bed_configuration": null,
             "cancellation_policy": null,
             "board_type": null,
             "special_conditions": []
           }
         ],
         "amenities": [
           "Air-conditioned",
           "Fireplace",
           "Coffee grinder",
           "Kettle",
           "Blender",
           "Dishwasher",
           "Ice maker",
           "Free Wi-Fi",
           "Heating"
         ]
       }
     ],
     "pagination": {
       "current_page": 1,
       "total_pages": 1
     },
     "metadata": {
       "scraping_date": "2025-01-02",
       "scraping_time": "20:42",
       "source_url": "https://www.kayak.com/hotels"
     }
   }
   ```
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

