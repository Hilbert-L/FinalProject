import React, { useState, useRef } from 'react';
import { Container, Col, Row, Form, Button, Modal, FloatingLabel } from 'react-bootstrap';
import { DateRangePicker } from 'react-date-range';
import 'bootstrap/dist/css/bootstrap.css';
import { makeRequest } from '../helpers';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';
import { differenceInDays } from 'date-fns';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';

interface TimeRange {
    start_time: string;
    end_time: string;
  }

export const BookingForm = () => {
    
    const token = localStorage.getItem('authToken');
    const searchParams = new URLSearchParams(location.search);
    const listingID = searchParams.get('id');
    const postcode = searchParams.get('postcode');
    const [spaceToBook, setSpaceToBook] = useState({})
    const [totalPrice, setTotalPrice] = useState(0);
    const [carRegistration, setCarRegistration] = useState('');
    const [vehicleType, setVehicleType] = useState('');
    const [showNotification, setShowNotification] = useState(false);
    const [currentReservations, setCurrentReservations] = useState([new Date]);
    const [dateRange, setDateRange] = useState({
        startDate: new Date(),
        endDate: new Date(),
        key: 'selection',
      });

    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const navigate = useNavigate();

    // Retrieves car spaces from the backend every time the mapCentre changes
	React.useEffect(() => {
		// Retrieves car spaces given the postcode
		async function retrieveCarspaces(postcode: string) {
            let currentListing = null;
			let body = {
				"limit": "100",
				"sort": "false",
				"postcode": postcode,
			}
			try {
				let response = await makeRequest("/search/postcode", "POST", body, undefined);
				if (response.status !== 200) {
					console.log("There was an error!");
                    return;
				} else {
					let spaces = response.resp;
					const carspaces = spaces['Postcode Search Results'];
                    // Runs through all of the carspaces in that postcode
                    Object.entries(carspaces).forEach(([key, value]) => {
                        // Checks if the id is equal to the id of the carspace the user wants to book
                        if (value && value._id === listingID) {
                            // Sets this as the space to book
                            setSpaceToBook(value);
                            currentListing = value;
                        }
                    });
				}
                if (currentListing) {
                    // Retrieves all the existing bookings for the given carspace
                    let reservations = await makeRequest(`/carspace/get_car_space_booking/${currentListing.carspaceid}`, "GET", undefined, { token });
                    // Finds all of the dates the car space is booked, given the ranges of the reservations
                    let allDates = extractDatesBetween(reservations.resp);
                    let allDatesList = [new Date];
                    // For each of the dates, extracts the day, month and year
                    allDates.forEach((dateString) => {
                        const parts = dateString.split('/');
                        const month = parseInt(parts[1], 10) - 1;
                        const day = parseInt(parts[0], 10);
                        const year = parseInt(parts[2], 10);
                        // Creates a date object for the date and adds it into the array
                        const dateObject = new Date(year, month, day);
                        allDatesList.push(dateObject);
                      });
                    setCurrentReservations(allDatesList);
                }
			} catch (error) {
				console.log(error);
			}
			return 0;
		}

		retrieveCarspaces(postcode ? postcode : "");

	}, []);

    // Finds all of the days between a given start and end date
    const extractDatesBetween = (data: TimeRange[]): string[] => {
        const result: string[] = [];
        data.forEach(({ start_time, end_time }) => {
            // Extracts the start and end date
            const startDate = new Date(start_time);
            const endDate = new Date(end_time);
            const currentDate = new Date(startDate);
            // Loops through the dates until it hits the end date
            while (currentDate <= endDate) {
                // Adds a date object to the array then moves onto the next date
                result.push(new Date(`${currentDate.getMonth() + 1}/${currentDate.getDate()}/${currentDate.getFullYear()}`).toLocaleDateString());
                currentDate.setDate(currentDate.getDate() + 1);
            }
        });
        return result;
      };

    React.useEffect(() => {
        const days = differenceInDays(dateRange.endDate, dateRange.startDate) + 1;
        // Finds the total price; returns if it is not a number
        if (isNaN(days * spaceToBook.price)) return;
        setTotalPrice(days * spaceToBook.price)
    }, [dateRange]);
    // Allows for a range of dates to be selected
    const handleSelect = (ranges) => {
        setDateRange(ranges.selection);
      }

    // Sends the booking request to the backend
    const handleBooking = () => {
        const token = localStorage.getItem("authToken");
        const username = localStorage.getItem("username");
        if (!token || !username) return;
        makeRequest(
            `/booking/create_booking/${username}/${spaceToBook.carspaceid}?provider_username=${spaceToBook.username}`,
            "POST",
            {
                start_date: dayjs(dateRange.startDate).toISOString(),
                end_date: dayjs(dateRange.endDate).toISOString()
            },
            { token }
        ).then((resp) => {
            if (resp.status === 200) {
                // If successful, returns to the search page
                setSuccess(true);
                localStorage.setItem('booked', 'true')
                navigate("/");
            } else {
                setError(resp.resp.detail);
                setShowNotification(true)
            }
        })
        
    }

    // A simple function used to check if two given dates are the same
    function isSameDay(date1: any, date2: any) {
        return (
          date1.getDate() === date2.getDate() &&
          date1.getMonth() === date2.getMonth() &&
          date1.getFullYear() === date2.getFullYear()
        );
      }

    // Used to render the days on the calendar a certain way
    function renderDayContent(day: any) {

        const disabledDays = currentReservations;
        // Check if the current day is one of the disabled days
        const isDisabled = disabledDays.some(disabledDay => isSameDay(day, disabledDay));
      
        // Style for disabled days; red font with strikethrough
        const disabledStyles = {
          color: 'red',
          textDecoration: 'line-through'
        };
      
        return (
          <div style={isDisabled ? disabledStyles: {color: 'grey'}}>
            {day.getDate()}
          </div>
        );
    }

    // Ensures all required fields are filled out
    const allFilledOut = carRegistration !== '' && vehicleType !== '' && totalPrice !== 0;

    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    return (
        <>
            <Container>
                <br />
                <Row>
                    <h1 style={{textAlign: "center"}}>book a carspace 📅</h1>
                </Row>
                <Row>
                    <Form.Group>
                        <Form.Label>Address</Form.Label>
                            <Form.Control
                            type="text"
                            value={spaceToBook.address}
                            disabled
                            />
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group>
                        <br />
                        <Form.Label>Price (per day)</Form.Label>
                            <Form.Control
                            type="text"
                            value={`$${spaceToBook.price}`}
                            disabled
                            />
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group>
                        <br />
                        <Form.Label>Provider</Form.Label>
                            <Form.Control
                            type="text"
                            value={spaceToBook.username}
                            disabled
                            />
                    </Form.Group>
                </Row><hr />
                <Row>
                    <Col className="d-flex justify-content-center">
                        <DateRangePicker dayContentRenderer={renderDayContent} minDate={new Date()} ranges={[dateRange]} onChange={handleSelect} />
                    </Col>
                </Row>
                <Row>
                    <Form.Group>
                        <br />
                        <Form.Label>Total Price</Form.Label>
                            <Form.Control
                            type="text"
                            value={`$${totalPrice}`}
                            disabled
                            />
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group>
                        <br />
                        <Form.Label>Car Registration</Form.Label>
                            <Form.Control
                            type="text"
                            placeholder='Please enter your car registration'
                            onChange={(event) => {setCarRegistration(event.target.value)}}
                            />
                    </Form.Group>
                </Row><br />
                <Row>
                    <Form.Group>
                        <Form.Label>Vehicle Type</Form.Label>
                        <FloatingLabel controlId="floatingVehicleType" label="Vehicle Type" className="mb-3">
                            <Form.Select onChange={(event) => {setVehicleType(event.target.value)}}>
                            <option value="">Please select an option</option>
                            <option value="hatchback">Hatchback</option>
                            <option value="sedan">Sedan</option>
                            <option value="suv">SUV</option>
                            <option value="ev">EV</option>
                            <option value="ute">Ute</option>
                            <option value="wagon">Wagon</option>
                            <option value="van">Van</option>
                            <option value="bike">Bike</option>
                            </Form.Select>
                        </FloatingLabel>
                    </Form.Group>
                </Row><br />
                <Row>
                    <Button onClick={handleBooking} disabled={!allFilledOut}>Book</Button>
                </Row><br />
            </Container>
            <Modal show={!!error} onHide={() => setError("")}>
                <Modal.Header closeButton>
                    <Modal.Title>Booking unsuccessful</Modal.Title>
                </Modal.Header>
                <Modal.Body>{error}</Modal.Body>
            </Modal>
        </>
    )
}