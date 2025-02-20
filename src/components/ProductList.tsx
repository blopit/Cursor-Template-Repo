import React, { type FC, type KeyboardEvent } from 'react';

interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
}

interface ProductListProps {
  products: Product[];
  onProductSelect?: (product: Product) => void;
}

export const ProductList: FC<ProductListProps> = ({ 
  products, 
  onProductSelect 
}) => {
  const handleKeyPress = (event: KeyboardEvent<HTMLButtonElement>, product: Product) => {
    if (event.key === 'Enter' || event.key === ' ') {
      onProductSelect?.(product);
    }
  };

  return (
    <ul className="product-list">
      {products.map((product) => (
        <li key={product.id} className="product-item">
          <button
            type="button"
            className="product-button"
            onClick={() => onProductSelect?.(product)}
            onKeyPress={(e) => handleKeyPress(e, product)}
          >
            <h3>{product.name}</h3>
            {product.description && <p>{product.description}</p>}
            <p className="price">
              ${product.price.toFixed(2)}
            </p>
          </button>
        </li>
      ))}
    </ul>
  );
}; 