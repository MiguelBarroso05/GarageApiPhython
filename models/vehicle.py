from utils.database import db

class Vehicle(db.Model):
    """
    Represents a vehicle in the database.

    Attributes:
        vehicle_id (int): Primary key for the vehicle table.
        client_id (int): Foreign key referencing the owner client.
        license_plate (str): Vehicle's license plate. Must be unique and cannot be null.
        brand (str): Vehicle's brand.
        model (str): Vehicle's model.
        year (int): Manufacturing year of the vehicle.
        created_at (datetime): Timestamp when the vehicle was registered.
    """

    vehicle_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Vehicle {self.license_plate}>"