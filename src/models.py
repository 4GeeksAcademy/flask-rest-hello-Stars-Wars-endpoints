from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
    String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    firts_name: Mapped[str] = mapped_column(String(), nullable=False)
    second_name: Mapped[str] = mapped_column(String(), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    population: Mapped[str] = mapped_column(String(50))

    residents: Mapped[list["People"]] = relationship(
        "People", back_populates="homeworld")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population

        }


class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100))
    pilot_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)

    pilot: Mapped["People"] = relationship(
        "People", back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "pilot_id": self.pilot_id
        }


class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    height: Mapped[str] = mapped_column(String(10))
    mass: Mapped[str] = mapped_column(String(10))
    birth_year: Mapped[str] = mapped_column(String(20))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicles: Mapped[list["Vehicle"]] = relationship("Vehicle", back_populates="pilot")

    homeworld: Mapped["Planet"] = relationship("Planet", back_populates="residents")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "birth_year": self.birth_year,
            "planet_id": self.planet_id
        }
    
