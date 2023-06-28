import styled from "styled-components";

export const FormContainer = styled.div<{width?: string, top?: string}>`
  margin: auto;
  width: ${props => props.width || "350px"};
  margin-top: ${props => props.top || "100px"};
  margin-bottom: 100px;
  border: 1px solid;
  border-radius: 0.375rem;
`;