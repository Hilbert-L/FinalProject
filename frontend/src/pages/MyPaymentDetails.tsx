import React, { useEffect, useState } from 'react';
import { Container, Row, Col, InputGroup, Form, Button, Modal, OverlayTrigger, Tooltip, Spinner } from 'react-bootstrap';
import { makeRequest } from '../helpers';

interface Payment {
    bsb?: string;
    accountNumber?: string;
    cardNumber?: string;
    cardExpiry?: string;
  }

export const MyPaymentDetails = (props: any) => {

    const username = props.username;
    
    let token = localStorage.getItem('authToken') || '';
    const [showModal, setShowModal] = useState(false);
    const [modalState, setModalState] = useState('');
    const [detailsExist, setDetailsExist] = useState(false);
    const [triggerRender, setTriggerRender] = useState(true);
    const [paymentDetails, setPaymentDetails] = useState<Payment>({});
	const [errorMessage, setErrorMessage] = useState('');
    const [bsbCheck, setBSBCheck] = useState(false);
    const [accountNumberCheck, setAccountNumberCheck]= useState(false);
    const [cardNumberCheck, setCardNumberCheck] = useState(false);
    const [cardExpiryCheck, setCardExpiryCheck] = useState(false);
    const [buttonDisabled, setButtonDisabled] = useState(true);
    const [fundsAmount, setFundsAmount] = useState(0);
    const [addFundsAmount, setAddFundsAmount] = useState(0);
    const [withdrawFundsAmount, setWithdrawFundsAmount] = useState(0);

    // State variables for all of the possible payment detail changes
    const [BSBChange, setBSBChange] = useState('');
    const [accountNumberChange, setAccountNumberChange] = useState('');
    const [cardNumberChange, setCardNumberChange] = useState('');
    const [cardExpiryChange, setCardExpiryChange] = useState('');

    // Used to initially retrieve a user's bank details
    useEffect(() => {
		async function retrieveUserBankDetails() {
			let token = localStorage.getItem('authToken') || '';
            try {
                let response = await makeRequest(`/bankaccounts/get_bank_account/${username}`, "GET", undefined, { token });
                if (response.status !== 200) return;
                let userInfo = (response.resp[`bank accounts for user: ${username}`])[0];
                // Set the user's bank details if they exist
                if (userInfo) {
                    setPaymentDetails(details => ({
                        ...details,
                        bsb: userInfo.accountbsb,
                        accountNumber: userInfo.accountnumber,
                        cardNumber: userInfo.cardnumber,
                        cardExpiry: userInfo.cardexpirydate,
                    }));
                    setDetailsExist(true);
                    // Update their balance
                    setFundsAmount(userInfo.balance);
                }
            } catch (error) {
                return;
            }
		}
		retrieveUserBankDetails();
	}, [triggerRender]);

	// Handles adding/changing bank details
	const handleBankChange = () => {

        let body = {
            "username": username,
            "bankname": null,
            "accountname": null,
            "accountbsb": BSBChange,
            "accountnumber": accountNumberChange,
            "cardtitle": null,
            "cardnumber": cardNumberChange,
            "cardexpirydate": cardExpiryChange,
            "cardccv": null
        }
        // Used to add new bank details, given the changes in the input fields
		async function addBank() {
			try {
				const response = await makeRequest("/bankaccounts/create_account", "POST", body, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp);
                    return;
				} 
                setDetailsExist(true);
                setBSBChange('');
                setAccountNumberChange('');
                setCardNumberChange('');
                setCardExpiryChange('');
                setButtonDisabled(true);
                setTriggerRender(triggerRender === true ? false : true);
			} catch (error) {
				console.log(error)
			}
		}

        // Used to update the bank details, given the changes in the input fields
        async function changeBank() {
			try {
				const response = await makeRequest(`/bankaccounts/update_account/${username}`, "PUT", body, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp);
                    return;
				}
                setBSBChange('');
                setAccountNumberChange('');
                setCardNumberChange('');
                setCardExpiryChange('');
                setButtonDisabled(true);
                setTriggerRender(triggerRender === true ? false : true);
			} catch (error) {
				console.log(error)
			}
		}
        // Runs the appropriate function depending on the button the user clicks
		if (modalState === 'add') {
            addBank();
        } else {
            changeBank();
        }		
		setShowModal(false);
	}

    // Uses regular expressions to validate the user's inputs
    const validateDetails = (type: string) => {

        // RegExp for checking BSB format
        let regex = /^\d{3}-\d{3}$/;
        let isValid = false;

        // Should be in form xxx-xxx
        if (type === "bsb") {
            isValid = regex.test(BSBChange);
            if (!isValid) setBSBCheck(true);
            if (isValid) setBSBCheck(false);
        // Should be in form xxxxxx
        } else if (type === "account") {
            regex = /^[1-9]\d{5,9}$/;
            isValid = regex.test(accountNumberChange);
            if (!isValid) setAccountNumberCheck(true);
            if (isValid) setAccountNumberCheck(false);
        // Should be in form xxxx-xxxx-xxxx-xxxx
        } else if (type === "card") {
            regex = /^\d{4}-\d{4}-\d{4}-\d{4}$/;
            isValid = regex.test(cardNumberChange);
            if (!isValid) setCardNumberCheck(true);
            if (isValid) setCardNumberCheck(false);
        // Should be in form xx/xx
        } else {
            regex = /^(0[1-9]|1[0-2])\/\d{2}$/;
            isValid = regex.test(cardExpiryChange);
            if (!isValid) setCardExpiryCheck(true);
            if (isValid) setCardExpiryCheck(false);
        }
        // Ensures all fields are filled
        if (!bsbCheck && !accountNumberCheck && !cardNumberCheck && !cardExpiryCheck && BSBChange && accountNumberChange && cardNumberChange && cardExpiryChange) setButtonDisabled(false);
    };

    // Handles deleting the bank details
    const handleDelete = () => {
        async function deleteBank() {
			try {
				const response = await makeRequest(`/bankaccounts/delete_account?username=${username}&confirm=true`, "DELETE", undefined, { token })
				if (response.status !== 200) {
					setErrorMessage(response.resp);
				}
                // Resets the state variables and sets the funds to 0
                setDetailsExist(false);
                setTriggerRender(triggerRender === true ? false : true);
                setPaymentDetails(details => ({
                    ...details,
                    bsb: '',
                    accountNumber: '',
                    cardNumber: '',
                    cardExpiry: '',
                }));
                setFundsAmount(0);
			} catch (error) {
				console.log(error)
			}
		}
        deleteBank();
        setShowModal(false)
    }

    // Sends a request to add funds to the user's account
    const addFunds = () => {
        const token = localStorage.getItem("authToken");
        const username = localStorage.getItem("username");
        if (!token || !username) return;
        makeRequest(`/bankaccounts/deposit/${username}?deposit=${addFundsAmount}`, "PUT", undefined, { token })
            .then((resp) => {
                if (resp.status === 200) {
                    setFundsAmount(resp.resp["New Balance"]);
                } else {
                    setErrorMessage(resp.resp.detail);
                }
                setAddFundsAmount(0);
            });
    }

    // Sends a request to withdraw funds from a user's account
    const withdrawFunds = () => {
        const token = localStorage.getItem("authToken");
        const username = localStorage.getItem("username");
        if (!token || !username) return;
        makeRequest(`/bankaccounts/withdraw/${username}?withdraw=${withdrawFundsAmount}`, "PUT", undefined, { token })
            .then((resp) => {
                if (resp.status === 200) {
                    setFundsAmount(resp.resp["New Balance"]);
                } else {
                    setErrorMessage(resp.resp.detail);
                }
                setWithdrawFundsAmount(0);
            });
    }

	// Handles showing the modal
	const handleShow = (type: string) => {
		setModalState(type);
		setShowModal(true)
	};

	// Handles closing the modal
	const handleClose = () => {
        setShowModal(false);
        setButtonDisabled(true);
    };

    return (
        <>
            <Container>
                <Row className="text-center">
                    <Col className="text-center">
                        <span><i>your funds</i></span><br />
                        <span style={{ fontSize: '40pt' }}>${fundsAmount.toFixed(1)}</span>
                    </Col>
                    <Col>
                        <Row>
                            <Col className="text-center">
                                <InputGroup className="mb-3">
                                    <Form.Control placeholder="$" type="number" value={addFundsAmount} onChange={(event) => setAddFundsAmount(parseInt(event.target.value, 10))}/>
                                    <Button variant="success" style={{ width: '140px' }} disabled={detailsExist ? false : true} onClick={addFunds}>add funds</Button>
                                </InputGroup>
                            </Col>
                        </Row>
                        <Row>
                            <Col className="text-center">
                                <InputGroup className="mb-3">
                                    <Form.Control placeholder="$" type="number" value={withdrawFundsAmount} onChange={(event) => setWithdrawFundsAmount(parseInt(event.target.value, 10))}/>
                                    <Button variant="danger" style={{ width: '140px' }} disabled={detailsExist ? false : true} onClick={withdrawFunds}>withdraw funds</Button>
                                </InputGroup>
                            </Col>
                        </Row>
                    </Col>
                </Row>
                <hr style={{ height: '3px', background: 'black' }}/>
                <Row className="text-center">
                    <span><i>your bank details</i></span><br /><br />
                    <InputGroup className="mb-3">
                        <InputGroup.Text style={{ width: '150px' }}>bsb</InputGroup.Text>
                        <Form.Control disabled value={paymentDetails.bsb} />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text style={{ width: '150px' }}>account number</InputGroup.Text>
                        <Form.Control disabled value={paymentDetails.accountNumber} />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text style={{ width: '150px' }}>card number</InputGroup.Text>
                        <Form.Control disabled value={paymentDetails.cardNumber} />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text style={{ width: '150px' }}>card expiry</InputGroup.Text>
                        <Form.Control disabled value={paymentDetails.cardExpiry} />
                    </InputGroup>
                </Row>
                <Row className="text-center">
                    <Col>
                        <Button variant="success" style={{ width: '100px' }} disabled={detailsExist ? true : false} onClick={() => handleShow('add')}>add</Button>
                    </Col>
                    <Col>
                        <Button style={{ width: '100px' }} disabled={detailsExist ? false : true} onClick={() => handleShow('change')}>change</Button>
                    </Col>
                    <Col>
                        <Button variant="danger" style={{ width: '100px' }} disabled={detailsExist ? false : true} onClick={() => handleShow('delete')}>remove</Button>
                    </Col>
                </Row>

                <Modal show={showModal} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>payment details 💳</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        { modalState !== "delete" &&
                        <Form>
                            <Form.Group className="mb-3">
                                <Form.Label>BSB</Form.Label>
                                <Form.Control type="text" required onBlur={() => validateDetails("bsb")} onChange={(event) => setBSBChange(event.target.value)}/>
                                { bsbCheck && 
                                <span style={{ fontSize: "8pt", color: "red" }}>BSB must be in xxx-xxx format!</span>
                                }
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>account number</Form.Label>
                                <Form.Control type="text" required onBlur={() => validateDetails("account")} onChange={(event) => setAccountNumberChange(event.target.value)}/>
                                { accountNumberCheck && 
                                <span style={{ fontSize: "8pt", color: "red" }}>Account number must be 6-10 digits with no leading zeros!</span>
                                }
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>card number</Form.Label>
                                <Form.Control type="text" required onBlur={() => validateDetails("card")} onChange={(event) => setCardNumberChange(event.target.value)}/>
                                { cardNumberCheck && 
                                <span style={{ fontSize: "8pt", color: "red" }}>Card number must be in xxxx-xxxx-xxxx-xxxx format!</span>
                                }
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>card expiry</Form.Label>
                                <Form.Control type="text" required onBlur={() => validateDetails("expiry")} onChange={(event) => setCardExpiryChange(event.target.value)}/>
                                { cardExpiryCheck && 
                                <span style={{ fontSize: "8pt", color: "red" }}>Card expiry must be in MM/YY format!</span>
                                }
                            </Form.Group>
                            <Button disabled={buttonDisabled === true ? true : false} onClick={handleBankChange}>save changes</Button>
                        </Form>
                        }
                        { modalState === "delete" &&
                        <>
                            <Row className="text-center">
                                <span>Are you sure you want to delete your payment details?</span><br />
                                <span><b>You will lose all the funds associated with your account</b> 😱</span><br /><br />
                            </Row>  
                            <Row>
                                <Col className="text-center">
                                    <Button style={{ width: '100px' }} onClick={handleClose}>No</Button>
                                </Col>
                                <Col className="text-center">
                                    <Button variant="danger" style={{ width: '100px' }} onClick={handleDelete}>Yes</Button>
                                </Col>
                            </Row>
                        </>
                        }
                    </Modal.Body>
                </Modal>
            </Container>
            <Modal show={!!errorMessage} onHide={() => setErrorMessage("")}>
                <Modal.Header>
                    <Modal.Title>Error</Modal.Title>
                </Modal.Header>
                <Modal.Body>{errorMessage}</Modal.Body>
                <Modal.Footer>
                    <Button onClick={() => setErrorMessage("")}>OK</Button>
                </Modal.Footer>
            </Modal>
        </>
    )
}





