import { PropsWithChildren } from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Outlet, useNavigate } from 'react-router-dom';
import { makeRequest } from '../helpers';

export const Layout = ({ children }: PropsWithChildren<{}>) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    const token = localStorage.getItem("authToken");
    if (!token) return;
    makeRequest("/user/auth/logout", "POST", undefined, { token })
      .then((response) => {
        if (response.status === 200) {
          localStorage.removeItem("authToken");
          navigate("/login");
        }
      });
  }

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
    </div>
  );
}
