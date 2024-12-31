import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Pagination({ currentPage, totalPages, onPageChange, isDarkMode }: { currentPage: number, totalPages: number, onPageChange: (page: number) => void, isDarkMode: boolean }) {
  return (
    <motion.div
    className="flex justify-center mt-8"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.5 }}
  >
    <Button
      variant="outline"
      size="icon"
      onClick={() => onPageChange(currentPage - 1)}
      disabled={currentPage === 1}
      className={`rounded-full mr-2 ${isDarkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : ''}`}
    >
      <ChevronLeft className="h-4 w-4" />
    </Button>
    {Array.from({ length: totalPages }, (_, i) => i + 1).map((number) => (
      <Button
        key={number}
        variant={currentPage === number ? 'default' : 'outline'}
        className={`mx-1 rounded-full ${isDarkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : ''}`}
        onClick={() => onPageChange(number)}
      >
        {number}
      </Button>
    ))}
    <Button
      variant="outline"
      size="icon"
      onClick={() => onPageChange(currentPage + 1)}
      disabled={currentPage === totalPages}
      className={`rounded-full ml-2 ${isDarkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : ''}`}
    >
      <ChevronRight className="h-4 w-4" />
    </Button>
  </motion.div>
  );
}
