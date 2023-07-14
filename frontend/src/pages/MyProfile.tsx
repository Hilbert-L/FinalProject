import React, { useEffect, useState } from 'react';
import { Container, Row, Nav, Spinner, Tab, Tabs } from 'react-bootstrap';
import { MyDetails } from "./MyDetails";
import { MyListings } from "./MyListings";
import { MyBookings } from "./MyBookings";
import { makeRequest } from '../helpers';


export const MyProfile = () => {

  const [username, setUsername] = useState('');
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    async function retrieveUserInfo() {
      let token = localStorage.getItem('authToken') || '';
      let response = await makeRequest("/user/get_current_user", "GET", undefined, { token });
      let profileInfo = response.resp['User Info'];
      setUsername(profileInfo.username)
      setIsLoaded(true);
    }
    retrieveUserInfo();
  }, []);

  if (!isLoaded) {
    return (
      <Container className="text-center">
        <br />
        <br />
        <br />
        <Spinner animation="grow" variant="dark" />
      </Container>
    )
  }

  return (
    <Container>
      <br />
      <Row className="text-center">
        <h1>{username}'s profile 😎</h1>
      </Row>
      <br />
      <Row>
        <Tabs fill defaultActiveKey="details">
          <Tab eventKey="details" title="my details">
            <br />
            <MyDetails />
          </Tab>
          <Tab eventKey="listings" title="my listings">
            <br />
            <MyListings />
          </Tab>
          <Tab eventKey="bookings" title="my bookings">
            <br />
            <MyBookings />
          </Tab>
        </Tabs>
      </Row>
    </Container>
  )
}

// export const MyProfile = (props: any) => {
//                 <Form.Text className="text-muted">Please enter a 3-digit number.</Form.Text>
//   // These will initialised as whatever we get back from the API call



//   // Checks for changes in input then updates state variable
//   const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//     if (modalContent === 'photo') {
//       // Check that user actually uploaded something
//       if (event.target.files) {
//         setDetailChange(URL.createObjectURL(event.target.files[0]));
//         return;
//       }
//     }
//     // If it's not a photo change, update the text
//     setDetailChange(event.target.value);
//   };

//   // Uses the newly entered details (detailChange) to update the profile elements
//   const handleSave = () => {
//     if (detailChange === null || detailChange === '' || detailChange === ' ') {
//       setShowError(true);
//       setShowModal(false);
//       return;
//     }
//     if (modalContent === 'first name') {
//       setProfile({ ...profile, firstName: detailChange });
//     } else if (modalContent === 'last name') {
//       setProfile({ ...profile, lastName: detailChange });
//     } else {
//       setProfile({ ...profile, [modalContent]: detailChange });
//     }
//     setShowModal(false);

//     let token = localStorage.getItem('authToken') || '';
  
//     if (modalContent === "password") {
//       let body = {
//         'username': username,// WE NEED TO CHANGE THESE FOR THE DEMO
//         "currentPassword": profile.password,// THIS NEEDS TO BE UPDATED TOO
//         "newPassword": detailChange
//       }
//       let headers = {
//         'accept': 'application/json',
//         'token': token,
//         'Content-Type': 'application/json',
//       }
//       makeRequest("/user/change_password", "PUT", body, headers)
//         .then((response) => {
//           if (response.status === 200) {
//             console.log(response.resp);
//             console.log("success!")
//           } else {
//             console.log(response.resp);
//           }
//         }).catch(() => {
//           console.log("Something went wrong");
//         })
//     } else {
//       let body = {
//         'username': username,// WE NEED TO CHANGE THESE FOR THE DEMO
//         "newEmail": profile.email,
//         "newFirstName": profile.firstName,
//         "newLastName": profile.lastName,
//         "newPhoneNumber": 0,
//       }
//       let headers = {
//         'accept': 'application/json',
//         'token': token,
//         'Content-Type': 'application/json',
//       }
//       makeRequest("/user/update_personal_details", "PUT", body, headers)
//         .then((response) => {
//           if (response.status === 200) {
//             console.log(response.resp);
//             console.log("success!")
//           } else {
//             console.log(response.resp);
//           }
//         }).catch(() => {
//           console.log("Something went wrong");
//         })
//     }
//   };

//   const handleClose = () => setShowModal(false);
//   const handleShow = (content: string) => {
//     setShowModal(true);
//     setModalContent(content);
//     setDetailChange('');
//   };

//   return (
//     <div style={container}>
//       <h1>Profile</h1>
//       <div style={profileContainer}>
//         <div style={profilePictureContainer}>
//           <img
//             src={profile.photo}
//             style={{ width: '165px', height: '165px' }}
//             alt="Profile Picture"
//           />
//           <br />
//           <button
//             className="btn btn-primary"
//             onClick={() => handleShow('photo')}
//             type="button"
//             id="button-addon2"
//           >
//             edit profile picture
//           </button>
//         </div>
//         <div style={profileDetailsContainer}>
//           <div className="input-group">
//             <span className="input-group-text">first name</span>
//             <input
//               type="text"
//               aria-label="Full name"
//               value={profile.firstName}
//               className="form-control"
//               disabled
//             />
//             <button
//               className="btn btn-primary"
//               onClick={() => handleShow('first name')}
//               type="button"
//               id="button-addon2"
//             >
//               change
//             </button>
//           </div>
//           <br />
//           <div className="input-group">
//             <span className="input-group-text">last name</span>
//             <input
//               type="text"
//               aria-label="Full name"
//               value={profile.lastName}
//               className="form-control"
//               disabled
//             />
//             <button
//               className="btn btn-primary"
//               onClick={() => handleShow('last name')}
//               type="button"
//               id="button-addon2"
//             >
//               change
//             </button>
//           </div>
//           <br />
//           <div className="input-group">
//             <span className="input-group-text">email</span>
//             <input
//               type="email"
//               aria-label="Full name"
//               value={profile.email}
//               className="form-control"
//               disabled
//             />
//             <button
//               className="btn btn-primary"
//               onClick={() => handleShow('email')}
//               type="button"
//               id="button-addon2"
//             >
//               change
//             </button>
//           </div>
//           <br />
//           <div className="input-group">
//             <span className="input-group-text">password</span>
//             <input
//               type="password"
//               aria-label="Full name"
//               value={profile.password}
//               className="form-control"
//               disabled
//             />
//             <button
//               className="btn btn-primary"
//               onClick={() => handleShow('password')}
//               type="button"
//               id="button-addon2"
//             >
//               change
//             </button>
//           </div>
//         </div>
//       </div>

//       <Modal show={showModal} onHide={handleClose}>
//         <Modal.Header closeButton>
//           <Modal.Title>change {modalContent}</Modal.Title>
//         </Modal.Header>
//         <Modal.Body>
//           {modalContent === 'photo' ? (
//             <>
//               <p>
//                 upload your new <b>photo</b>
//               </p>
//               <input
//                 type="file"
//                 onChange={handleChange}
//                 className="form-control"
//               />
//             </>
//           ) : (
//             <>
//               <p>
//                 type your new <b>{modalContent}</b>
//               </p>
//               <input
//                 type="text"
//                 onChange={handleChange}
//                 className="form-control"
//               />
//             </>
//           )}
//         </Modal.Body>
//         <Modal.Footer>
//           <button className="btn btn-secondary" onClick={handleClose}>
//             Close
//           </button>
//           <button className="btn btn-primary" onClick={handleSave}>
//             Save Changes
//           </button>
//         </Modal.Footer>
//       </Modal>

//       { showError && <div className="alert alert-danger alert-dismissible fade show" style={{position: 'absolute', top: '200px'}} role="alert">
//         <strong>Error!</strong> You can't leave the field empty.
//         <button type="button" className="btn-close" onClick={() => setShowError(false)} data-bs-dismiss="alert" aria-label="Close"></button>
//       </div>
//       }
//     </div>
//   );
// };

