
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { MapPin, Star, Heart } from 'lucide-react';
import { motion } from 'framer-motion';

export default function HotelCard({ hotel, isDarkMode, onSelect }: { hotel: any, isDarkMode: boolean, onSelect: any }) {
  return (
    <motion.div
    className={`mb-6 overflow-hidden transition-all hover:shadow-xl rounded-3xl max-w-4xl mx-auto ${isDarkMode ? 'bg-gray-800 text-white' : 'bg-white'}`}
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -50 }}
    transition={{ duration: 0.5 }}
  >
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
      <div className="flex-1 p-6 sm:p-8">
        <h3 className={`text-2xl font-semibold tracking-tight mb-2 ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>{hotel.hotel_name}</h3>
        <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-3">
          <MapPin className="h-4 w-4" />
          {hotel.location}
        </div>
        <Badge variant="secondary" className={`rounded-full px-3 py-1 ${isDarkMode ? 'bg-purple-900 text-purple-200' : 'bg-purple-100 text-purple-800'}`}>
          <Star className="h-4 w-4 mr-1 fill-yellow-400 text-yellow-400" />
          {hotel.review_scores.rating}
        </Badge>
        <div className={`mt-auto text-2xl font-bold ${isDarkMode ? 'text-purple-400' : 'text-purple-800'}`}>${hotel.rooms[0].price.toFixed(2)}</div>
        <Button onClick={() => onSelect(hotel)}>See Rooms</Button>
      </div>
    </div>
  </motion.div>
  );
}