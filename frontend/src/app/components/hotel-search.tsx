'use client'

import { useState, useEffect } from 'react'
import { Search, Heart, Star, MapPin, Coffee, Wifi, Car, Check, Link, ChevronLeft, ChevronRight } from 'lucide-react'
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
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"

// Read data from json file
const HOTELS = require('../../../../data/hotel_data.json');

const amenityIcons = {
  wifi: <Wifi className="h-4 w-4" />,
  parking: <Car className="h-4 w-4" />,
  coffee: <Coffee className="h-4 w-4" />,
}

export default function HotelSearch() {
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('recommended')
  const [priceFilter, setPriceFilter] = useState('all')
  const [ratingFilter, setRatingFilter] = useState('all')
  const [currentPage, setCurrentPage] = useState(1)
  const [hotelsPerPage] = useState(9)

  // Filter hotels based on the search query, price, and rating
  const filteredHotels = HOTELS.filter((hotel: { name: string; location: string; price: string; rating: string; image_url: string; amenities: string; hotel_link: string }) => {
    const isNameOrLocationMatch = hotel.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      hotel.location.toLowerCase().includes(searchQuery.toLowerCase());

    // Price Filter
    const priceMatch = priceFilter === 'all' ||
      (priceFilter === 'budget' && parseInt(hotel.price.replace('$', '')) <= 100) ||
      (priceFilter === 'mid' && parseInt(hotel.price.replace('$', '')) > 100 && parseInt(hotel.price.replace('$', '')) <= 200) ||
      (priceFilter === 'luxury' && parseInt(hotel.price.replace('$', '')) > 200);

    // Rating Filter
    const ratingMatch = ratingFilter === 'all' ||
      (ratingFilter === '4plus' && parseFloat(hotel.rating.split('\n')[2]) >= 4) ||
      (ratingFilter === '3plus' && parseFloat(hotel.rating.split('\n')[2]) >= 3);

    return isNameOrLocationMatch && priceMatch && ratingMatch;
  })

  const sortedHotels = [...filteredHotels].sort((a, b) => {
    if (sortBy === 'price-asc') {
      return parseInt(a.price.replace('$', '')) - parseInt(b.price.replace('$', ''))
    }
    if (sortBy === 'price-desc') {
      return parseInt(b.price.replace('$', '')) - parseInt(a.price.replace('$', ''))
    }
    if (sortBy === 'rating') {
      return parseFloat(b.rating.split('\n')[2]) - parseFloat(a.rating.split('\n')[2])
    }

    return 0
  })

  const indexOfLastHotel = currentPage * hotelsPerPage
  const indexOfFirstHotel = indexOfLastHotel - hotelsPerPage
  const currentHotels = sortedHotels.slice(indexOfFirstHotel, indexOfLastHotel)

  const totalPages = Math.ceil(sortedHotels.length / hotelsPerPage)

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber)

  useEffect(() => {
    setCurrentPage(1)
  }, [searchQuery, sortBy, priceFilter, ratingFilter])

  return (
    <section className="py-12 bg-gray-50 ">
      <div className="container mx-auto px-4 relative">
        <div className='flex items-center justify-center'><h2 className="text-3xl font-bold mb-8">Find Your Perfect Hotel</h2></div>
        <div className="bg-white rounded-lg shadow-md p-2 sticky top-4 z-10">
          <div className="flex flex-col gap-4 md:flex-row md:items-center mb-6 ">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search hotels by name or location..."
                className="pl-8 bg-background transition-colors focus-visible:ring-2"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <div className="flex flex-wrap gap-2 ">
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-[160px] bg-background">
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
                <SelectTrigger className="w-[160px] bg-background">
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
                <SelectTrigger className="w-[160px] bg-background">
                  <SelectValue placeholder="Rating" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Ratings</SelectItem>
                  <SelectItem value="4plus">4+ Stars</SelectItem>
                  <SelectItem value="3plus">3+ Stars</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex items-center justify-between mb-4 ">
            <p className="text-sm text-muted-foreground">
              Showing {indexOfFirstHotel + 1}-{Math.min(indexOfLastHotel, sortedHotels.length)} of {sortedHotels.length} properties in Manhattan
            </p>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  {/* <Button variant="outline" size="sm">
                    <MapPin className="h-4 w-4 mr-2" />
                    View Map
                  </Button> */}
                </TooltipTrigger>
                <TooltipContent>
                  <p>Open map view</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </div>
        <div className="mt-6 space-y-4 px-12 flex flex-col items-center justify-center">
          {currentHotels.map((hotel, index) => (
            <Card key={index} className="w-[calc(100%-1rem)] max-w-5xl overflow-hidden transition-all hover:shadow-lg">
            <CardContent className="p-0">
              <div className="flex flex-col sm:flex-row">
                <div className="relative w-full sm:w-64 sm:h-full overflow-hidden group bg-rose-200">
                  <img
                    src={hotel.image_url}
                    alt={hotel.name}
                    className="object-cover w-full h-full transition-transform group-hover:scale-105"
                  />
                  <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-2 right-2 bg-background/80 backdrop-blur-sm hover:bg-background/90"
                  >
                    <Heart className="h-4 w-4" />
                    <span className="sr-only">Add to favorites</span>
                  </Button>
                </div>
                <div className="flex-1 p-4">
                  <div className="flex flex-col h-full">
                    <div>
                      <h3 className="text-lg font-semibold tracking-tight mb-1">{hotel.name}</h3>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                        <MapPin className="h-4 w-4" />
                        {hotel.location}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="secondary" className="rounded-md">
                        <Star className="h-3 w-3 mr-1 fill-primary text-primary" />
                        {hotel.rating.split('\n')[2]}
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        {hotel.rating.split('\n')[1]}
                      </span>
                      <Badge className="rounded-md bg-green-500 text-xs">
                        {hotel.rating.split('\n')[0]}
                      </Badge>
                    </div>
                    <div className="flex gap-2 mb-2">
                      {Object.entries(amenityIcons).map(([key, icon]) => (
                        <TooltipProvider key={key}>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <div className="p-1 rounded-full bg-muted">
                                {icon}
                              </div>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p className="capitalize">{key}</p>
                            </TooltipContent>
                          </Tooltip>
                        </TooltipProvider>
                      ))}
                    </div>
                    {hotel.amenities !== "N/A" && (
                      <div className="mt-auto">
                        <div className="flex items-center gap-2 text-xs text-green-600">
                          <Check className="h-3 w-3" />
                          {hotel.amenities}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <Separator orientation="vertical" className="hidden sm:block" />
                <div className="p-4 sm:w-64 flex flex-row sm:flex-col justify-between items-stretch sm:border-l">
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground mb-1">Starting from</div>
                    <div className="text-2xl font-bold">{hotel.price}</div>
                    <div className="text-xs text-muted-foreground">per night</div>
                  </div>
                  <Button className="mt-2 w-full bg-gradient-to-r from-blue-500 to-violet-500 " size="lg">
                    <a href={hotel.hotel_link}>
                      See availability
                    </a>
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
          
          ))}
        </div>
        {totalPages > 1 && (
          <div className="flex justify-center mt-6">
            <Button
              variant="outline"
              size="icon"
              onClick={() => paginate(currentPage - 1)}
              disabled={currentPage === 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((number) => (
              <Button
                key={number}
                variant={currentPage === number ? "default" : "outline"}
                className="mx-1 "
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
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </section>
  )
}

