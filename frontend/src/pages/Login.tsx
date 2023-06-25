import { useState } from 'react';
import logo from '../images/logo.png';
import { useNavigate } from 'react-router-dom';
import { Button, FloatingLabel, Form } from 'react-bootstrap';
import { StyledLink } from '../components/StyledLink';
import { FormContainer } from '../components/StyledFormContainer';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const handleLogin = () => {
    // TODO: actually send email and password to server for authentication
    console.log(email);
    console.log(password);
    localStorage.setItem("authToken", "logged-in");
    navigate("/");
  }

  return (
    <FormContainer>
      <div style={{textAlign: "center", margin: "30px"}}>
        <img src={logo} style={{ width: "200px", height: "auto" }}/>
      </div>
      <div style={{ margin: "30px 15px" }}>
        <FloatingLabel controlId="floatingEmail" label="Email" className="mb-3">
          <Form.Control
            type="email"
            placeholder="Email"
            value={email}
            onChange={(event) => setEmail(event.target.value)} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingPassword" label="Password" className="mb-3">
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)} />
        </FloatingLabel>
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleLogin}>Log In</Button>
        </div>
        <div style={{ paddingTop: "20px", textAlign: "center" }}>
          <StyledLink onClick={() => navigate("/register")}>
            Not a user yet? Register here
          </StyledLink>
        </div>
      </div>
    </FormContainer>
  );
};
