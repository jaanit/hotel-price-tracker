import { Search, Sun, Moon } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';

export default function FilterControls({
    searchQuery,
    setSearchQuery,
    sortBy,
    setSortBy,
    priceFilter,
    setPriceFilter,
    ratingFilter,
    setRatingFilter,
    toggleDarkMode,
    isDarkMode,
}: {
    searchQuery: string,
    setSearchQuery: (query: string) => void,
    sortBy: string,
    setSortBy: (sortBy: string) => void,
    priceFilter: string,
    setPriceFilter: (priceFilter: string) => void,
    ratingFilter: string,
    setRatingFilter: (ratingFilter: string) => void,
    toggleDarkMode: () => void,
    isDarkMode: boolean,
}) {
  return (
    <motion.div 
    className={`rounded-3xl shadow-lg p-6 mb-8 transition-colors duration-300 ${isDarkMode ? 'bg-gray-800' : 'bg-white'}`}
    initial={{ opacity: 0, scale: 0.9 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.5 }}
  >
    <div className="flex flex-col md:flex-row gap-4 items-center mb-6">
      <div className="relative flex-1 w-full">
        <Search className={`absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`} />
        <Input
          placeholder="Search hotels by name or location..."
          className={`pl-10 pr-4 py-3 rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 w-full ${
            isDarkMode
              ? 'bg-gray-700 border-gray-600 focus:border-purple-500 focus:ring-purple-400 text-white'
              : 'border-purple-200 focus:border-purple-400 focus:ring-purple-200'
          }`}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>
      <div className="flex flex-wrap gap-2 justify-center md:justify-start">
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className={`w-[160px] rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 ${
            isDarkMode
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
          <SelectTrigger className={`w-[160px] rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 ${
            isDarkMode
              ? 'bg-gray-700 border-gray-600 focus:border-purple-500 focus:ring-purple-400 text-white'
              : 'border-purple-200 focus:border-purple-400 focus:ring-purple-200'
          }`}>
            <SelectValue placeholder="Price" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Prices</SelectItem>
            <SelectItem value="budget">Budget ($0-$100)</SelectItem>
            <SelectItem value="mid">Mid-Range ($100-$200)</SelectItem>
            <SelectItem value="luxury">Luxury ($200+) </SelectItem>
          </SelectContent>
        </Select>
        <Select value={ratingFilter} onValueChange={setRatingFilter}>
          <SelectTrigger className={`w-[160px] rounded-full border-2 focus:ring focus:ring-opacity-50 transition-all duration-300 ${
            isDarkMode
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
          {isDarkMode ? <Sun className="h-[1.2rem] w-[1.2rem]" /> : <Moon className="h-[1.2rem] w-[1.2rem]" />}
        </Button>
      </div>
    </div>
  </motion.div>
  );
}