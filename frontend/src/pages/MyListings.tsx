import { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Modal } from 'react-bootstrap';
import { makeRequest } from '../helpers';
import { DateRangePicker } from 'react-date-range';
import { ListingComponent } from '../components/ListingComponent';
import { NotificationBox } from '../components/NotificationBox';

export const MyListings = (props: any) => {

    const username = props.username;
    let token = localStorage.getItem('authToken') || '';
    const [myListings, setMyListings] = useState([{}]);
    const [showBookingsModal, setShowBookingsModal] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [bookingsListingToBeChecked, setBookingsListingToBeChecked] = useState('');
    const [listingToBeUpdated, setListingToBeUpdated] = useState('');
    const [listingToBeDeleted, setListingToBeDeleted] = useState('');
    const [triggerRender, setTriggerRender] = useState(true);
    const [showNotification, setShowNotification] = useState(false);
    const [dateRange, setDateRange] = useState({
        startDate: new Date(),
        endDate: new Date(),
        key: 'selection',
      });

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
    }, [triggerRender])

    const bookingListingCheck = (id: string) => {
        setBookingsListingToBeChecked(id);
        setShowBookingsModal(true);
        console.log(id);
    }

    const updateListingCheck = (id: string) => {
        setListingToBeUpdated(id);
        setShowModal(true);
        console.log(id);
    }

    const deleteListingCheck = (id: string) => {
        setListingToBeDeleted(id);
        setShowDeleteModal(true);
    }

    const deleteListing = async () => {
        try {
            let response = await makeRequest(`/carspace/deletecarspace/${username}/${listingToBeDeleted}`, "DELETE", undefined, { token });
            if (response.status !== 200) {
                setShowNotification(true)
                setTimeout(() => {setShowNotification(false)}, 5000);
            } else {
                setTriggerRender(triggerRender === true ? false : true);
            }
        } catch (error) {
            console.log(error);
        }

        setListingToBeDeleted('');
        setShowDeleteModal(false);
    }

    const handleCloseBookingsModal = () => setShowBookingsModal(false);
	const handleCloseModal = () => setShowModal(false);
    const handleCloseDeleteModal = () => setShowDeleteModal(false);

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

    const handleSelect = (ranges: any) => {
    setDateRange(ranges.selection);
    }

    return (
        <Container>
            { myListings && Object.entries(myListings).map(([key, value]: [any, any]) => (
                <Container key={key}>
                    <Row className="align-items-center" style={{ border:'1px solid black', borderRadius: '8px', padding: '10px 10px 10px 0px' }}>
                        <Col md="auto">
                            <img src={value["Your Car Space Information"] && value["Your Car Space Information"]["image"]} style={{ width: '150px', height: '150px' }}/>
                        </Col>
                        <Col className="text-center">
                            <span style={{ fontSize: '35pt' }}>${value["Your Car Space Information"] && value["Your Car Space Information"]["price"]}</span> <br />
                            <span><i>per day</i></span>
                        </Col>
                        <Col >
                            <span style={{ fontSize: '15pt' }}>📍 {value["Your Car Space Information"] && value["Your Car Space Information"]["suburb"]}</span> <br />
                            <span style={{ fontSize: '15pt' }}>📏 {value["Your Car Space Information"] && Math.ceil(parseFloat(value["Your Car Space Information"]["width"]))} m by {value["Your Car Space Information"] && Math.ceil(parseFloat(value["Your Car Space Information"]["breadth"]))} m</span><br />
                            <span style={{ fontSize: '15pt' }}>🚗 {value["Your Car Space Information"] && value["Your Car Space Information"]["vehiclesize"].replace(/^\w/, (c: string) => c.toUpperCase())}</span>
                        </Col>
                        <Col className="text-center" md="auto">
                            <Row>
                                <Button variant='warning' style={{ width: '100px' }} onClick={() => bookingListingCheck(value["Your Car Space Information"]["carspaceid"])}>bookings</Button>
                            </Row><br />
                            <Row>
                                <Button style={{ width: '100px' }} onClick={() => updateListingCheck(value["Your Car Space Information"]["carspaceid"])}>edit</Button>
                            </Row><br />
                            <Row>
                                <Button variant='danger' style={{ width: '100px' }} onClick={() => deleteListingCheck(value["Your Car Space Information"]["carspaceid"])}>delete</Button>
                            </Row>
                        </Col>
                    </Row><br />
                </Container>
            ))}

            <Modal show={showBookingsModal} onHide={handleCloseBookingsModal}>
                <Modal.Header closeButton>
                    <Modal.Title>bookings 📅</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <DateRangePicker dayContentRenderer={renderDayContent} showPreview={false} minDate={new Date()} onChange={handleSelect} ranges={[dateRange]}/>
                </Modal.Body>
            </Modal>

            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>update carspace ✏️</Modal.Title>
                </Modal.Header>
                <ListingComponent username={username} token={token} listing={listingToBeUpdated} allListings={myListings} onClose={handleCloseModal} rerender={() => setTriggerRender(triggerRender === true ? false : true)}></ListingComponent>
            </Modal>

            <Modal show={showDeleteModal} onHide={handleCloseDeleteModal}>
                <Modal.Header closeButton>
                    <Modal.Title>delete carspace 🗑️</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Row className="text-center">
                        <span>Are you sure you want to delete this carspace listing?</span><br /><br />
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
            {showNotification && 
            <NotificationBox variant='danger' title='🚫 Listing Error' message='You cannot delete this listing. There are future bookings!' ></NotificationBox>
            }
        </Container>
    )
}