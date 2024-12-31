import Header from './components/header'
import Footer from './components/footer'
import HotelSearch from './components/hotel-search'
import FeaturedDestinations from './components/featured-destinations'
import Newsletter from './components/newsletter'

export default function Page() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* <Header /> */}
      <main className="flex-grow">
        {/* <HeroSection /> */}
        <HotelSearch />
        {/* <FeaturedDestinations /> */}
        {/* <Newsletter /> */}
      </main>
      {/* <Footer /> */}
    </div>
  )
}

function HeroSection() {
  return (
    <section className="relative bg-gradient-to-r from-blue-600 to-blue-400 text-white py-20">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Find Your Perfect Stay</h1>
        <p className="text-xl mb-8">Discover amazing hotels at unbeatable prices</p>
      </div>
    </section>
  )
}

