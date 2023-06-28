import { Button, FloatingLabel, Form } from "react-bootstrap";
import { FormContainer } from "../components/StyledFormContainer";
import { useState } from "react";

type SpaceType = "indoor-lot"
  | "outdoor-lot"
  | "undercover"
  | "outside"
  | "carport"
  | "driveway"
  | "garage"


type LisitngInfo = {
  address: string;
  spaceType: string;
  vehicleType: string;
  accessKey?: boolean;
  length?: number;
  width?: number;
}

export const ListingForm = () => {
  const [info, setInfo] = useState<LisitngInfo>({
    address: '',
    spaceType: '',
    vehicleType: ''
  });

  const [error, setError] = useState<string>();
  
  return (
    <FormContainer>
      <div style={{ margin: "30px 15px" }}>
        <FloatingLabel controlId="floatingAddress" label="What is the address?" className="mb-3">
          <Form.Control
            type="text"
            placeholder="What is the address?"
            value={info.address}
            onChange={(event) => setInfo({...info, address: event.target.value})}
          />
        </FloatingLabel>
        <FloatingLabel controlId="floatingPassword" label="Password" className="mb-3">
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </FloatingLabel>
        {error && <span style={{ color: "#D7504D", fontSize: "14px" }}>{error}</span>}
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleLogin}
            disabled={!allFilledOut}
          >Add Listing</Button>
        </div>
      </div>
    </FormContainer>
  );
};
