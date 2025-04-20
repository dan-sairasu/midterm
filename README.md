# Travel Booking System

## Overview
this is a Python-based booking system for Out Midterm Examination. The system allows users to manage 

## Features
- Admin Terminal
- Client UI
- Booking Management


## Getting Started

### Prerequisites
- Python 3.12 or higher

### Installation
1. Clone the repository:
```
git clone https://github.com/dan-sairasu/midterm.git
```
2. Change to the project directory:
```
cd midterm
```
### Run the backend
3. Change to backend:
```
cd backend
```
4. Run the app backend
```
python app.py
```
### Run the Admin
5. navigate to admin folder
```
cd admin
```
6. Run the admin file
```
python admin.py
```
### Run the Client UI
7. navigate to client folder
```
cd client
```
8. Run the client on web browser
```
localhost/midterm/client
```



## Usage
### Admin on Terminal
1. User must run the admin python file
2. User must enter the admin username and password to login
3. User can add new package, delete and view all packages
### Client on Web Browser
1. User must run the client on web browser
2. User can view all packages offered

## Project Structure
The project consists of the following key components:

- `BookingSystem`: The main class that manages the booking system, destinations, and family bookings.
- `Destination`: Represents a travel destination with associated costs.
- `Family`: Represents a family booking, including the name, destination, and member details.
- `Person` (abstract), `Adult`, and `Child`: Classes that handle the cost calculations for different types of family members.

## UML Diagram
The project follows an object-oriented design, which is illustrated in the UML diagram below:

![SkyHigh Adventures Booking System UML Diagram](UML%20Diagram%20-%20Default.jpg)

## Contributing
Contributions, bug reports, and feature requests are welcome. Please follow the standard GitHub workflow (fork, branch, commit, push, and pull request).

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- The initial project requirements were provided by the RCIT 1763 - Object-Oriented Programming course at Bank Rakyat School of Business, Innovation, Technology and Entrepreneurship (BRSBITE).
