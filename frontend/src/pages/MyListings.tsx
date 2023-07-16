import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Modal } from 'react-bootstrap';
import { makeRequest } from '../helpers';

export const MyListings = (props: any) => {

    const username = props.username;
    let token = localStorage.getItem('authToken') || '';
    const [myListings, setMyListings] = useState([{}]);
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [listingToBeUpdated, setListingToBeUpdated] = useState('');
    const [listingToBeDeleted, setListingToBeDeleted] = useState('');

    useEffect(() => {
        // Retrieves car spaces given the postcode
		async function retrieveListings() {
			try {
				let response = await makeRequest(`/carspace/get_car_space_Info/${username}`, "GET", undefined, { token });
				if (response.status !== 200) {
					console.log("There was an error!")
				} else {
					let listings = response.resp;
                    setMyListings(listings);
                    return listings;
				}
			} catch (error) {
				console.log(error);
			}
			return 0;
		}
        retrieveListings();
    }, [myListings])

    const updateListingCheck = (id: string) => {
        setListingToBeUpdated(id);
        setShowModal(true);
        console.log(id);
    }

    const updateListing = () => {
        // TODO
        // Update the listing
        console.log(listingToBeUpdated);
        //
        setListingToBeUpdated('');
        setShowModal(false);
    }

    const deleteListingCheck = (id: string) => {
        setListingToBeDeleted(id);
        setShowDeleteModal(true);
        console.log(id);
    }

    const deleteListing = () => {
        // TODO
        // Delete the listing
        console.log(listingToBeDeleted);
        //
        setListingToBeDeleted('');
        setShowDeleteModal(false);
    }

	const handleCloseModal = () => setShowModal(false);
    const handleCloseDeleteModal = () => setShowDeleteModal(false);

    return (
        <Container>
            { myListings && Object.entries(myListings).map(([key, value]) => (
                <>
                    <Row className="align-items-center" style={{ border:'1px solid black', borderRadius: '8px', padding: '10px 10px 10px 0px' }}>
                        <Col md="auto">
                            <img style={{ width: '150px', height: '150px' }}/>
                        </Col>
                        <Col className="text-center">
                            <span style={{ fontSize: '35pt' }}>${value["Your Car Space Information"] && value["Your Car Space Information"]["price"]}</span> <br />
                            <span><i>per day</i></span>
                        </Col>
                        <Col >
                            <span style={{ fontSize: '15pt' }}>📍 {value["Your Car Space Information"] && value["Your Car Space Information"]["suburb"]}</span> <br />
                            <span style={{ fontSize: '15pt' }}>📏 {value["Your Car Space Information"] && value["Your Car Space Information"]["width"]} m by {value["Your Car Space Information"] && value["Your Car Space Information"]["breadth"]} m</span><br />
                            <span style={{ fontSize: '15pt' }}>🚗 {value["Your Car Space Information"] && value["Your Car Space Information"]["vehiclesize"].replace(/^\w/, (c: string) => c.toUpperCase())}</span>
                        </Col>
                        <Col className="text-center" md="auto">
                            <Row>
                                <Button style={{ width: '100px' }} onClick={() => updateListingCheck("1")}>edit</Button>
                            </Row><br />
                            <Row>
                                <Button variant='danger' style={{ width: '100px' }} onClick={() => deleteListingCheck("1")}>delete</Button>
                            </Row>
                        </Col>
                    </Row><br />
                </>
            ))}

            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Carspace</Modal.Title>
                </Modal.Header>
                <Modal.Body>Carspace Info</Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={updateListing}>Update</Button>
                </Modal.Footer>
            </Modal>

            <Modal show={showDeleteModal} onHide={handleCloseDeleteModal}>
                <Modal.Header closeButton>
                    <Modal.Title>delete carspace 🗑️</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Row className="text-center">
                        <span>Are you sure you want to delete this carspace listing?</span><br />
                        <span><b>All existing bookings will be cancelled</b> 😱</span><br /><br />
                    </Row>  
                    <Row>
                        <Col className="text-center">
                            <Button style={{ width: '100px' }} onClick={handleCloseDeleteModal}>No</Button>
                        </Col>
                        <Col className="text-center">
                            <Button variant="danger" style={{ width: '100px' }} onClick={deleteListing}>Yes</Button>
                        </Col>
                    </Row>
                </Modal.Body>
            </Modal>
        </Container>
    )
}