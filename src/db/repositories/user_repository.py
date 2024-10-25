from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.db.models import User, Role
from src.schemas.user import UserCreate, UserInDB, UserInfo
from typing import Optional, List


class UserRepository:
    """
    Repository for managing user-related database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserInDB:
        """
        Add a new user to the database and return the UserInDB model.

        Automatically handles created_at and updated_at using SQLAlchemy's
        server-side default values.
        User can choose specific user role like "admin", "manager", "customer"

        User's email must be unique.

        """
        db_user = User(
            name=user.name,
            surname=user.surname,
            email=user.email,
            role=user.role  # Role should be passed correctly if provided
            # orders relationship will not be handled here since Order is not ready yet
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserInDB.from_orm(db_user)

    def get_user_by_id(self, user_id: int) -> Optional[UserInDB]:
        """
        Retrieve a user by their ID from the database.
        """
        try:
            db_user = self.db.query(User).filter(User.id == user_id).one()
            return UserInDB.from_orm(db_user)
        except NoResultFound:
            return None

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Retrieve a user by their email from the database.
        """
        try:
            db_user = self.db.query(User).filter(User.email == email).one()
            return UserInDB.from_orm(db_user)
        except NoResultFound:
            return None

    def get_users_by_role(self, user_role: Role) -> Optional[List[UserInDB]]:
        """
        Retrieve all users from the database with a specific role (admin, manager, customer).

        Returns a list of UserInDB schemas.
        """
        db_users = self.db.query(User).filter(User.role == user_role).all()
        result = [UserInDB.from_orm(user) for user in db_users]
        if len(result) == 0:
            return None
        return result

    def get_all_users(self) -> Optional[List[UserInDB]]:
        """
        Retrieve all users from the database.

        Returns a list of UserInDB schemas.
        """
        db_users = self.db.query(User).all()
        all_orders = [UserInDB.from_orm(user) for user in db_users]
        if len(all_orders) == 0:
            return None
        return all_orders

    def delete_user_by_id(self, user_id: int) -> Optional[int]:
        """
        Delete a user from the database by their ID.

        Returns the ID of the deleted user if successful, otherwise None.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return user_id
        return None

    #
    def update_user_by_id(self, user_id: int, user_data: UserInfo) -> Optional[UserInDB]:
        """
        Partially update a user's information by their ID.

        Returns the updated UserInDB schema if the user is found and updated, otherwise None.
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()

        if not db_user:
            return None

        # Update only the fields that were provided (non-default fields)
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return UserInDB.from_orm(db_user)
