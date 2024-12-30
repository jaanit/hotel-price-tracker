"use client"
import Header from './components/header'
import Footer from './components/footer'
import HotelSearch from './components/hotel-search'
import FeaturedDestinations from './components/featured-destinations'
import Newsletter from './components/newsletter'
import { useState } from 'react'

export default function Page() {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow">
        {/* <HeroSection /> */}
        <HotelSearch />

      </main>

    </div>
  )
}

function HeroSection() {


  return (
    <section
      className="relative h-[300px] text-white flex items-center justify-center"
      style={{
        backgroundColor: 'bg-gradient-to-r from-blue-500 to-violet-500',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <div className="absolute inset-0 bg-black bg-opacity-50"></div>
      <div className="relative z-10 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Find Your Perfect Stay</h1>
        <p className="text-xl mb-8">Discover amazing hotels at unbeatable prices</p>
      </div>
    </section>
  );
}

