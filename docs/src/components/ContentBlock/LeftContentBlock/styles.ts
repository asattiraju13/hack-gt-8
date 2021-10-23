import styled from "styled-components";

export const LeftContentSection = styled("section")`
  position: relative;
  padding: 0rem 0 8rem;
  height: 100vh;
  width; 100vw;
  padding-top: 10%;
  @media only screen and (max-width: 1024px) {
    padding: 4rem 0 4rem;
  }
`;

export const Content = styled("p")`
  margin: 1.5rem 0 2rem 0;
`;

export const ContentWrapper = styled("div")`
  position: relative;
  

  @media only screen and (max-width: 575px) {
    padding-top: 4rem;
  }
`;

export const ServiceWrapper = styled("div")`
  display: flex;
  justify-content: space-between;
  max-width: 100%;
`;

export const MinTitle = styled("h4")`
  font-size: 25px;
  line-height: 1rem;
  padding: 0.5rem 0;
  text-transform: uppercase;
  color: #373737;
  font-family: "Motiva Sans Light", sans-serif;
`;

export const MinPara = styled("p")`
  font-size: 13px;
`;
