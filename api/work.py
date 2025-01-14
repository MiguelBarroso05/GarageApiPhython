import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.work_service import (
    get_all_works,
    get_work,
    create_work,
    update_work,
    delete_work
)
from utils.utils import generate_swagger_model
from models.work import Work

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing works
works_ns = Namespace('work', description='CRUD operations for managing works')

# Generate the Swagger model for the work resource
work_model = generate_swagger_model(
    api=works_ns,
    model=Work,
    exclude_fields=[],
    readonly_fields=['work_id', 'created_at', 'updated_at']
)


@works_ns.route('/')
class WorkList(Resource):
    """
    Handles operations on the collection of works.
    Supports retrieving all works (GET) and creating new works (POST).
    """

    @works_ns.doc('get_all_works')
    @works_ns.marshal_list_with(work_model)
    def get(self):
        """
        Retrieve all works.
        :return: List of all works
        """
        try:
            return get_all_works()
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving works: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving works: {e}")
            works_ns.abort(500, "An error occurred while retrieving the works.")

    @works_ns.doc('create_work')
    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model, code=201)
    def post(self):
        """
        Create a new work.
        :return: The created work with HTTP status code 201
        """
        data = works_ns.payload
        try:
            return create_work(
                data["vehicle_id"],
                data["description"]
            ), 201
        except HTTPException as http_err:
            logger.error(f"HTTP error while creating work: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error creating work: {e}")
            works_ns.abort(500, "An error occurred while creating the work.")


@works_ns.route('/<int:work_id>')
@works_ns.param('work_id', 'The ID of the work')
class Work(Resource):
    """
    Handles operations on a single work.
    Supports retrieving (GET), updating (PUT), and deleting (DELETE) a work.
    """

    @works_ns.doc('get_work')
    @works_ns.marshal_with(work_model)
    def get(self, work_id):
        """
        Retrieve a work by ID.
        :param work_id: The ID of the work
        :return: The work details or 404 if not found
        """
        try:
            work = get_work(work_id)
            if not work:
                works_ns.abort(404, f"Work with ID {work_id} not found.")
            return work
        except HTTPException as http_err:
            logger.error(f"HTTP error while retrieving work with ID {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error retrieving work with ID {work_id}: {e}")
            works_ns.abort(500, "An error occurred while retrieving the work.")

    @works_ns.doc('update_work')
    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model)
    def put(self, work_id):
        """
        Update a work by ID.
        :param work_id: The ID of the work
        :return: The updated work details or 404 if not found
        """
        data = works_ns.payload
        try:
            work = update_work(
                work_id,
                data["status"],
                data.get("description")
            )
            if not work:
                works_ns.abort(404, f"Work with ID {work_id} not found.")
            return work
        except HTTPException as http_err:
            logger.error(f"HTTP error while updating work with ID {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error updating work with ID {work_id}: {e}")
            works_ns.abort(500, "An error occurred while updating the work.")

    @works_ns.doc('delete_work')
    @works_ns.response(204, 'Work successfully deleted')
    def delete(self, work_id):
        """
        Delete a work by ID.
        :param work_id: The ID of the work
        :return: HTTP 204 status code if deleted successfully or 404 if not found
        """
        try:
            result = delete_work(work_id)
            if not result:
                works_ns.abort(404, f"Work with ID {work_id} not found.")
            return '', 204
        except HTTPException as http_err:
            logger.error(f"HTTP error while deleting work with ID {work_id}: {http_err}")
            raise http_err
        except Exception as e:
            logger.error(f"Error deleting work with ID {work_id}: {e}")
            works_ns.abort(500, "An error occurred while deleting the work.")