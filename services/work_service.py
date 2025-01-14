import logging
from utils.database import db
from models.work import Work

logger = logging.getLogger(__name__)

def get_all_works():
    """
    Retrieve all works.
    :return: List of dictionaries containing work data.
    """
    try:
        works = Work.query.all()
        return [
            {
                "work_id": work.work_id,
                "vehicle_id": work.vehicle_id,
                "description": work.description,
                "status": work.status,
                "created_at": work.created_at,
                "updated_at": work.updated_at,
            }
            for work in works
        ]
    except Exception as e:
        logger.error(f"Error fetching all works: {e}")
        return {"error": "Internal Server Error"}

def get_work(work_id):
    """
    Retrieve a work by ID.
    :param work_id: The ID of the work to retrieve.
    :return: Dictionary containing work data or None if not found.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        return {
            "work_id": work.work_id,
            "vehicle_id": work.vehicle_id,
            "description": work.description,
            "status": work.status,
            "created_at": work.created_at,
            "updated_at": work.updated_at,
        }
    except Exception as e:
        logger.error(f"Error fetching work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def create_work(vehicle_id, description):
    """
    Create a new work.
    :param vehicle_id: ID of the vehicle being repaired.
    :param description: Description of the work.
    :return: Dictionary containing the newly created work's data.
    """
    try:
        work = Work(vehicle_id=vehicle_id, description=description)
        db.session.add(work)
        db.session.commit()
        return {
            "work_id": work.work_id,
            "vehicle_id": work.vehicle_id,
            "description": work.description,
            "status": work.status,
            "created_at": work.created_at,
            "updated_at": work.updated_at,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating work: {e}")
        return {"error": "Internal Server Error"}

def update_work(work_id, status, description=None):
    """
    Update an existing work.
    :param work_id: ID of the work to update.
    :param status: New status of the work.
    :param description: Updated description (optional).
    :return: Dictionary containing the updated work's data.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None

        work.status = status
        if description:
            work.description = description

        db.session.commit()
        return {
            "work_id": work.work_id,
            "vehicle_id": work.vehicle_id,
            "description": work.description,
            "status": work.status,
            "created_at": work.created_at,
            "updated_at": work.updated_at,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_work(work_id):
    """
    Delete a work.
    :param work_id: The ID of the work to delete.
    :return: True if deletion was successful, False otherwise.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        db.session.delete(work)
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting work {work_id}: {e}")
        return {"error": "Internal Server Error"}