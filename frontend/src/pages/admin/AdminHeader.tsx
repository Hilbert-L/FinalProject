import { Container, Nav, Navbar } from "react-bootstrap"
import { useNavigate } from "react-router-dom";
import { makeRequest } from "../../helpers";

export const AdminHeader = () => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest("/admin/auth/logout", "POST", undefined, { token })
      .then((response) => {
        if (response.status === 200) {
          localStorage.removeItem("adminToken");
          navigate("/login/admin");
        }
      });
  }

  return (
    <div>
      <Navbar expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="#" onClick={() => navigate("/")}>Car Space</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  )
}