import React, { useState } from 'react';
import { Container, Col, Row, Form, Button, Modal } from 'react-bootstrap';
import { DateRangePicker } from 'react-date-range';
import 'bootstrap/dist/css/bootstrap.css';
import { makeRequest } from '../helpers';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';
import { differenceInDays } from 'date-fns';
import { useNavigate } from 'react-router-dom';

export const BookingForm = () => {
    
    const searchParams = new URLSearchParams(location.search);
    const listingID = searchParams.get('id');
    const postcode = searchParams.get('postcode');
    const [spaceToBook, setSpaceToBook] = useState({})
    const [showModal, setShowModal] = useState(false);
    const [totalPrice, setTotalPrice] = useState(0);
    const [dateRange, setDateRange] = useState({
        startDate: new Date(),
        endDate: new Date(),
        key: 'selection',
      });

    const navigate = useNavigate();

    // Retrieves car spaces from the backend every time the mapCentre changes
	React.useEffect(() => {

		// Retrieves car spaces given the postcode
		async function retrieveCarspaces(postcode: string) {
			let body = {
				"limit": "10",
				"sort": "false",
				"postcode": postcode,
			}
			try {
				let response = await makeRequest("/search/postcode", "POST", body, undefined);
				if (response.status !== 200) {
					console.log("There was an error!")
				} else {
					let spaces = response.resp;
					const carspaces = spaces['Postcode Search Results'];
                    Object.entries(carspaces).forEach(([key, value]) => {
                        if (value._id === listingID) {
                            setSpaceToBook(value);
                            console.log(value);
                        }
                    });
				}
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
        const myFunds = parseInt(localStorage.getItem('myFunds'), 10);
        const days = differenceInDays(dateRange.endDate, dateRange.startDate) + 1;
        if (totalPrice > myFunds) {
            setShowModal(true);
        } else {
            localStorage.setItem('myFunds', (myFunds - totalPrice).toString());
            navigate('/');
        }
    }

    const handleCloseModal = () => setShowModal(false);

    return (
        <Container>
            <br />
            <Row>
                <h1 style={{textAlign: "center"}}>book a carspace 📅</h1>
			</Row>
            <Row>
                <Form.Group>
                    <br />
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
                    <DateRangePicker minDate={new Date()} ranges={[dateRange]} onChange={handleSelect} />
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
            </Row><br />
            <Row>
                <Button onClick={handleBooking}>Book</Button>
            </Row>

            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Booking</Modal.Title>
                </Modal.Header>
                <Modal.Body>You do not have enough funds in your account to book for this many days. Add more funds to your account or reduce the length of your booking 😔</Modal.Body>
            </Modal>

        </Container>
    )
}