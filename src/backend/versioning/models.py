from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProductData(Base):
    __tablename__ = 'product_data'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    # Add other product data columns as needed
    version = Column(Integer, default=1)  # Version number for tracking changes
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def increment_version(self):
        self.version += 1

    def __repr__(self):
        return f"<ProductData(id={self.id}, name='{self.name}', version={self.version})>"


class VersionHistory(Base):
    __tablename__ = 'version_history'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    version = Column(Integer)
    change_description = Column(String)
    changed_at = Column(DateTime, default=func.now())
    # You can add columns to store the actual data changes if needed (e.g., JSON)

    def __repr__(self):
        return f"<VersionHistory(id={self.id}, product_id={self.product_id}, version={self.version})>"