import { PropsWithChildren, useState, useEffect } from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Outlet, useNavigate } from 'react-router-dom';
import { makeRequest } from '../helpers';
import { NotificationBox } from '../components/NotificationBox';

export const Layout = ({ children }: PropsWithChildren<{}>) => {
  const navigate = useNavigate();
  const token = localStorage.getItem("authToken");
  const [showNotification, setShowNotification] = useState(false);

  // Used to log the user out, clears the authtoken
  const handleLogout = () => {
    if (!token) return;
    makeRequest("/user/auth/logout", "POST", undefined, { token })
      .then((response) => {
        if (response.status === 200) {
          localStorage.removeItem("authToken");
          navigate("/login");
        }
      });
  }

  // Checks if the user has had any of their car spaces booked
  useEffect(() => {
    async function checkForBookings() {
      let reservations = localStorage.getItem("reservations");
      try {
        const response = await makeRequest("/user/get_current_reservations", "GET", undefined, { token })
        if (response.status !== 200) {
          console.log(response.resp)
        } 
        // If there is a new booking, update the value in local storage and show the notification
        if (response.resp['Reservation Count'] > parseInt(reservations, 10)) {
          localStorage.setItem("reservations", response.resp['Reservation Count']);
          setShowNotification(true)
          setTimeout(() => {setShowNotification(false)}, 5000);
        }
      } catch (error) {
        console.log(error)
      }
    }
    // Repeat the check every 10 seconds
    const interval = setInterval(checkForBookings, 10000);

    // Clean up the interval when the component unmounts to avoid memory leaks
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div>
      <Navbar expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="#" onClick={() => navigate("/")}>Care Space Renting System</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link onClick={() => navigate("/profile")}>My Profile</Nav.Link>
              <Nav.Link onClick={() => navigate("/listingform")}>Add Listing</Nav.Link>
              <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {children}
      <Outlet />
      { showNotification &&
      <NotificationBox title={'New reservation'} message={'Someone has booked one of your carspace listings!'}></NotificationBox>
      }
    </div>
  );
}
