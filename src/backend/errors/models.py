from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ValidationResults(Base):
    __tablename__ = 'validation_results'

    id = Column(Integer, primary_key=True)
    error_message = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # Add any other relevant fields, e.g., user_id, component, etc.

    def __repr__(self):
        return f"<ValidationResult(id={self.id}, message='{self.error_message}', timestamp='{self.timestamp}')>"

# Example database setup (replace with your actual configuration)
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///:memory:') # or your preferred database URL
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

if __name__ == '__main__':
    # Example usage (for testing)
    # from sqlalchemy import create_engine
    # engine = create_engine('sqlite:///:memory:')
    # Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # result = ValidationResults(error_message="Test error message")
    # session.add(result)
    # session.commit()

    # retrieved_result = session.query(ValidationResults).first()
    # print(retrieved_result)
    pass