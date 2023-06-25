import React from 'react';
import { host, makeRequest } from '../helpers';
import '../styling/Login.css'; // Import the CSS file
import logo from '../images/logo.png';
import { Navigate, Route, Routes, Link, useNavigate } from 'react-router-dom';
import { LoginFormField } from '../Types/Authentication';

export const Login = (props: any) => {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');

  const navigate = useNavigate();

  const loginBtn = async () => {
    props.setTokenFn('test');
    // localStorage.setItem('token', 'test');
    navigate('/');
    // try {
    //   if (username === '' || password === '') {
    //     alert('Username and password cannot be empty');
    //     return;
    //   }
    //   const url = host + '/user/auth/register';
    //   const method = 'POST';
    //   const headers = {
    //     Accept: 'application/json',
    //     'Content-Type': 'application/json',
    //   };

    //   const body = JSON.stringify({
    //     username: username,
    //     password: password,
    //   });

    //   const data = await makeRequest(url, method, headers, body);

    //   if (data.error) {
    //     alert(data.error);
    //   } else {
    //     console.log(data);
    //     console.log(data.token);
    //     console.log('token', data.token);
    //     // props.setTokenFn(data.token);
    //     // localStorage.setItem('token', data.token);
    //     // history.push('/');
    //   }
    // } catch (error) {
    //   console.error('Error:', error);
    // }
  };

  const loginFormFields: LoginFormField[] = [
    {
      placeholder: 'Username',
      value: username,
      inputType: 'text',
      onChange: (event) => setUsername(event.target.value),
    },
    {
      placeholder: 'Password',
      value: password,
      inputType: 'text',
      onChange: (event) => setPassword(event.target.value),
    },
  ];

  return (
    <div className="login-page">
      <div className="login-form">
        <div className="image-container">
          <img src={logo}></img>
        </div>
        <div>Login: </div>
        <br></br>
        {loginFormFields.map((field: LoginFormField, index: number) => (
          <React.Fragment key={index}>
            <input
              type={field.inputType}
              placeholder={field.placeholder}
              value={field.value}
              onChange={field.onChange}
            />
          </React.Fragment>
        ))}

        <button onClick={loginBtn}>Login</button>
      </div>
    </div>
  );
};

export default Login;
