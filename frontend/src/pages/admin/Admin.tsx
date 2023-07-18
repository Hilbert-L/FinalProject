import { Container, Tab, Tabs } from "react-bootstrap"
import { AdminHeader } from "./AdminHeader"
import { AdminUsers } from "./AdminUsers"
import { AdminListings } from "./AdminListings"

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
            <div>bookings</div>
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