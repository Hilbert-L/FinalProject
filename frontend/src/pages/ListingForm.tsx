import { Button, Col, FloatingLabel, Form, Row } from "react-bootstrap";
import { FormContainer } from "../components/StyledFormContainer";
import { useState } from "react";
import { makeRequest } from "../helpers";
import { useNavigate } from "react-router-dom";

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

type LisitngInfo = {
  address?: string;
  spaceType?: SpaceType;
  vehicleType?: VehicleType;
  accessKey?: boolean;
  length?: number;
  width?: number;
}

export const ListingForm = () => {
  const [info, setInfo] = useState<LisitngInfo>({});

  const [error, setError] = useState<string>();

  const navigate = useNavigate();

  const token = localStorage.getItem("authToken")!;

  const handleSubmit = () => {
    const body = {
      "Address": String(info.address),
      "SpaceType": String(info.spaceType),
      "VehicleSize": String(info.vehicleType),
      "AccessKeyRequired": String(info.accessKey),
      "Breadth": String(info.length),
      "Width": String(info.width),
    };
    makeRequest("/carspace/create_car_space", "POST", body, { token })
      .then((response) => {
        if (response.status === 200) navigate("/");
        else setError(response.resp.detail);
      })
  }

  const allFilledOut = info.address !== undefined
    && info.spaceType !== undefined
    && info.vehicleType !== undefined
    && info.accessKey !== undefined
    && info.width !== undefined
    && info.length !== undefined
  
  return (
    <FormContainer width="500px" top="50px">
      <div style={{ margin: "30px 15px" }}>
        <h1 style={{textAlign: "center"}}>Add your car space</h1>
        <Form.Group>
          <br />
          <Form.Label>What is the address?</Form.Label>
            <FloatingLabel controlId="floatingAddress" label="Address" className="mb-3">
              <Form.Control
                type="text"
                placeholder="Address"
                value={info.address}
                onChange={(event) => setInfo({...info, address: event.target.value})}
              />
            </FloatingLabel>
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
          <Form.Label>What's the largest type of vehicle can it hold?</Form.Label>
          <FloatingLabel controlId="floatingVehicleType" label="Vehicle Type" className="mb-3">
            <Form.Select
              value={info.vehicleType}
              onChange={
                (event) => {console.log(event.target.value); setInfo({
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
        {error && <span style={{ color: "#D7504D", fontSize: "14px" }}>{error}</span>}
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleSubmit}
            disabled={!allFilledOut}
          >Add Listing</Button>
        </div>
      </div>
    </FormContainer>
  );
};
