from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import logging

Base = declarative_base()

class ProductMatching(Base):
    """
    Represents a matching between two products and stores the confidence score.
    """
    __tablename__ = 'ProductMatching'

    id = Column(Integer, primary_key=True)
    product_id1 = Column(Integer, nullable=False)  # ID of the first product
    product_id2 = Column(Integer, nullable=False)  # ID of the second product
    confidence_score = Column(Float, nullable=False)  # Confidence score of the match
    match_timestamp = Column(DateTime, nullable=False)  # Timestamp of when the match was made
    matched_by_algorithm = Column(String, nullable=True) # Algorithm used for matching
    
    def __init__(self, product_id1, product_id2, confidence_score, match_timestamp, matched_by_algorithm="default"):
        self.product_id1 = product_id1
        self.product_id2 = product_id2
        self.confidence_score = confidence_score
        self.match_timestamp = match_timestamp
        self.matched_by_algorithm = matched_by_algorithm

    def __repr__(self):
        return f"<ProductMatching(id={self.id}, product_id1={self.product_id1}, product_id2={self.product_id2}, confidence_score={self.confidence_score:.2f})>"

    @classmethod
    def create_match(cls, product_id1, product_id2, confidence_score, match_timestamp, matched_by_algorithm="default"):
        """
        Creates a new ProductMatching instance.

        Args:
            product_id1 (int): ID of the first product.
            product_id2 (int): ID of the second product.
            confidence_score (float): Confidence score of the match.
            match_timestamp (datetime): Timestamp of the match.
            matched_by_algorithm (str, optional): Algorithm used for the match. Defaults to "default".

        Returns:
            ProductMatching: The created ProductMatching instance.
        """
        if confidence_score < 0.7:  # Confidence threshold to minimize false positives.  Adjust as needed.
            logging.warning(f"Low confidence score ({confidence_score:.2f}) for match between {product_id1} and {product_id2}.  Match not created.")
            return None

        try:
            match = cls(product_id1, product_id2, confidence_score, match_timestamp, matched_by_algorithm)
            return match
        except Exception as e:
            logging.error(f"Error creating product match: {e}")
            return None
        
        
# Example Usage (for testing/demonstration - not part of the core model)
if __name__ == '__main__':
    from datetime import datetime
    
    # Create a dummy match
    match = ProductMatching.create_match(123, 456, 0.85, datetime.now(), "AlgorithmX")
    if match:
        print(match)
        
    match = ProductMatching.create_match(789, 101, 0.5, datetime.now()) # Test low confidence
    if match is None:
        print("Low confidence match was not created")