"""Database models for sample sales data"""
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    """Product catalog table"""
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    
    # Relationship
    orders = relationship("Order", back_populates="product")


class Customer(Base):
    """Customer information table"""
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(255), nullable=False)
    region = Column(String(100), nullable=False)
    
    # Relationship
    orders = relationship("Order", back_populates="customer")


class Order(Base):
    """Sales order transactions table"""
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    order_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    revenue = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")
