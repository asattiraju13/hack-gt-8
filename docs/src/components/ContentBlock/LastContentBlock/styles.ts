import styled from "styled-components";

export const MemberName = styled("h6")`
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  justify-content: center;
`;

export const LeftContentSection = styled("section")`
  position: relative;
  padding: 0px 30px 30px 60px;
  height: 100vh;
  width: 100vw;
  padding-top: 5%;
  @media only screen and (max-width: 1024px) {
    padding: 0rem 0rem;
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

export const HeadingContent = styled("h6")`
  color: #373737;
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
