import { Button, Col, FloatingLabel, Form, Row, Modal } from "react-bootstrap";
import { useState, useEffect } from "react";
import { makeRequest } from '../helpers';

type SpaceType = 
  | "indoor-lot"
  | "outdoor-lot"
  | "undercover"
  | "outside"
  | "carport"
  | "driveway"
  | "locked-garage"

type VehicleType = 
  | "hatchback"
  | "sedan"
  | "suv"
  | "ev"
  | "ute"
  | "wagon"
  | "van"
  | "bike"

  type ListingInfo = {
    address?: string;
    spaceType?: SpaceType;
    vehicleType?: VehicleType;
    accessKey?: boolean;
    length?: number;
    width?: number;
    price?: number;
    photo?: string;
  }

export const ListingComponent = (props: any) => {  

    const token = props.token;
    const [info, setInfo] = useState<ListingInfo>({});

    useEffect(() => {
        const currentListing = props.allListings.find((listing: any) => listing["Your Car Space Information"].carspaceid === props.listing);
        const currentListingInfo = currentListing["Your Car Space Information"];

        setInfo(info => ({
            ...info,
            address: currentListingInfo.address,
            spaceType: currentListingInfo.spacetype,
            vehicleType: currentListingInfo.vehiclesize,
            accessKey: currentListingInfo.accesskeyrequired,
            length: currentListingInfo.breadth,
            width: currentListingInfo.width,
            price: currentListingInfo.price
        }))
    }, [])

    const updateListing = async () => {
        // try {
        //     const body = {
        //         width: info.width,
        //         breadth: info.length,
        //         spacetype: info.spaceType,
        //         accesskeyrequired: info.accessKey,
        //         vehiclesize: info.vehicleType,
        //         price: info.price,
        //     }
        //     let response = await makeRequest(`/carspace/updatecarspace/${props.username}/${props.listing}`, "PUT", body, { token });
        //     if (response.status !== 200) {
        //         console.log("There was an error!")
        //     }
        // } catch (error) {
        //     console.log(error);
        // }
        props.onClose();
    }

    const allFilledOut = info.spaceType !== undefined
    && info.vehicleType !== undefined
    && info.accessKey !== undefined
    && info.width !== undefined
    && info.length !== undefined
    && info.price !== undefined
    && !isNaN(info.width)
    && !isNaN(info.length)
    && !isNaN(info.price)


    return (
        <>
            <Modal.Body>
                <Form.Group>
                    <Form.Label>What is the address?</Form.Label>
                        <Form.Control
                        type="text"
                        className="mb-3"
                        value={info.address}
                        disabled
                        placeholder="Address"
                        />
                </Form.Group>
                <Form.Group>
                    <Form.Label>What type of car space is this?</Form.Label>
                    <FloatingLabel controlId="floatingSpaceType" label="Space Type" className="mb-3">
                        <Form.Select
                        value={info.spaceType}
                        onChange={
                            (event) => setInfo({
                            ...info,
                            spaceType:
                                event.target.value === "none"
                                ? undefined
                                : event.target.value as SpaceType
                            })
                        }
                        >
                        <option value="none">Space type</option>
                        <option value="indoor-lot">Indoor Lot</option>
                        <option value="outdoor-lot">Outdoor Lot</option>
                        <option value="undercover">Undercover</option>
                        <option value="outside">Outside</option>
                        <option value="carport">Carport</option>
                        <option value="driveway">Driveway</option>
                        <option value="locked-garage">Locked Garage</option>
                        </Form.Select>
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                <Form.Label>What's the largest type of vehicle it can hold?</Form.Label>
                <FloatingLabel controlId="floatingVehicleType" label="Vehicle Type" className="mb-3">
                    <Form.Select
                    value={info.vehicleType}
                    onChange={
                        (event) => {setInfo({
                        ...info,
                        vehicleType:
                            event.target.value === "none"
                            ? undefined
                            : event.target.value as VehicleType
                        })}
                    }>
                    <option value="none">Vehicle type</option>
                    <option value="hatchback">Hatchback</option>
                    <option value="sedan">Sedan</option>
                    <option value="suv">SUV</option>
                    <option value="ev">EV</option>
                    <option value="ute">Ute</option>
                    <option value="wagon">Wagon</option>
                    <option value="van">Van</option>
                    <option value="bike">Bike</option>
                    </Form.Select>
                </FloatingLabel>
                </Form.Group>
                <Form.Group>
                <Form.Label>Is an access key required?</Form.Label>
                <div className="mb-1">
                    <Form.Check 
                    checked={info.accessKey === true}
                    onChange={() => setInfo({...info, accessKey: true})}
                    inline
                    name="access-key"
                    label="Yes"
                    type="radio"
                    />
                    <Form.Check
                    checked={info.accessKey === false}
                    onChange={() => setInfo({...info, accessKey: false})}
                    inline
                    name="access-key"
                    label="No"
                    type="radio"
                    />
                </div>
                </Form.Group>
                <Form.Group>
                <br />
                <Form.Label>How big is the car space (in metres)?</Form.Label>
                <Row>
                    <Col>
                    <FloatingLabel controlId="floatingLength" label="Length (metres)" className="mb-3">
                        <Form.Control
                        type="number"
                        placeholder="Length (metres)"
                        value={info.length}
                        onChange={event => setInfo({...info, length: parseInt(event.target.value, 10)})}
                        />
                    </FloatingLabel>
                    </Col>
                    <Col>
                    <FloatingLabel controlId="floatingWidth" label="Width (metres)" className="mb-3">
                        <Form.Control
                        type="number"
                        placeholder="Width (metres)"
                        value={info.width}
                        onChange={event => setInfo({...info, width: parseInt(event.target.value, 10)})}
                        />
                    </FloatingLabel>
                    </Col>
                </Row>
                </Form.Group>
                <Form.Group>
                <Form.Label>What is the price per day?</Form.Label>
                    <FloatingLabel controlId="floatingPrice" label="Price" className="mb-3">
                    <Form.Control
                            type="number"
                            value={info.price}
                            placeholder="Price"
                            onChange={event => setInfo({...info, price: parseInt(event.target.value, 10)})}
                        />
                    </FloatingLabel>
                </Form.Group>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="primary" disabled={!allFilledOut} onClick={updateListing}>Update</Button>
            </Modal.Footer>
        </>
    )
}