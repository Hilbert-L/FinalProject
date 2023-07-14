import React, { useEffect, useState } from 'react';
import { Container, Row, Col, InputGroup, Form, Button, Modal, OverlayTrigger, Tooltip, Spinner } from 'react-bootstrap';
import { makeRequest } from '../helpers';

interface Profile {
    firstName?: string;
    lastName?: string;
    email?: string;
    password?: string;
    photo?: string;
  }

// TODO
// Add error messages + validation

export const MyDetails = () => {

	let token = localStorage.getItem('authToken') || '';

	const [isLoaded, setIsLoaded] = useState(false);
	const [profile, setProfile] = useState<Profile>({});
	const [modalState, setModalState] = useState('password');
	const [showModal, setShowModal] = useState(false);
	const [username, setUsername] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [triggerRender, setTriggerRender] = useState(true);

	// State variables for all of the possible profile changes
	const [firstNameChange, setFirstNameChange] = useState('');
	const [lastNameChange, setLastNameChange] = useState('');
	const [emailChange, setEmailChange] = useState('');
	const [currentPassword, setCurrentPassword] = useState('');
	const [passwordChange, setPasswordChange] = useState('');
	const [photoChange, setPhotoChange] = useState('');
	const [BSBChange, setBSBChange] = useState('');
	const [accountNumberChange, setAccountNumberChange] = useState('');
	
	useEffect(() => {
		async function retrieveUserInfo() {
			let token = localStorage.getItem('authToken') || '';
			let response = await makeRequest("/user/get_current_user", "GET", undefined, { token });
			let profileInfo = response.resp['User Info'];
			setUsername(profileInfo.username)
			const base64Data = btoa(profileInfo.profileImagedata); // Needs work
			const image = `data:image/jpeg;base64,${base64Data}`;
			setProfile(profile => ({
				...profile,
				firstName: profileInfo.firstname,
				lastName: profileInfo.lastname,
				email: profileInfo.email,
				password: profileInfo.passwordunhashed,
				photo: image,
			}));
			setIsLoaded(true);
		}
		retrieveUserInfo();
	}, [triggerRender]);

	// Handles showing the modal
	const handleShow = (type: string) => {
		setModalState(type);
		setShowModal(true)
	};

	// Handles closing the modal
	const handleClose = () => setShowModal(false);

	// Handles changing profile details
	const handleDetailChange = () => {
		async function uploadDetails() {
			let body = {
					"username": username,
					"newEmail": emailChange,
					"newFirstName": firstNameChange,
					"newLastName": lastNameChange,
					"newPhoneNumber": "0",
			}
			try {
				const response = await makeRequest("/user/update_personal_details", "PUT", body, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp.detail[0].msg);
					// console.log(response)
				} 
			} catch (error) {
				console.log(error)
			}
		}
		uploadDetails();
		setTriggerRender(triggerRender === true ? false : true);
		setShowModal(false);
	}

	// Handles changing password
	const handlePasswordChange = () => {
		async function uploadPassword() {
			let body = {
					"username": username,
					"currentPassword": currentPassword,
					"newPassword": passwordChange,
			}
			try {
				const response = await makeRequest("/user/change_password", "PUT", body, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp.detail[0].msg);
				} 
			} catch (error) {
				console.log(error)
			}
		}
		uploadPassword();
		setTriggerRender(triggerRender === true ? false : true);
		setShowModal(false);
	}

	// TODO
	// API not working
	// Handles changing bank details
	const handleBankChange = () => {
		async function uploadBank() {
			let body = {
					"username": username,
					"id": 0,
					"newbankaccount": {
						"bsb": BSBChange,
						"accountnumber": accountNumberChange,
						"expiry_date": "",
						"ccv": ""
					}
			}
			try {
				const response = await makeRequest("/user/add_bank_account", "PUT", body, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp.detail[0].msg);
				} 
			} catch (error) {
				console.log(error)
			}
		}
		uploadBank();
		setTriggerRender(triggerRender === true ? false : true);
		setShowModal(false);
	}
	
	// Takes the photo input the user uploaded
	// TODO
	// Validation
	const uploadPhoto = (event: any) => {
		if (event.target.files) {
			const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        setPhotoChange(base64String);
      };
      reader.readAsDataURL(event.target.files[0]);
    }
	}

	// Handles changing profile picture
	const handlePhotoChange = () => {
		console.log(photoChange);
		async function uploadPhoto() {
			let body = {
					"image": photoChange,
			}
			try {
				const response = await makeRequest("/user/upload_profile_picture", "POST", body, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp.detail[0].msg);
				} 
			} catch (error) {
				console.log(error)
			}
		}
		uploadPhoto();
		setTriggerRender(triggerRender === true ? false : true);
		setShowModal(false);
	}

	const renderTooltip = (props: any) => (
		<Tooltip {...props}>
			change
		</Tooltip>
	);

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
			<Row>
				<Col className="text-center">
					<div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
						<OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }} overlay={renderTooltip}>
							<img src={profile.photo} style={{ width: '250px', height: '250px', borderRadius: '150px', cursor: 'pointer' }} onClick={() => handleShow('photo')}></img>
						</OverlayTrigger>
					</div>
				</Col>
				<Col>
					<InputGroup className="mb-3">
						<InputGroup.Text style={{ width: '100px' }}>first name</InputGroup.Text>
						<Form.Control disabled aria-label="First name" value={profile.firstName}/>
					</InputGroup>
					<InputGroup className="mb-3">
						<InputGroup.Text style={{ width: '100px' }}>last name</InputGroup.Text>
						<Form.Control disabled aria-label="Last name" value={profile.lastName}/>
					</InputGroup>
					<InputGroup className="mb-3">
						<InputGroup.Text style={{ width: '100px' }}>email</InputGroup.Text>
						<Form.Control disabled aria-label="Email" value={profile.email}/>
					</InputGroup>
					<InputGroup className="mb-3">
						<InputGroup.Text style={{ width: '100px' }}>password</InputGroup.Text>
						<Form.Control type="password" disabled aria-label="Password" value={profile.password}/>
					</InputGroup>
					<InputGroup>
						<InputGroup.Text style={{ width: '100px' }}>bank</InputGroup.Text>
						<Form.Control disabled aria-label="Card" value='Hello'/>
					</InputGroup>
				</Col>
			</Row>
			<br />
			<Row className="text-center">
				<Col>
					<Button style={{ width: '180px' }} onClick={() => handleShow('details')}>change details</Button>
				</Col>
				<Col>
					<Button style={{ width: '180px' }} onClick={() => handleShow('password')}>change password</Button>
				</Col>
				<Col>
					<Button style={{ width: '180px' }} onClick={() => handleShow('bank')}>change bank details</Button>
				</Col>
			</Row>

			<Modal show={showModal} onHide={handleClose}>
				<Modal.Header closeButton>
					<Modal.Title>profile change 📝</Modal.Title>
				</Modal.Header>
				<Modal.Body>
					{ modalState === 'details' &&
						<Form>
							<Form.Group className="mb-3">
								<Form.Label>new first name</Form.Label>
								<Form.Control type="text" placeholder={profile.firstName} onChange={(event) => setFirstNameChange(event.target.value)}/>
							</Form.Group>
							<Form.Group className="mb-3">
								<Form.Label>new last name</Form.Label>
								<Form.Control type="text" placeholder={profile.lastName} onChange={(event) => setLastNameChange(event.target.value)}/>
							</Form.Group>
							<Form.Group className="mb-3">
								<Form.Label>new email address</Form.Label>
								<Form.Control type="email" placeholder={profile.email} onChange={(event) => setEmailChange(event.target.value)}/>
							</Form.Group>
							<Button onClick={handleDetailChange}>save changes</Button>
						</Form>
					}
					{ modalState === 'password' &&
						<Form>
							<Form.Group className="mb-3">
								<Form.Label>current password</Form.Label>
								<Form.Control type="password" required onChange={(event) => setCurrentPassword(event.target.value)}/>
							</Form.Group>
							<Form.Group className="mb-3">
								<Form.Label>new password</Form.Label>
								<Form.Control type="password" required onChange={(event) => setPasswordChange(event.target.value)}/>
							</Form.Group>
							<Button onClick={handlePasswordChange}>save changes</Button>
						</Form>
					}
					{ modalState === 'bank' &&
						<Form>
							<Form.Group className="mb-3">
								<Form.Label>new BSB</Form.Label>
								<Form.Control type="number" required onChange={(event) => setBSBChange(event.target.value)}/>
							</Form.Group>
							<Form.Group className="mb-3">
								<Form.Label>new account number</Form.Label>
								<Form.Control type="number" required onChange={(event) => setAccountNumberChange(event.target.value)}/>
							</Form.Group>
							<Button onClick={handleBankChange}>save changes</Button>
						</Form>
					}
					{ modalState === 'photo' &&
						<Form>
							<Form.Group className="mb-3">
								<Form.Label>new profile picture</Form.Label>
								<Form.Control type="file" required onChange={(event) => uploadPhoto(event)}/>
							</Form.Group>
							<Button onClick={handlePhotoChange}>save changes</Button>
						</Form>
					}
				</Modal.Body>
			</Modal>
		</Container>
	)
}