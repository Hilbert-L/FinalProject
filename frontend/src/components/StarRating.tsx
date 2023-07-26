import React from 'react';

interface StarRatingProps {
  stars: number;
}

export const StarRating = ({ stars }) => {
  // Generate an array with the length of the number of stars
  const starArray = Array.from({ length: stars });

  return (
    <div>
      {starArray.map((_, index) => (
        <span key={index} role="img" aria-label="star">⭐</span>
      ))}
    </div>
  );
};