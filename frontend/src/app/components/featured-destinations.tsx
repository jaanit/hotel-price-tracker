import { Card, CardContent } from "@/components/ui/card"

const destinations = [
  { name: "Paris", image: "/placeholder.svg?height=200&width=300", description: "The City of Light" },
  { name: "Tokyo", image: "/placeholder.svg?height=200&width=300", description: "Where tradition meets future" },
  { name: "New York", image: "/placeholder.svg?height=200&width=300", description: "The Big Apple" },
  { name: "Rome", image: "/placeholder.svg?height=200&width=300", description: "Eternal City" },
]

export default function FeaturedDestinations() {
  return (
    <section className="py-12">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8">Featured Destinations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {destinations.map((destination) => (
            <Card key={destination.name} className="overflow-hidden">
              <img src={destination.image} alt={destination.name} className="w-full h-48 object-cover" />
              <CardContent className="p-4">
                <h3 className="font-semibold text-lg mb-2">{destination.name}</h3>
                <p className="text-muted-foreground">{destination.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

