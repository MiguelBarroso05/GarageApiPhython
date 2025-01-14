import logging
from utils.database import db
from models.vehicle import Vehicle

logger = logging.getLogger(__name__)

def get_all_vehicles():
    """
    Retrieve all vehicles.
    :return: List of dictionaries containing vehicle data.
    """
    try:
        vehicles = Vehicle.query.all()
        return [
            {
                "vehicle_id": vehicle.vehicle_id,
                "client_id": vehicle.client_id,
                "license_plate": vehicle.license_plate,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "created_at": vehicle.created_at,
            }
            for vehicle in vehicles
        ]
    except Exception as e:
        logger.error(f"Error fetching all vehicles: {e}")
        return {"error": "Internal Server Error"}

def get_vehicle(vehicle_id):
    """
    Retrieve a vehicle by ID.
    :param vehicle_id: The ID of the vehicle to retrieve.
    :return: Dictionary containing vehicle data or None if not found.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        return {
            "vehicle_id": vehicle.vehicle_id,
            "client_id": vehicle.client_id,
            "license_plate": vehicle.license_plate,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "created_at": vehicle.created_at,
        }
    except Exception as e:
        logger.error(f"Error fetching vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

def create_vehicle(client_id, license_plate, brand, model, year):
    """
    Create a new vehicle.
    :param client_id: ID of the client who owns the vehicle.
    :param license_plate: Vehicle's license plate.
    :param brand: Vehicle's brand.
    :param model: Vehicle's model.
    :param year: Manufacturing year of the vehicle.
    :return: Dictionary containing the newly created vehicle's data.
    """
    try:
        vehicle = Vehicle(
            client_id=client_id, license_plate=license_plate, brand=brand, model=model, year=year
        )
        db.session.add(vehicle)
        db.session.commit()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "client_id": vehicle.client_id,
            "license_plate": vehicle.license_plate,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "created_at": vehicle.created_at,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating vehicle: {e}")
        return {"error": "Internal Server Error"}

def update_vehicle(vehicle_id, client_id, license_plate, brand, model, year):
    """
    Update an existing vehicle.
    :param vehicle_id: ID of the vehicle to update.
    :param client_id: ID of the client who owns the vehicle.
    :param license_plate: Vehicle's license plate.
    :param brand: Vehicle's brand.
    :param model: Vehicle's model.
    :param year: Manufacturing year of the vehicle.
    :return: Dictionary containing the updated vehicle's data.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None

        vehicle.client_id = client_id or vehicle.client_id
        vehicle.license_plate = license_plate or vehicle.license_plate
        vehicle.brand = brand or vehicle.brand
        vehicle.model = model or vehicle.model
        vehicle.year = year or vehicle.year

        db.session.commit()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "client_id": vehicle.client_id,
            "license_plate": vehicle.license_plate,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "created_at": vehicle.created_at,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_vehicle(vehicle_id):
    """
    Delete a vehicle.
    :param vehicle_id: The ID of the vehicle to delete.
    :return: True if deletion was successful, False otherwise.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        db.session.delete(vehicle)
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}
