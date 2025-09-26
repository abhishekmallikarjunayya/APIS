# APIS
A full-stack CRUD web application for managing car information, built with FastAPI as the backend and a simple HTML/JS frontend. Supports multiple storage backends:  In-memory JSON (demo mode)  SQLite / PostgreSQL (SQLAlchemy ORM)  MongoDB (Motor async driver)


Started with FastAPI + JSON

Built a simple REST API to manage cars.
Used Pydantic models to define the data structure.
Supported GET (list all cars) and POST (add a car).
Frontend was a simple HTML/JS table interacting with JSON APIs.

2. Extended to relational databases (SQLite & PostgreSQL)

Switched from in-memory storage to SQL databases.
Learned to define tables and columns for cars.
Used SQLAlchemy / async drivers for database operations.
CRUD operations became persistent—data remains even if the server restarts.
Same frontend could work with minimal changes.

3️. Integrated MongoDB (NoSQL)

Used Motor (async MongoDB client) to store cars as documents.
MongoDB documents have _id, converted to id for frontend.
Learned to handle ObjectId conversion, which caused undefined ID issue earlier.
Frontend now interacts seamlessly with a NoSQL backend.

4️. Built a Realistic Car Info App

Full CRUD functionality:
Create new cars
Read car list
Update car details
Delete cars

==>Frontend features:
Editable form (for add & edit)
Table with Edit/Delete buttons
IDs displayed correctly
Styled modern UI with CSS

==>Backend handles:
Async API calls
MongoDB _id handling
Validation with Pydantic

Key Learnings

FastAPI makes async API development simple.
JSON, SQL, and NoSQL can all be used with similar REST APIs.
Frontend JS can interact with any backend via fetch/AJAX.
Handling IDs correctly (esp. MongoDB _id) is crucial for Edit/Delete functionality.

A realistic web app requires both backend and frontend working together.
