from __init__ import CURSOR, CONN


class Employee:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, job_title,  id=None):
        self.id = id
        self.name = name
        self.job_title = job_title

    def __repr__(self):
        return (
            f"<Employee {self.id}: {self.name}, {self.job_title}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Employee instances """
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Employee instances """
        sql = """
            DROP TABLE IF EXISTS employees;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title values of the current Employee object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO employees (name, job_title)
                VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.job_title))
        CONN.commit()

        self.id = CURSOR.lastrowid
        Employee.all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Employee object."""
        sql = """
            UPDATE employees
            SET name = ?, job_title = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.job_title, self.id))
        CONN.commit()

    def delete(self):
        """Delete the row corresponding to the current Employee object"""
        sql = """
            DELETE FROM employees
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def create(cls, name, job_title):
        """ Initialize a new Employee object and save the object to the database """
        employee = Employee(name, job_title)
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        """Return an Employee object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        employee = Employee.all.get(row[0])
        if employee:
            # ensure attributes match row values in case local instance was modified
            employee.name = row[1]
            employee.job_title = row[2]
        # not in dictionary, create new instance and add to dictionary
        else:
            employee = cls(row[1], row[2])
            employee.id = row[0]
            Employee.all[employee.id] = employee
        return employee

    @classmethod
    def get_all(cls):
        """Return a list containing one Employee object per table row"""
        sql = """
            SELECT *
            FROM employees
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Employee object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM employees
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Employee object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM employees
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
