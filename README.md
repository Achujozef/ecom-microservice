# Microservice Ecommerce Application

## Overview

This is a microservice application that transforms a tightly coupled ecommerce application into a loosely coupled microservice architecture. The application comprises six services, with five of them built in Django and one built using Flask.

## Services

1. **Banner Service (Flask)**: This service is responsible for managing and displaying banners on the frontend.

2. **API Gateway Service (Django)**: The API gateway service serves as the entry point to the application. It provides user authentication and routing requests to the appropriate microservices.

3. **Wallet Service (Django)**: The Wallet service handles user wallet functionality, including transactions and balances.

4. **Category Service (Django)**: The Category service manages product categories and their relationships.

5. **Product Service (Django)**: This service is responsible for managing product information, including product details and images.

6. **Product Variant Service (Django)**: The Product Variant service manages different variants of products, such as size, color, and availability.

## Design Principles

The microservice application follows the REST architectural style. It emphasizes synchronous actions and leverages the REST principles for communication between services.

## HTML Templates

All HTML templates are centralized in the Gateway service. This ensures a single point of control for frontend templates, simplifying management and maintenance.

## Usage

To run the microservice application, follow the steps below:

1. **Prerequisites**:
   - Ensure you have Python and the necessary packages (Django and Flask) installed.
   - Set up a suitable database system (e.g., PostgreSQL) and configure the connection in Django settings.

2. **Service Configuration**:
   - Configure the settings for each service, such as database connections, API endpoints, and any environment-specific variables.

3. **Running the Services**:
   - Start each service individually. You can use Django's `python manage.py runserver` for Django services and Flask's built-in development server for the Flask service.
   - Make sure the API Gateway service is running to act as the entry point.

4. **Testing**:
   - Implement comprehensive testing for each service to ensure functionality and interaction between services.

5. **Deployment**:
   - Consider containerizing your services using Docker for ease of deployment.

## Contribution Guidelines

We welcome contributions to this microservice application. If you would like to contribute, please follow these guidelines:

- Fork the repository and create a feature branch for your changes.
- Ensure that your code adheres to the coding standards of the respective service (Django or Flask).
- Write tests to cover new functionality.
- Submit a pull request with a clear description of your changes.

## License

This microservice application is open-source and released under the [MIT License](LICENSE). You are free to use, modify, and distribute it in accordance with the license terms.

## Contact

If you have questions or need further assistance, feel free to contact us at [your contact email].

Happy microservice development!
