import React, { useState } from 'react';
import logo from '../images/logo.png';
import { RegistrationFormField } from '../Types/Authentication';
import '../styling/register.css';
import { useNavigate } from 'react-router-dom';
import { FormContainer } from '../components/StyledFormContainer';
import { Button, FloatingLabel, Form } from 'react-bootstrap';
import { StyledLink } from '../components/StyledLink';

type UserInfo = {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  password: string;
  repeatPassword: string;
}

export const Register = () => {
  const [info, setInfo] = useState<UserInfo>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    repeatPassword: '',
  });

  const navigate = useNavigate();

  const handleRegister = () => {
    console.log(info);
    localStorage.setItem("authToken", "logged-in");
    navigate("/");
  }

  return (
    <FormContainer>
      <div style={{textAlign: "center", margin: "30px"}}>
        <img src={logo} style={{ width: "200px", height: "auto" }}/>
      </div>
      <div style={{ margin: "30px 15px" }}>
        <FloatingLabel controlId="floatingFirstName" label="First name" className="mb-3">
          <Form.Control
            type="text"
            placeholder="First name"
            value={info.firstName}
            onChange={(event) => setInfo({...info, firstName: event.target.value})} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingLastName" label="Last name" className="mb-3">
          <Form.Control
            type="text"
            placeholder="Last name"
            value={info.lastName}
            onChange={(event) => setInfo({...info, lastName: event.target.value})} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingEmail" label="Email" className="mb-3">
          <Form.Control
            type="email"
            placeholder="Email"
            value={info.email}
            onChange={(event) => setInfo({...info, email: event.target.value})} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingPhone" label="Phone" className="mb-3">
          <Form.Control
            type="text"
            placeholder="Phone"
            value={info.phone}
            onChange={(event) => setInfo({...info, phone: event.target.value})} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingPassword" label="Password" className="mb-3">
          <Form.Control
            type="password"
            placeholder="Password"
            value={info.password}
            onChange={(event) => setInfo({...info, password: event.target.value})} />
        </FloatingLabel>
        <FloatingLabel controlId="floatingRepeatPassword" label="Repeat password" className="mb-3">
          <Form.Control
            type="password"
            placeholder="Repeat password"
            value={info.repeatPassword}
            onChange={(event) => setInfo({...info, repeatPassword: event.target.value})} />
        </FloatingLabel>
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleRegister}>Register</Button>
        </div>
        <div style={{ paddingTop: "20px", textAlign: "center" }}>
          <StyledLink onClick={() => navigate("/login")}>
            Already a user? Log in here
          </StyledLink>
        </div>
      </div>
    </FormContainer>
  );
};
