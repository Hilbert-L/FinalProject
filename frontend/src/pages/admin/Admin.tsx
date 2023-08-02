import { Container, Tab, Tabs } from "react-bootstrap"
import { AdminHeader } from "./AdminHeader"
import { AdminUsers } from "./AdminUsers"
import { AdminListings } from "./AdminListings"
import { AdminBookings } from "./AdminBookings"

export const Admin = () => {
  return (
    <>
      <AdminHeader />
      <Container>
        <br />
        <Tabs fill defaultActiveKey="users">
          <Tab eventKey="users" title="Users">
            <br />
            <AdminUsers />
          </Tab>
          <Tab eventKey="bookings" title="Bookings">
            <br />
            <AdminBookings />
          </Tab>
          <Tab eventKey="listings" title="Listings">
            <br />
            <AdminListings />
          </Tab>
        </Tabs>
      </Container>
    </>
  )
}