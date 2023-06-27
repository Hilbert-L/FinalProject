import { useEffect, useState } from 'react';
import logo from '../images/logo.png';
import { useNavigate } from 'react-router-dom';
import { FormContainer } from '../components/StyledFormContainer';
import { Button, FloatingLabel, Form } from 'react-bootstrap';
import { StyledLink } from '../components/StyledLink';
import { makeRequest } from '../helpers';

type UserInfo = {
  firstName: string;
  lastName: string;
  userName: string;
  email: string;
  phone: string;
  password: string;
  repeatPassword: string;
}

export const Register = () => {
  const [info, setInfo] = useState<UserInfo>({
    firstName: '',
    lastName: '',
    userName: '',
    email: '',
    phone: '',
    password: '',
    repeatPassword: '',
  });

  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    // redirect to home page if logged in
    if (localStorage.getItem("authToken")) {
      navigate("/");
    }
  }, []);

  const handleRegister = async () => {
    if (info.password !== info.repeatPassword) {
      setError("Passwords do not match");
      return;
    }
    try {
      const body = {
        firstname: info.firstName,
        lastname: info.lastName,
        username: info.userName,
        email: info.email,
        password: info.password,
        phonenumber: info.phone,
      };
      const response = await makeRequest("/user/auth/register", "POST", body);
      if (response.status === 200) {
        localStorage.setItem("authToken", "logged-in");
        navigate("/");
      } else {
        setError(
          Array.isArray(response.resp.detail)
            ? response.resp.detail[0].msg  // bad email format
            : response.resp.detail         // other kinds of errors
        );
      }
    } catch(e) {
      console.log(e)
      setError("Something went wrong");
    }
  }

  const allFilledOut = info.firstName
    && info.lastName
    && info.userName
    && info.email
    && info.phone
    && info.password
    && info.repeatPassword

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
        <FloatingLabel controlId="floatingUserName" label="Username" className="mb-3">
          <Form.Control
            type="text"
            placeholder="Username"
            value={info.userName}
            onChange={(event) => setInfo({...info, userName: event.target.value})} />
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
        {error && <span style={{ color: "#D7504D", fontSize: "14px" }}>{error}</span>}
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleRegister}
            disabled={!allFilledOut}
          >Register</Button>
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
