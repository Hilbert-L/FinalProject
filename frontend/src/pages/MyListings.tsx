import { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Modal } from 'react-bootstrap';
import { makeRequest } from '../helpers';
import { DateRangePicker } from 'react-date-range';
import { ListingComponent } from '../components/ListingComponent';
import { NotificationBox } from '../components/NotificationBox';

interface TimeRange {
    start_time: string;
    end_time: string;
  }

export const MyListings = (props: any) => {

    const username = props.username;
    let token = localStorage.getItem('authToken') || '';
    const [myListings, setMyListings] = useState([{}]);
    const [showBookingsModal, setShowBookingsModal] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [listingToBeUpdated, setListingToBeUpdated] = useState('');
    const [listingToBeDeleted, setListingToBeDeleted] = useState('');
    const [triggerRender, setTriggerRender] = useState(true);
    const [currentReservations, setCurrentReservations] = useState([new Date]);
    const [showNotification, setShowNotification] = useState(false);
    const [dateRange, setDateRange] = useState({
        startDate: new Date(),
        endDate: new Date(),
        key: 'selection',
      });

    useEffect(() => {
        // Retrieves car spaces given that the user has posted
		async function retrieveListings() {
			try {
				let response = await makeRequest(`/carspace/get_car_space_Info/${username}`, "GET", undefined, { token });
				if (response.status !== 200) {
					console.log("There was an error!")
				} else {
					let listings = response.resp;
                    // Store the listings in a state variable
                    setMyListings(listings);
                    return listings;
				}
			} catch (error) {
				console.log(error);
			}
			return 0;
		}
        retrieveListings();
    }, [triggerRender]);

    // Extracts all the dates between the given start and end dates
    const extractDatesBetween = (data: TimeRange[]): string[] => {
        const result: string[] = [];
        data.forEach(({ start_time, end_time }) => {
          const startDate = new Date(start_time);
          const endDate = new Date(end_time);
          const currentDate = new Date(startDate);
      
          // Loops through the dates until all the dates are covered
          while (currentDate <= endDate) {
            result.push(new Date(`${currentDate.getMonth() + 1}/${currentDate.getDate()}/${currentDate.getFullYear()}`).toLocaleDateString());
            currentDate.setDate(currentDate.getDate() + 1);
          }
        });
        return result;
      };

    // Retrieves all the reservations for the given carspace
    const bookingListingCheck = async (id: string) => {
        let reservations = await makeRequest(`/carspace/get_car_space_booking/${id}`, "GET", undefined, { token });
        // Extracts all the dates between the reservation dates
        let allDates = extractDatesBetween(reservations.resp);
        let allDatesList = [new Date];
        // For each date, extracts the day, month and year
        allDates.forEach((dateString) => {
            const parts = dateString.split('/');
            const month = parseInt(parts[1], 10) - 1;
            const day = parseInt(parts[0], 10);
            const year = parseInt(parts[2], 10);
            // Creates a new date object and adds it to the list
            const dateObject = new Date(year, month, day);
            allDatesList.push(dateObject);
            });
        setCurrentReservations(allDatesList);
        setShowBookingsModal(true);
    }

    // Sets the id for the listing to be updated and shows the modal
    const updateListingCheck = (id: string) => {
        setListingToBeUpdated(id);
        setShowModal(true);
    }

    // Sets the id for the listing to be deleted and shows the modal
    const deleteListingCheck = (id: string) => {
        setListingToBeDeleted(id);
        setShowDeleteModal(true);
    }

    // Sends a request to delete a given listing
    const deleteListing = async () => {
        try {
            let response = await makeRequest(`/carspace/deletecarspace/${username}/${listingToBeDeleted}`, "DELETE", undefined, { token });
            if (response.status !== 200) {
                // Set the notification to show for 5 seconds if there is an error
                setShowNotification(true)
                setTimeout(() => {setShowNotification(false)}, 5000);
            } else {
                // Otherwise rerender the page
                setTriggerRender(triggerRender === true ? false : true);
            }
        } catch (error) {
            console.log(error);
        }
        // Reset the state variables
        setListingToBeDeleted('');
        setShowDeleteModal(false);
    }

    // Handle closing the modals
    const handleCloseBookingsModal = () => setShowBookingsModal(false);
	const handleCloseModal = () => setShowModal(false);
    const handleCloseDeleteModal = () => setShowDeleteModal(false);

    // A function used to check if two given dates are the same
    function isSameDay(date1: any, date2: any) {
        return (
          date1.getDate() === date2.getDate() &&
          date1.getMonth() === date2.getMonth() &&
          date1.getFullYear() === date2.getFullYear()
        );
      }

    // Used to render the days on the calendar using a given style
    function renderDayContent(day: any) {

        const disabledDays = currentReservations;
      
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

            <Modal size="lg" show={showBookingsModal} onHide={handleCloseBookingsModal}>
                <Modal.Header closeButton>
                    <Modal.Title>bookings 📅</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Col className="text-center">
                        <DateRangePicker dayContentRenderer={renderDayContent} showPreview={false} minDate={new Date()} onChange={handleSelect} ranges={[dateRange]}/>
                    </Col>
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