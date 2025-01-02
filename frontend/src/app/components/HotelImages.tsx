'use client';

import * as React from 'react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';
import { Card, CardContent } from '@/components/ui/card';
import Image from 'next/image';

interface Image {
  url: string;
  alt: string;
}

export default function HotelImages({ images }: { images: Image[] }) {

  if (!images || images.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-col rounded-md">
      <Carousel
        className="relative rounded-md overflow-hidden"
      >
        <CarouselContent>
          {images.map((image, index) => {
            return (
              <CarouselItem key={index}>
                <Card className="border-0 mr-2">
                  <CardContent className="flex rounded-md items-center justify-center p-0">
                    <Image
                      src={image.url}
                      alt={image.alt}
                      width={1020}
                      height={1020}
                      className="object-cover w-full h-full rounded-lg"
                      loading={index === 0 ? "eager" : "lazy"}
                    />
                  </CardContent>
                </Card>
              </CarouselItem>
            );
          })}
        </CarouselContent>
        <CarouselPrevious className="left-4" />
        <CarouselNext className="right-4" />
      </Carousel>
    </div>
  );
}
