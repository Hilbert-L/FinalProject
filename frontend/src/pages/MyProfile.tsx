import React, { useEffect, useState } from 'react';
import { Container, Row, Nav, Spinner, Tab, Tabs } from 'react-bootstrap';
import { MyDetails } from "./MyDetails";
import { MyPaymentDetails } from "./MyPaymentDetails";
import { MyListings } from "./MyListings";
import { MyBookings } from "./MyBookings";
import { makeRequest } from '../helpers';


export const MyProfile = () => {

  const [username, setUsername] = useState('');
  const [isLoaded, setIsLoaded] = useState(false);

  // Gets the user's information and sets it in the state variable
  useEffect(() => {
    async function retrieveUserInfo() {
      let token = localStorage.getItem('authToken') || '';
      let response = await makeRequest("/user/get_current_user", "GET", undefined, { token });
      let profileInfo = response.resp['User Info'];
      setUsername(profileInfo.username)
      setIsLoaded(true);
    }
    retrieveUserInfo();
  }, []);

  // Displays a spinner until the page loads
  if (!isLoaded) {
    return (
      <Container className="text-center">
        <br />
        <br />
        <br />
        <Spinner animation="grow" variant="dark" />
      </Container>
    )
  }

  return (
    <Container>
      <br />
      <Row className="text-center">
        <h1>{username}'s profile 😎</h1>
      </Row>
      <br />
      <Row>
        <Tabs fill defaultActiveKey="details">
          <Tab eventKey="details" title="my details">
            <br />
            <MyDetails />
          </Tab>
          <Tab eventKey="bank" title="payment details">
            <br />
            <MyPaymentDetails username={username}/>
          </Tab>
          <Tab eventKey="listings" title="my listings">
            <br />
            <MyListings username={username}/>
          </Tab>
          <Tab eventKey="bookings" title="my bookings">
            <br />
            <MyBookings />
          </Tab>
        </Tabs>
      </Row>
    </Container>
  )
}