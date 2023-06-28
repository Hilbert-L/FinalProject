import { useEffect, useState } from 'react';
import logo from '../images/logo.png';
import { useNavigate } from 'react-router-dom';
import { Button, FloatingLabel, Form } from 'react-bootstrap';
import { StyledLink } from '../components/StyledLink';
import { FormContainer } from '../components/StyledFormContainer';
import { makeRequest } from '../helpers';

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    // redirect to home page if logged in
    if (localStorage.getItem("authToken")) navigate("/");
  }, []);

  const handleLogin = () => {
    makeRequest("/user/auth/login", "POST", { username, password })
      .then((response) => {
        if (response.status === 200) {
          localStorage.setItem("authToken", response.resp.token);
          navigate("/");
        } else {
          setError(response.resp.detail);
          console.log(response.resp);
        }
      }).catch(() => {
        console.log("Something went wrong");
      })
  }

  const allFilledOut = username && password

  return (
    <FormContainer>
      <div style={{textAlign: "center", margin: "30px"}}>
        <img src={logo} style={{ width: "200px", height: "auto" }}/>
      </div>
      <div style={{ margin: "30px 15px" }}>
        <FloatingLabel controlId="floatingUserName" label="Username" className="mb-3">
          <Form.Control
            type="text"
            placeholder="Username"
            value={username}
            onChange={(event) => setUsername(event.target.value)} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingPassword" label="Password" className="mb-3">
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)} />
        </FloatingLabel>
        {error && <span style={{ color: "#D7504D", fontSize: "14px" }}>{error}</span>}
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleLogin}
            disabled={!allFilledOut}
          >Log In</Button>
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
