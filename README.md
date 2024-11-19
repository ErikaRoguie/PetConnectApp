# Pet Connect Application

A web application for managing and displaying pet information, featuring superhero-themed pet profiles with inventory management capabilities.

## Overview

Pet Connect is a Flask-based web application that allows users to manage and showcase pets with a unique superhero theme. The application includes features for managing pet profiles, inventory tracking, and a catalogue display system.

Version: 0.1.0

## Tech Stack

- **Backend**: Python 3.11 with Flask
- **Database**: PostgreSQL
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Data Import**: Support for Microsoft Access database import

## Dependencies

- Flask (^3.0.3)
- Flask-SQLAlchemy (^3.1.1)
- pyodbc (^5.1.0)
- psycopg2-binary (^2.9.9)

## Features

- **Pet Profile Management**
  - Create, read, update, and delete pet profiles
  - Upload and manage pet images
  - Track superhero characteristics (hero name, superpower, hero type)

- **Catalogue System**
  - Search functionality
  - Sorting capabilities
  - Responsive grid layout

- **Inventory Management**
  - Track pet-specific inventory
  - Manage premade items
  - Quantity tracking

- **Resource Center**
  - Educational materials
  - Pet care information
  - Supporting documentation

## Quick Start (Replit)

1. Fork the Repl from [Replit](https://replit.com/@username/pet-connect)
2. Click the "Run" button to start the application
3. The application will automatically:
   - Install required dependencies
   - Set up the PostgreSQL database
   - Create necessary tables
   - Start the Flask server

The application will be available at the URL provided by Replit.

## Environment Configuration

### Required Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/petconnect

# Optional Configuration
DEBUG=True  # Enable debug mode (default: False)
PORT=5000   # Server port (default: 5000)
HOST=0.0.0.0  # Server host (default: 0.0.0.0)
```

### Port Configuration

The application uses the following port configurations:
- Local development: Port 5000
- Replit deployment: External port 80, mapped to local port 5000

## Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pet-connect.git
   cd pet-connect
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/petconnect
   ```

4. Initialize the database:
   ```bash
   python main.py
   ```

## API Endpoints

### Pets

- `GET /api/pets` - Retrieve all pets (supports search parameter)
- `POST /api/pets` - Create a new pet
- `PUT /api/pets/<pet_id>` - Update an existing pet
- `DELETE /api/pets/<pet_id>` - Delete a pet

### Inventory

- `GET /api/inventory` - Retrieve all inventory items
- `POST /api/inventory` - Create a new inventory item
- `PUT /api/inventory/<item_id>` - Update an existing inventory item
- `DELETE /api/inventory/<item_id>` - Delete an inventory item

## Database Schema

### SuperPet Table
```sql
CREATE TABLE super_pet (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hero_name VARCHAR(100),
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),
    color VARCHAR(50),
    superpower VARCHAR(100),
    hero_type VARCHAR(50),
    hero_appearance VARCHAR(200),
    image_url VARCHAR(255)
);
```

### Inventory Table
```sql
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES super_pet(id) NOT NULL,
    quantity INTEGER NOT NULL,
    is_premade BOOLEAN NOT NULL DEFAULT FALSE
);
```

## Development

The application uses a modular structure:
- `main.py` - Application entry point and route definitions
- `models.py` - Database models
- `db_utils.py` - Database utility functions
- `static/` - Frontend assets (JS, CSS, images)
- `templates/` - HTML templates

## Project Structure
```
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── catalogue.js
│   │   ├── inventory.js
│   │   └── main.js
│   └── images/
├── templates/
│   ├── base.html
│   ├── catalogue.html
│   ├── index.html
│   ├── inventory.html
│   ├── pets.html
│   └── resources.html
├── main.py
├── models.py
├── db_utils.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Running the Application

Start the server:
```bash
python main.py
```
The application will be available at `http://localhost:5000`

## Deployment

The application is configured to deploy on Replit:
1. Fork the Repl
2. The environment will automatically configure:
   - Python 3.11
   - PostgreSQL database
   - Required system dependencies
3. Click the "Run" button to deploy
4. Access your application via the provided Replit URL

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify DATABASE_URL environment variable is correctly set
   - Ensure PostgreSQL service is running
   - Check database user permissions

2. **Image Upload Issues**
   - Check upload directory permissions
   - Verify allowed file extensions (`png`, `jpg`, `jpeg`, `gif`)
   - Ensure sufficient disk space

3. **Access Database Import Issues**
   - Ensure Microsoft Access drivers are installed
   - Verify Access database file path
   - Check file permissions

4. **Port Binding Issues**
   - Check if port 5000 is already in use
   - Verify port permissions
   - Use `lsof -i :5000` to check port usage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback about Pet Connect:
- **Project Link**: [https://replit.com/@username/pet-connect](https://replit.com/@username/pet-connect)
- **Report Issues**: Use the Issues tab on the Replit project
- **Feature Requests**: Create a new thread in the Replit project's Discussions tab

## Acknowledgments

- Thanks to all contributors who have helped shape Pet Connect
- Special thanks to the open-source community for the tools and libraries used in this project
- Inspiration from superhero comics and pet care services

---
© 2024 Pet Connect. All rights reserved.
