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


## Usage
1. When prompted, enter the family name.
2. Select a destination option (1-3).
3. Input the number of adults and children in the family.
4. Repeat the process for additional families or type 'quit' to finish.
5. The system will display the total cost for each family in Malaysian Ringgit (MYR).

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
