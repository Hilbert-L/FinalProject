export const StarRating = ({ stars }) => {
  // Generates an array that is the length of the number of stars
  const starArray = Array.from({ length: stars });

  return (
    <div>
      {starArray.map((_, index) => (
        <span key={index}>⭐</span>
      ))}
    </div>
  );
};