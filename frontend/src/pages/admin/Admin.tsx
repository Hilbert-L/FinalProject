import { Container, Tab, Tabs } from "react-bootstrap"
import { AdminHeader } from "./AdminHeader"
import { AdminUsers } from "./AdminUsers"

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
            <div>listings</div>
          </Tab>
        </Tabs>
      </Container>
    </>
  )
}