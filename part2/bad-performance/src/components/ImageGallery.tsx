import React from "react";

const largeImageUrls = [
  "https://images.unsplash.com/photo-1471879832106-c7ab9e0cee23?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1501854140801-50d01698950b?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1504198322253-cfa87a0ff25f?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
  "https://images.unsplash.com/photo-1426604966848-d7adac402bff?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=3000",
];

const images = [...largeImageUrls, ...largeImageUrls, ...largeImageUrls].map(
  (url, index) => ({
    id: index,
    url,
    title: `Image ${index}`,
    description: `This is the description for image ${index}.`,
  })
);

const ImageGallery = () => {
  return (
    <div className="image-gallery">
      <h2>Image Gallery</h2>
      <div className="gallery-grid">
        {images.map((image) => (
          <div key={image.id} className="gallery-item">
            <img src={image.url} alt={image.title} style={{ opacity: 1 }} />
            <div className="image-info">
              <h3>{image.title}</h3>
              <p>{image.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageGallery;
