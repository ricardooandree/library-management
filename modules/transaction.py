###################################################################################################
#######################################       IMPORTS       #######################################
###################################################################################################
import datetime

from sqlalchemy import Column, Float, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from modules.user import Base

###################################################################################################
#######################################       CLASSES       #######################################
###################################################################################################
class Transaction(Base):
    __tablename__ = 'transactions'
    _id = Column(Integer, primary_key=True)
    _user_id = Column(Integer, ForeignKey('users._id'))
    _book_id = Column(Integer, ForeignKey('books._id'))
    _type = Column(String)  # Type of transaction: Rental/Return
    _checkout_date = Column(Date)
    _return_date = Column(Date)
    _fee = Column(Float)
    _status = Column(Boolean) # Status of rental transaction: Paid/Non-paid
    
    # Define relationships
    user = relationship("User", back_populates="transactions")
    book = relationship("Book", back_populates="transactions")
    
    # Define setter methods for attributes
    def set_user_id(self, user_id):
        # User id attribute validation
        if not isinstance(user_id, int):
            raise ValueError("User id must be an integer")

        # Set user id attribute            
        self._user_id = user_id
    
    def set_book_id(self, book_id):
        # Book id attribute validation
        if not isinstance(book_id, int):
            raise ValueError("Book id must be an integer")
        
        # Set book id attribute
        self._book_id = book_id
        
    def set_type(self, type):
        # Type attribute validation
        if not isinstance(type, str):
            raise ValueError("Type must be a string")
        
        if type not in ['Rental', 'Return', 'Early Return', 'Late Return']:
            raise ValueError("Type is not supported")
            
        # Set type attribute
        self._type = type
        
    def set_checkout_date(self, checkout_date):
        # Checkout date attribute validation
        if not isinstance(checkout_date, datetime.date):
            raise ValueError("Checkout date must be a date object (yyyy-mm-dd)")
        
        # Set checkout date attribute
        self._checkout_date = checkout_date
        
    def set_return_date(self, return_date):
        # Return date attribute validation
        if not isinstance(return_date, datetime.date):
            raise ValueError("Return date must be a date object (yyyy-mm-dd)")
        
        # Set return date attribute
        self._return_date = return_date
        
    def set_fee(self, fee):
        # Fee attribute validation
        if not isinstance(fee, float):
            raise ValueError("Fee must be a float")
        
        if fee < 0:
            raise ValueError("Fee must be a positive float")
        
        # Set fee attribute
        self._fee = fee
    
    def set_status(self, active):
        # Status attribute validation
        if not isinstance(active, bool):
            raise ValueError("Status must be a boolean")
        
        # Set status attribute
        self._status = active
        
    # Define getter methods for attributes
    def get_type(self):
        return self._type
    
    def get_checkout_date(self):
        return self._checkout_date
    
    def get_return_date(self):
        return self._return_date
    
    def get_fee(self):
        return self._fee
    
    def get_status(self):
        return self._status
    
    def display(self):
        ...

    @classmethod
    def authenticate_user_book(cls, session, user_id, book_id, type=None):
        """Authenticates a specific user rental transactions
        """
        # Query the database to find a transaction with the specified book and user
        transactions = session.query(Transaction).filter(Transaction._user_id == user_id, Transaction._book_id == book_id, Transaction._type == type).all()

        # Check if transaction exists in the database
        if transactions: 
            return transactions
        else:
            return None
    
    @classmethod
    def register(cls, session, user_id, book_id, checkout_date, return_date, fee, status, type):
        """Register new transaction
        """
        # Create a new Transaction object
        new_transaction = Transaction()
        
        # Check if new_user was created successfully
        if new_transaction:
            # Set new transaction attributes
            new_transaction.set_user_id(user_id)
            new_transaction.set_book_id(book_id)
            new_transaction.set_type(type)
            new_transaction.set_checkout_date(checkout_date)
            new_transaction.set_return_date(return_date)
            new_transaction.set_fee(fee)
            new_transaction.set_status(status)
            
            # Add new transaction to the database
            session.add(new_transaction)
            session.commit()
            
            return True    # Registration successful
        else:
            return False    # Registration failed
        
        