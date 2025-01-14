import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.vehicle_service import (
    get_all_vehicles,
    get_vehicle,
    create_vehicle,
    update_vehicle,
    delete_vehicle
)
from utils.utils import generate_swagger_model
from models.vehicle import Vehicle

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing vehicles
vehicles_ns = Namespace('vehicle', description='CRUD operations for managing vehicles')

# Generate the Swagger model for the vehicle resource
vehicle_model = generate_swagger_model(
    api=vehicles_ns,
    model=Vehicle,
    exclude_fields=[],
    readonly_fields=['vehicle_id']
)


@vehicles_ns.route('/')
class VehicleList(Resource):
    """
    Handles operations on the collection of vehicles.
    Supports retrieving all vehicles (GET) and creating new vehicles (POST).
    """

    @vehicles_ns.doc('get_all_vehicles')
    @vehicles_ns.marshal_list_with(vehicle_model)
    def get(self):
        """
        Retrieve all vehicles.
        :return: List of all vehicles
        """
        try:
            return get_all_vehicles()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving vehicles: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving vehicles: {e}")
            vehicles_ns.abort(500, "An error occurred while retrieving the vehicles.")

    @vehicles_ns.doc('create_vehicle')
    @vehicles_ns.expect(vehicle_model, validate=True)
    @vehicles_ns.marshal_with(vehicle_model, code=201)
    def post(self):
        """
        Create a new vehicle.
        :return: The created vehicle with HTTP status code 201
        """
        data = vehicles_ns.payload
        try:
            return create_vehicle(
                data["client_id"],
                data["license_plate"],
                data["brand"],
                data["model"],
                data["year"]
            ), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating vehicle: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating vehicle: {e}")
            vehicles_ns.abort(500, "An error occurred while creating the vehicle.")


@vehicles_ns.route('/<int:vehicle_id>')
@vehicles_ns.param('vehicle_id', 'The ID of the vehicle')
class Vehicle(Resource):
    """
    Handles operations on a single vehicle.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a vehicle.
    """

    @vehicles_ns.doc('get_vehicle')
    @vehicles_ns.marshal_with(vehicle_model)
    def get(self, vehicle_id):
        """
        Retrieve a vehicle by ID.
        :param vehicle_id: The ID of the vehicle
        :return: The vehicle details or 404 if not found
        """
        try:
            vehicle = get_vehicle(vehicle_id)
            if not vehicle:
                vehicles_ns.abort(404, f"Vehicle with ID {vehicle_id} not found.")
            return vehicle
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving vehicle with ID {vehicle_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving vehicle with ID {vehicle_id}: {e}")
            vehicles_ns.abort(500, "An error occurred while retrieving the vehicle.")

    @vehicles_ns.doc('update_vehicle')
    @vehicles_ns.expect(vehicle_model, validate=True)
    @vehicles_ns.marshal_with(vehicle_model)
    def put(self, vehicle_id):
        """
        Update a vehicle by ID.
        :param vehicle_id: The ID of the vehicle
        :return: The updated vehicle details or 404 if not found
        """
        data = vehicles_ns.payload
        try:
            vehicle = update_vehicle(
                vehicle_id,
                data.get("client_id"),
                data.get("license_plate"),
                data.get("brand"),
                data.get("model"),
                data.get("year")
            )
            if not vehicle:
                vehicles_ns.abort(404, f"Vehicle with ID {vehicle_id} not found.")
            return vehicle
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating vehicle with ID {vehicle_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating vehicle with ID {vehicle_id}: {e}")
            vehicles_ns.abort(500, "An error occurred while updating the vehicle.")

    @vehicles_ns.doc('delete_vehicle')
    @vehicles_ns.response(204, 'Vehicle successfully deleted')
    def delete(self, vehicle_id):
        """
        Delete a vehicle by ID.
        :param vehicle_id: The ID of the vehicle
        :return: HTTP 204 status code if deleted successfully or 404 if not found
        """
        try:
            result = delete_vehicle(vehicle_id)
            if not result:
                vehicles_ns.abort(404, f"Vehicle with ID {vehicle_id} not found.")
            return '', 204
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting vehicle with ID {vehicle_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error deleting vehicle with ID {vehicle_id}: {e}")
            vehicles_ns.abort(500, "An error occurred while deleting the vehicle.")