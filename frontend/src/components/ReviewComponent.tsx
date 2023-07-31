import { Button, Col, FloatingLabel, Form, Row, Modal } from "react-bootstrap";
import { useState, useEffect } from "react";
import { makeRequest } from '../helpers';

  type ReviewInfo = {
    username?: string;
    overall?: string;
    location?: string;
    cleanliness?: string;
    easeofaccess?: string;
    communication?: string;
    writtenfeedback?: string;
  }

export const ReviewComponent = (props: any) => { 

    const token = props.token;
    const [review, setReview] = useState<ReviewInfo>({});

    const postReview = async () => {
        try {
            const body = {
                ownerusername: review.username,
                overall: review.overall,
                location: review.location,
                cleanliness: review.cleanliness,
                easeofaccess: review.easeofaccess,
                communication: review.communication,
                writtenfeedback: review.writtenfeedback
            }
            let response = await makeRequest(`/carspace/create_review?carspaceid=${props.listing}`, "POST", body, { token });
            if (response.status !== 200) {
                console.log("There was an error!")
            }
        } catch (error) {
            console.log(error);
        }
        props.onClose();
    }

    const allFilledOut = review.overall !== undefined
    && review.location !== undefined
    && review.cleanliness !== undefined
    && review.easeofaccess !== undefined
    && review.communication !== undefined
    && review.writtenfeedback !== undefined

    return (
        <>
            <Modal.Body>
                <Form.Group>
                    <Form.Label>Location</Form.Label>
                    <FloatingLabel controlId="floatingLocation" label="Location" className="mb-3">
                        <Form.Select
                        value={review.location}
                        onChange={
                            (event) => {setReview({
                            ...review,
                            location:
                                event.target.value === "none"
                                ? undefined
                                : event.target.value
                            })}
                        }>
                        <option value="none">-</option>
                        <option value="1">⭐</option>
                        <option value="2">⭐⭐</option>
                        <option value="3">⭐⭐⭐</option>
                        <option value="4">⭐⭐⭐⭐</option>
                        <option value="5">⭐⭐⭐⭐⭐</option>
                        </Form.Select>
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                    <Form.Label>Cleanliness</Form.Label>
                    <FloatingLabel controlId="floatingCleanliness" label="Cleanliness" className="mb-3">
                        <Form.Select
                        value={review.cleanliness}
                        onChange={
                            (event) => {setReview({
                            ...review,
                            cleanliness:
                                event.target.value === "none"
                                ? undefined
                                : event.target.value
                            })}
                        }>
                        <option value="none">-</option>
                        <option value="1">⭐</option>
                        <option value="2">⭐⭐</option>
                        <option value="3">⭐⭐⭐</option>
                        <option value="4">⭐⭐⭐⭐</option>
                        <option value="5">⭐⭐⭐⭐⭐</option>
                        </Form.Select>
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                    <Form.Label>Ease of Access</Form.Label>
                    <FloatingLabel controlId="floatingEaseOfAccess" label="Ease of Access" className="mb-3">
                        <Form.Select
                        value={review.easeofaccess}
                        onChange={
                            (event) => {setReview({
                            ...review,
                            easeofaccess:
                                event.target.value === "none"
                                ? undefined
                                : event.target.value
                            })}
                        }>
                        <option value="none">-</option>
                        <option value="1">⭐</option>
                        <option value="2">⭐⭐</option>
                        <option value="3">⭐⭐⭐</option>
                        <option value="4">⭐⭐⭐⭐</option>
                        <option value="5">⭐⭐⭐⭐⭐</option>
                        </Form.Select>
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                    <Form.Label>Communication</Form.Label>
                    <FloatingLabel controlId="floatingCommunication" label="Communication" className="mb-3">
                        <Form.Select
                        value={review.communication}
                        onChange={
                            (event) => {setReview({
                            ...review,
                            communication:
                                event.target.value === "none"
                                ? undefined
                                : event.target.value
                            })}
                        }>
                        <option value="none">-</option>
                        <option value="1">⭐</option>
                        <option value="2">⭐⭐</option>
                        <option value="3">⭐⭐⭐</option>
                        <option value="4">⭐⭐⭐⭐</option>
                        <option value="5">⭐⭐⭐⭐⭐</option>
                        </Form.Select>
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                    <Form.Label>Overall</Form.Label>
                    <FloatingLabel controlId="floatingOverall" label="Overall" className="mb-3">
                        <Form.Select
                        value={review.overall}
                        onChange={
                            (event) => {console.log(event.target.value); setReview({
                            ...review,
                            overall:
                                event.target.value === "none"
                                ? undefined
                                : event.target.value
                            })}
                        }>
                        <option value="none">-</option>
                        <option value="1">⭐</option>
                        <option value="2">⭐⭐</option>
                        <option value="3">⭐⭐⭐</option>
                        <option value="4">⭐⭐⭐⭐</option>
                        <option value="5">⭐⭐⭐⭐⭐</option>
                        </Form.Select>
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                <Form.Label>Comment</Form.Label>
                    <FloatingLabel controlId="floatingComment" label="Comment" className="mb-3">
                    <Form.Control
                            type="text"
                            value={review.writtenfeedback}
                            placeholder="Comment"
                            onChange={event => setReview({...review, writtenfeedback: event.target.value})}
                        />
                    </FloatingLabel>
                </Form.Group>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="primary" disabled={!allFilledOut} onClick={postReview}>Post Review</Button>
            </Modal.Footer>
        </>
    )
}