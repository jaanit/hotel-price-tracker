import HotelSearch from './components/hotel-search'

export default function Page() {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow">
        <HotelSearch />
      </main>
    </div>
  )
}

