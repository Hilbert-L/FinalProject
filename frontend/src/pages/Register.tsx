import React from 'react';
import logo from '../images/logo.png';
import { makeRequest, host } from '../helpers';
import { RegistrationFormField } from '../Types/Authentication';
import '../styling/register.css';
import { Navigate, Route, Routes, Link, useNavigate } from 'react-router-dom';

export const Register = (props: any) => {
  const [title, setTitle] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [repeatPassword, setRepeatPassword] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [firstname, setFirstname] = React.useState('');
  const [lastname, setLastname] = React.useState('');
  const [phoneNumber, setPhoneNumber] = React.useState('');

  const navigate = useNavigate();

  const registerBtn = async () => {
    props.setTokenFn('test');
    // localStorage.setItem('token', 'test');
    navigate('/');
  };

  const registrationFormFields: RegistrationFormField[] = [
    {
      placeholder: 'Title',
      value: title,
      inputType: 'text',
      onChange: (event) => setTitle(event.target.value),
    },
    {
      placeholder: 'First Name',
      value: firstname,
      inputType: 'text',
      onChange: (event) => setFirstname(event.target.value),
    },
    {
      placeholder: 'Last Name',
      value: lastname,
      inputType: 'text',
      onChange: (event) => setLastname(event.target.value),
    },
    {
      placeholder: 'Username',
      value: username,
      inputType: 'text',
      onChange: (event) => setUsername(event.target.value),
    },
    {
      placeholder: 'Password',
      value: password,
      inputType: 'password',
      onChange: (event) => setPassword(event.target.value),
    },
    {
      placeholder: 'Repeat Password',
      value: repeatPassword,
      inputType: 'password',
      onChange: (event) => setRepeatPassword(event.target.value),
    },
    {
      placeholder: 'Email',
      value: email,
      inputType: 'text',
      onChange: (event) => setEmail(event.target.value),
    },
    {
      placeholder: 'Phone Number',
      value: phoneNumber,
      inputType: 'text',
      onChange: (event) => setPhoneNumber(event.target.value),
    },
  ];

  return (
    <div className="register-page">
      <div className="register-form">
        <div className="image-container">
          <img src={logo}></img>
        </div>
        <div>Fill in Registration Form: </div>
        <br></br>
        {registrationFormFields.map(
          (field: RegistrationFormField, index: number) => (
            <React.Fragment key={index}>
              <input
                type={field.inputType}
                placeholder={field.placeholder}
                value={field.value}
                onChange={field.onChange}
              />
            </React.Fragment>
          )
        )}
        <button onClick={registerBtn}>Register</button>
      </div>
    </div>
  );
};
