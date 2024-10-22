# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?

- Although item and user are split, the user module still uses the Item class for some of its functions. Technically, 
one could think to keep a duplicate of the Item class within the user module, the problem there is that such 
microservices run into the risk of schema desyncing, and the management of DB migrations on that table would become 
not obvious.
- If we were to run the user module as independent unit we'd have item_id which is configured as foreign key of a 
non-existent table, because the item table is not declared there. 

2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?

- The Session instance is manually propagated everywhere. Passing around the session like so is coupling the 
persistence layer with everything else and although SQLALchemy has some flexibility, it's 
definitely locking in the project in a way. For example: if in the current state of things we were to introduce 
testing with a persistence layer simulated using a dictionary, we would not be able to.

3. What would be your plan to refactor the project to stick to the clean architecture?

- Use a repository pattern coupled with FastAPI's Depends class to modularize the persistence layer. I'd also unify the 
model declaration in a single file so that alembic migrations won't be an issue and the modules can actually work with 
the complete DB model. 

4. How can you make dependencies between modules more explicit?

- My answer was to move everything that was forcibly interconnected (like the persistence layer) in one place, decoupling as much as possible anything else. I'd say this could be realistically deployed as a distributed monolith now.
Complete summary of what I did:
- Refactored the persistence layer to be in just one place (`be_task_ca.database` package)
- Refactored the repository to use the repository pattern with a tight integration both with the Python generics and 
the FastAPI dependency system
- Removed some manual conversions (pydantic takes care of automatically doing that, which allowed me to decouple more code)
- Decoupled most of the persistence layer from the actual routing implementation. `usecases.py` doesn't really know what the repository does nor does it need to manually handle DB-explicit code
- Added rudimentary tests with a separate DB configuration, overriding the one the application uses as standard (for practical purposes it's the same Sqlite in-memory DB, but it doesn't need to be)
- Added the Sqlite in-memory DB
Other things that were just corrections:
- Removed some manual duplicated key checks (I instead catch the integrity exception)
- Made the whole app more REST-compliant (201 status code added, removed the object with just a list of other objects as a field, added directly the list of objects to the route)
- Updated the libraries so that I could use a top to bottom async implementation
- Added typing where it was needed so that Swagger could show the correct documentation

*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.