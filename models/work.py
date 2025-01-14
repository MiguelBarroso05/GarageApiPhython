from utils.database import db

class Work(db.Model):
    """
    Represents a work/reparation in the database.

    Attributes:
        work_id (int): Primary key for the work table.
        vehicle_id (int): Foreign key referencing the vehicle being repaired.
        description (str): Description of the work being performed.
        status (str): Current status of the work (e.g., pending, in_progress, completed, cancelled).
        created_at (datetime): Timestamp when the work was created.
        updated_at (datetime): Timestamp when the work was last updated.
    """

    work_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"<Work {self.description} - {self.status}>"