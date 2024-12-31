'use client'

import { useState, useEffect } from 'react'
import { Search, Heart, Star, MapPin, Coffee, Wifi, Car, ChevronLeft, ChevronRight, X, Sun, Moon } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { motion, AnimatePresence } from 'framer-motion'

import hotelData from '../../../../scraper/notebooks/data/hotel_data.json'

const amenityIcons = {
  wifi: <Wifi className="h-4 w-4" />,
  parking: <Car className="h-4 w-4" />,
  coffee: <Coffee className="h-4 w-4" />,
}

interface Room {
  room_type: string;
  price: number;
  bed_configuration: string;
  cancellation_policy: string;
  board_type: string;
  special_conditions: string[];
}

interface Hotel {
  hotel_name: string;
  location: string;
  details: string;
  review_scores: {
    rating: number;
    count: number;
  };
  amenities: string[];
  rooms: Room[];
  image_url: string;
  hotel_link: string;
}

export default function HotelSearch() {
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('recommended')
  const [priceFilter, setPriceFilter] = useState('all')
  const [ratingFilter, setRatingFilter] = useState('all')
  const [currentPage, setCurrentPage] = useState(1)
  const [selectedHotel, setSelectedHotel] = useState<Hotel | null>(null)
  const [isDarkMode, setIsDarkMode] = useState(true)

  const filteredHotels = hotelData.hotels.filter((hotel: any) => {
    const isNameOrLocationMatch = hotel.hotel_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      hotel.location.toLowerCase().includes(searchQuery.toLowerCase());

    const priceMatch = priceFilter === 'all' ||
      (priceFilter === 'budget' && hotel.rooms[0].price <= 100) ||
      (priceFilter === 'mid' && hotel.rooms[0].price > 100 && hotel.rooms[0].price <= 200) ||
      (priceFilter === 'luxury' && hotel.rooms[0].price > 200);

    const ratingMatch = ratingFilter === 'all' ||
      (ratingFilter === '4plus' && hotel.review_scores.rating >= 4) ||
      (ratingFilter === '3plus' && hotel.review_scores.rating >= 3);

    return isNameOrLocationMatch && priceMatch && ratingMatch;
  })

  const sortedHotels = [...filteredHotels].sort((a, b) => {
    if (sortBy === 'price-asc') {
      return a.rooms[0].price - b.rooms[0].price
    }
    if (sortBy === 'price-desc') {
      return b.rooms[0].price - a.rooms[0].price
    }
    if (sortBy === 'rating') {
      return b.review_scores.rating - a.review_scores.rating
    }
    return 0
  })

  const hotelsPerPage = 5
  const indexOfLastHotel = currentPage * hotelsPerPage
  const indexOfFirstHotel = indexOfLastHotel - hotelsPerPage
  const currentHotels = sortedHotels.slice(indexOfFirstHotel, indexOfLastHotel)

  const totalPages = Math.ceil(sortedHotels.length / hotelsPerPage)

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber)

  useEffect(() => {
    setCurrentPage(1)
  }, [searchQuery, sortBy, priceFilter, ratingFilter])

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
    document.documentElement.classList.toggle('light')
  }

  return (
    <section className={`py-12 min-h-screen transition-colors duration-300 px-2 ${isDarkMode ? 'dark bg-gray-900' : 'bg-gray-100'}`}>
      <div className="container mx-auto px-4 relative max-w-7xl ">
        <motion.h1
          className="text-5xl font-serif mb-1 text-center tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Discover Your Dream Getaway
        </motion.h1>
        <motion.h1
          className="text-lg font-serif mb-8 text-center tracking-tight bg-clip-text text-transparent bg-primary dark:from-purple-400 dark:to-pink-400"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          We compare hotel prices from hundreds of sites
        </motion.h1>
        <motion.div
          className={`sticky top-4 z-10 rounded-3xl shadow-lg p-3 mb-8 transition-colors duration-300 ${isDarkMode ? 'bg-gray-800' : 'bg-white'}`}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex flex-col md:flex-row gap-4 items-center mb-6 ">
            <div className="relative flex-1 w-full">
              <Search className={`absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`} />
              <Input
                placeholder="Search hotels by name or location..."
                className={`pl-10 pr-4 py-3 rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 w-full ${isDarkMode
                  ? 'bg-gray-700 border-gray-600 focus:border-purple-500 focus:ring-purple-400 text-white'
                  : 'border-purple-200 focus:border-purple-400 focus:ring-purple-200'
                  }`}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <div className="flex flex-wrap gap-2 justify-center md:justify-start ">
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className={`w-[160px] rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 ${isDarkMode
                  ? 'bg-gray-700 border-gray-600 focus:border-purple-500 focus:ring-purple-400 text-white'
                  : 'border-purple-200 focus:border-purple-400 focus:ring-purple-200'
                  }`}>
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="recommended">Recommended</SelectItem>
                  <SelectItem value="price-asc">Price: Low to High</SelectItem>
                  <SelectItem value="price-desc">Price: High to Low</SelectItem>
                  <SelectItem value="rating">Rating</SelectItem>
                </SelectContent>
              </Select>
              <Select value={priceFilter} onValueChange={setPriceFilter}>
                <SelectTrigger className={`w-[160px] rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 ${isDarkMode
                  ? 'bg-gray-700 border-gray-600 focus:border-purple-500 focus:ring-purple-400 text-white'
                  : 'border-purple-200 focus:border-purple-400 focus:ring-purple-200'
                  }`}>
                  <SelectValue placeholder="Price" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Prices</SelectItem>
                  <SelectItem value="budget">Budget ($0-$100)</SelectItem>
                  <SelectItem value="mid">Mid-Range ($100-$200)</SelectItem>
                  <SelectItem value="luxury">Luxury ($200+)</SelectItem>
                </SelectContent>
              </Select>
              <Select value={ratingFilter} onValueChange={setRatingFilter}>
                <SelectTrigger className={`w-[160px] rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 ${isDarkMode
                  ? 'bg-gray-700 border-gray-600 focus:border-purple-500 focus:ring-purple-400 text-white'
                  : 'border-purple-200 focus:border-purple-400 focus:ring-purple-200'
                  }`}>
                  <SelectValue placeholder="Rating" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Ratings</SelectItem>
                  <SelectItem value="4plus">4+ Stars</SelectItem>
                  <SelectItem value="3plus">3+ Stars</SelectItem>
                </SelectContent>
              </Select>
              <Button
                variant="outline"
                size="icon"
                onClick={toggleDarkMode}
                className={`rounded-full ${isDarkMode ? 'bg-gray-700 text-yellow-400 hover:bg-gray-600' : 'bg-white text-gray-900 hover:bg-gray-100'}`}
              >
                {isDarkMode ? <Moon className="h-[1.2rem] w-[1.2rem]" /> : <Sun className="h-[1.2rem] w-[1.2rem]" />}
              </Button>
            </div>
          </div>
          <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'} text-center md:text-left`}>
            Showing {indexOfFirstHotel + 1}-{Math.min(indexOfLastHotel, sortedHotels.length)} of {sortedHotels.length} properties in {hotelData.city}
          </p>
        </motion.div>
        <AnimatePresence>
          {currentHotels.map((hotel, index) => (
            <motion.div
              key={hotel.hotel_name}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className={`mb-6 overflow-hidden transition-all hover:shadow-xl rounded-3xl max-w-4xl mx-auto ${isDarkMode ? 'bg-gray-800 text-white' : 'bg-white'}`}>
                <CardContent className="p-0">
                  <div className="flex flex-col sm:flex-row">
                    <div className="relative w-full sm:w-1/3 h-64 sm:h-auto overflow-hidden group">
                      <img
                        src={hotel.image_url}
                        alt={hotel.hotel_name}
                        className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-110"
                      />
                      <Button
                        variant="ghost"
                        size="icon"
                        className="absolute top-2 right-2 bg-white/80 backdrop-blur-sm hover:bg-white/90 rounded-full text-red-500"
                      >
                        <Heart className="h-5 w-5" />
                        <span className="sr-only">Add to favorites</span>
                      </Button>
                    </div>
                    <div className="flex-1 p-6 sm:p-2">
                      <div className="flex flex-col h-full">
                        <h3 className={`text-2xl font-semibold tracking-tight mb-2 ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>{hotel.hotel_name}</h3>
                        <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-3">
                          <MapPin className="h-4 w-4" />
                          {hotel.location}
                        </div>
                        <div className="flex items-center gap-2 mb-4">
                          <Badge variant="secondary" className={`rounded-full px-3 py-1 ${isDarkMode ? 'bg-purple-900 text-purple-200' : 'bg-purple-100 text-purple-800'}`}>
                            <Star className="h-4 w-4 mr-1 fill-yellow-400 text-yellow-400" />
                            {hotel.review_scores.rating}
                          </Badge>
                          <span className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                            {hotel.review_scores.count} reviews
                          </span>
                        </div>
                        <div className="flex gap-2 mb-4 flex-wrap">
                          {hotel.amenities.slice(0, 3).map((amenity, index) => (
                            <Badge key={index} variant="outline" className={`rounded-full px-3 py-1 ${isDarkMode ? 'border-gray-700 text-gray-300' : ''}`}>
                              {amenityIcons[amenity.toLowerCase().replace(/\s+/g, '') as keyof typeof amenityIcons] || amenity}
                            </Badge>
                          ))}
                        </div>
                        <div className="mt-auto flex items-center justify-between">
                          <div>
                            <div className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Starting from</div>
                            <div className={`text-2xl font-bold ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>${hotel.rooms[0].price.toFixed(2)}</div>
                            <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>per night</div>
                          </div>
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button
                                className="rounded-full px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600 transition-all duration-300"
                                onClick={() => setSelectedHotel(hotel as Hotel)}
                              >
                                See Rooms
                              </Button>
                            </DialogTrigger>
                            <DialogContent className={`max-w-3xl ${isDarkMode ? 'bg-gray-800 text-white' : 'bg-white'}`}>
                              <DialogHeader>
                                <DialogTitle className={`text-2xl font-bold ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>{selectedHotel?.hotel_name}</DialogTitle>
                                <DialogDescription className={isDarkMode ? 'text-gray-400' : 'text-gray-600'}>{selectedHotel?.details}</DialogDescription>
                              </DialogHeader>
                              <div className="grid gap-4">
                                <div className="grid grid-cols-2 items-center gap-4">
                                  <img
                                    src={selectedHotel?.image_url}
                                    alt={selectedHotel?.hotel_name}
                                    className="w-full h-auto rounded-lg"
                                  />
                                  <div>
                                    <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'} mb-2`}>{selectedHotel?.location}</p>
                                    <div className="flex items-center gap-2 mb-2">
                                      <Badge variant="secondary" className={`rounded-full px-3 py-1 ${isDarkMode ? 'bg-purple-900 text-purple-200' : 'bg-purple-100 text-purple-800'}`}>
                                        <Star className="h-4 w-4 mr-1 fill-yellow-400 text-yellow-400" />
                                        {selectedHotel?.review_scores.rating}
                                      </Badge>
                                      <span className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                                        {selectedHotel?.review_scores.count} reviews
                                      </span>
                                    </div>
                                    <div className="flex flex-wrap gap-2">
                                      {selectedHotel?.amenities.map((amenity, index) => (
                                        <Badge key={index} variant="outline" className={`rounded-full px-3 py-1 ${isDarkMode ? 'border-gray-700 text-gray-300' : ''}`}>{amenity}</Badge>
                                      ))}
                                    </div>
                                  </div>
                                </div>
                                <h4 className={`text-lg font-semibold ${isDarkMode ? 'text-purple-400' : 'text-purple-800'} mt-4`}>Available Rooms</h4>
                                <ScrollArea className={`h-[300px] rounded-md border p-4 ${isDarkMode ? 'border-gray-700' : ''}`}>
                                  {selectedHotel?.rooms.map((room, index) => (
                                    <div key={index} className={`mb-6 p-4 border rounded-lg ${isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50'}`}>
                                      <div className="flex justify-between items-start mb-2">
                                        <h5 className={`font-semibold ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>{room.room_type}</h5>
                                        <div className="text-right">
                                          <div className={`text-lg font-bold ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>${room.price.toFixed(2)}</div>
                                          <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>per night</div>
                                        </div>
                                      </div>
                                      <p className={`text-sm mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>{room.bed_configuration}</p>
                                      <p className={`text-sm mb-2 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>{room.board_type}</p>
                                      <p className="text-xs text-green-600">{room.cancellation_policy}</p>
                                      {room.special_conditions.length > 0 && (
                                        <div className="mt-2">
                                          <h6 className={`text-xs font-medium mb-1 ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>Special Conditions:</h6>
                                          <ul className={`list-disc list-inside text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                                            {room.special_conditions.map((condition, idx) => (
                                              <li key={idx}>{condition}</li>
                                            ))}
                                          </ul>
                                        </div>
                                      )}
                                      <Button className="mt-4 w-full rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600 transition-all duration-300">
                                        Book Now
                                      </Button>
                                    </div>
                                  ))}
                                </ScrollArea>
                              </div>
                            </DialogContent>
                          </Dialog>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </AnimatePresence>
        {totalPages > 1 && (
          <div className="flex justify-center mt-8">
            <Button
              variant="outline"
              size="icon"
              onClick={() => paginate(currentPage - 1)}
              disabled={currentPage === 1}
              className={`rounded-full mr-2 ${isDarkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : ''}`}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((number) => (
              <Button
                key={number}
                variant={currentPage === number ? "default" : "outline"}
                className={`mx-1 rounded-full ${isDarkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : ''}`}
                onClick={() => paginate(number)}
              >
                {number}
              </Button>
            ))}
            <Button
              variant="outline"
              size="icon"
              onClick={() => paginate(currentPage + 1)}
              disabled={currentPage === totalPages}
              className={`rounded-full ml-2 ${isDarkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : ''}`}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </section>
  )
}

