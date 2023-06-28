import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import { Modal } from 'react-bootstrap';
import { makeRequest } from '../helpers';

interface Profile {
  name: string;
  email: string;
  password: string;
  photo: string;
}

export const MyProfile = (props: any) => {
  const container: React.CSSProperties = {
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '15px',
  };

  const profileContainer: React.CSSProperties = {
    width: '95%',
    maxWidth: '900px',
    border: '2px solid black',
    padding: '40px 0px',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    borderRadius: '10px',
  };

  const profilePictureContainer: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
  };

  const profileDetailsContainer: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
  };

  // These will initialised as whatever we get back from the API call
  const [profile, setProfile] = useState<Profile>({
    name: 'Osman Catal',
    email: 'osman@email.com',
    password: 'osman123',
    photo: '',
  });

  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState('');
  const [detailChange, setDetailChange] = useState('');
  const [showError, setShowError] = useState(false);

  // Checks for changes in input then updates state variable
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (modalContent === 'photo') {
      // Check that user actually uploaded something
      if (event.target.files) {
        setDetailChange(URL.createObjectURL(event.target.files[0]));
        return;
      }
    }
    // If it's not a photo change, update the text
    setDetailChange(event.target.value);
  };

  // Uses the newly entered details (detailChange) to update the profile elements
  const handleSave = () => {
    if (detailChange === null || detailChange === '' || detailChange === ' ') {
      setShowError(true);
      setShowModal(false);
      return;
    }
    setProfile({ ...profile, [modalContent]: detailChange });
    setShowModal(false);
    console.log(detailChange)

    let token = localStorage.getItem('authToken') || '';
  
    if (modalContent === "password") {
      let body = {
        'username': "osman123",// WE NEED TO CHANGE THESE FOR THE DEMO
        "currentPassword": "osman",// THIS NEEDS TO BE UPDATED TOO
        "newPassword": detailChange
      }
      let headers = {
        'accept': 'application/json',
        'token': token,
        'Content-Type': 'application/json',
      }
      makeRequest("/user/change_password", "PUT", body, headers)
        .then((response) => {
          if (response.status === 200) {
            console.log(response.resp);
            console.log("success!")
          } else {
            console.log(response.resp);
          }
        }).catch(() => {
          console.log("Something went wrong");
        })
    } else {
      let body = {
        'username': "osman123",// WE NEED TO CHANGE THESE FOR THE DEMO
        "newEmail": detailChange,
        "newTitle": "user@example.com",
        "newFirstName": "hey",
        "newLastName": "hey",
        "newProfilePic": "hey"
      }
      let headers = {
        'accept': 'application/json',
        'token': token,
        'Content-Type': 'application/json',
      }
      makeRequest("/user/update_personal_details", "PUT", body, headers)
        .then((response) => {
          if (response.status === 200) {
            console.log(response.resp);
            console.log("success!")
          } else {
            console.log(response.resp);
          }
        }).catch(() => {
          console.log("Something went wrong");
        })
    }
  };

  const handleClose = () => setShowModal(false);
  const handleShow = (content: string) => {
    setShowModal(true);
    setModalContent(content);
    setDetailChange('');
  };

  return (
    <div style={container}>
      <h1>Profile</h1>
      <div style={profileContainer}>
        <div style={profilePictureContainer}>
          <img
            src={profile.photo}
            style={{ width: '165px', height: '165px' }}
            alt="Profile Picture"
          />
          <br />
          <button
            className="btn btn-primary"
            onClick={() => handleShow('photo')}
            type="button"
            id="button-addon2"
          >
            edit profile picture
          </button>
        </div>
        <div style={profileDetailsContainer}>
          <div className="input-group">
            <span className="input-group-text">name</span>
            <input
              type="text"
              aria-label="Full name"
              value={profile.name}
              className="form-control"
              disabled
            />
            <button
              className="btn btn-primary"
              onClick={() => handleShow('name')}
              type="button"
              id="button-addon2"
            >
              change
            </button>
          </div>
          <br />
          <div className="input-group">
            <span className="input-group-text">email</span>
            <input
              type="email"
              aria-label="Full name"
              value={profile.email}
              className="form-control"
              disabled
            />
            <button
              className="btn btn-primary"
              onClick={() => handleShow('email')}
              type="button"
              id="button-addon2"
            >
              change
            </button>
          </div>
          <br />
          <div className="input-group">
            <span className="input-group-text">password</span>
            <input
              type="password"
              aria-label="Full name"
              value={profile.password}
              className="form-control"
              disabled
            />
            <button
              className="btn btn-primary"
              onClick={() => handleShow('password')}
              type="button"
              id="button-addon2"
            >
              change
            </button>
          </div>
        </div>
      </div>

      <Modal show={showModal} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>change {modalContent}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {modalContent === 'photo' ? (
            <>
              <p>
                upload your new <b>photo</b>
              </p>
              <input
                type="file"
                onChange={handleChange}
                className="form-control"
              />
            </>
          ) : (
            <>
              <p>
                type your new <b>{modalContent}</b>
              </p>
              <input
                type="text"
                onChange={handleChange}
                className="form-control"
              />
            </>
          )}
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-secondary" onClick={handleClose}>
            Close
          </button>
          <button className="btn btn-primary" onClick={handleSave}>
            Save Changes
          </button>
        </Modal.Footer>
      </Modal>

      { showError && <div className="alert alert-danger alert-dismissible fade show" style={{position: 'absolute', top: '200px'}} role="alert">
        <strong>Error!</strong> You can't leave the field empty.
        <button type="button" className="btn-close" onClick={() => setShowError(false)} data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
      }
    </div>
  );
};

// eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im9zbWFuMTIzIn0.6RRMM5GOiywaGqq8Y40QBRxxquYqQR4A0_SipgNIpNQ