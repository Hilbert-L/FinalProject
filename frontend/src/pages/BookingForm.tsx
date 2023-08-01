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
import { NotificationBox } from '../components/NotificationBox';

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
    const [currentReservations, setCurrentReservations] = useState([]);
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
                    Object.entries(carspaces).forEach(([key, value]) => {
                        if (value && value._id === listingID) {
                            setSpaceToBook(value);
                            currentListing = value;
                            console.log(value);
                        }
                    });
				}
                // let daysBetween = []
                // if (currentListing) {
                //     let reservations = await makeRequest(`/carspace/get_car_space_booking/${currentListing.carspaceid}`, "GET", undefined, { token });
                //     setCurrentReservations(reservations.resp);
                //     const extractedDays = reservations.resp.map(({ start_time, end_time }) => {
                //         const startDate = new Date(start_time);
                //         const endDate = new Date(end_time);
                      
                //         // Calculate the difference in days between the start and end dates
                //         const timeDiff = endDate.getTime() - startDate.getTime();
                //         const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
                      
                //         // Create an array to store the days between the start and end dates (including start date)
                //         const daysBetween = [];
                //         for (let i = 0; i < daysDiff; i++) {
                //           const day = new Date(startDate);
                //           day.setDate(day.getDate() + i);
                //           daysBetween.push(day.toLocaleDateString());
                //         }
                        
                //     })
                //     console.log(daysBetween);
                //     console.log(reservations.resp)
                    
                // }
			} catch (error) {
				console.log(error);
			}
			return 0;
		}

		retrieveCarspaces(postcode ? postcode : "");

	}, []);

    React.useEffect(() => {
        const days = differenceInDays(dateRange.endDate, dateRange.startDate) + 1;
        if (isNaN(days * spaceToBook.price)) return;
        setTotalPrice(days * spaceToBook.price)
    }, [dateRange]);

    const handleSelect = (ranges) => {
        setDateRange(ranges.selection);
      }

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
                setSuccess(true);
                localStorage.setItem('booked', 'true')
                navigate("/");
            } else {
                setError(resp.resp.detail);
                setShowNotification(true)
            }
        })
        
    }

    function isSameDay(date1: any, date2: any) {
        return (
          date1.getDate() === date2.getDate() &&
          date1.getMonth() === date2.getMonth() &&
          date1.getFullYear() === date2.getFullYear()
        );
      }

    function renderDayContent(day: any) {

        const disabledDays = [new Date('08/10/2023'), new Date('08/15/2023')];
      
        // Check if the current day is one of the disabled days
        const isDisabled = disabledDays.some(disabledDay => isSameDay(day, disabledDay));;
      
        // Style for disabled days
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
                {/* {showNotification && 
                <NotificationBox position='middle-center' variant='danger' title='🚫 Booking Error' message={error} ></NotificationBox>
                } */}
            </Container>
            <Modal show={!!error} onHide={() => setError("")}>
                <Modal.Header closeButton>
                    <Modal.Title>Booking unsuccessful</Modal.Title>
                </Modal.Header>
                <Modal.Body>{error}</Modal.Body>
            </Modal>
            {/* <Modal show={success} onHide={() => navigate("/")}>
                <Modal.Header closeButton>
                    <Modal.Title>Booking Successful!</Modal.Title>
                </Modal.Header>
                <Modal.Footer>
                    <Button onClick={() => navigate("/")}>OK</Button>
                </Modal.Footer>
            </Modal> */}
        </>
    )
}