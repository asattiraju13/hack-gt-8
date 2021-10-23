import styled from "styled-components";

export const WindowContainer = styled("div")`
  width: 100vw;
  height: 100vh;
  color: #373737;
`;

export const HeadingContent = styled("h6")`
  color: #F8F0E3;
  padding:  40px;
`;

export const RightBlockContainer = styled("section")`

  background: #373737;
  width: auto;
  height: 100vh;
  color: #F8F0E3;
  margin-left: 0;
  padding-top: calc(50% - 800px);

  @media only screen and (max-width: 1024px) {
    padding: 0rem 0 9rem;
  }

  @media only screen and (max-width: 768px) {
    padding: 0rem 0 6rem;
  }
`;

export const Content = styled("p")`
  margin: 1.5rem 0 2rem 0;
  color: #F8F0E3;
  padding:  40px;
`;

export const ContentWrapper = styled("div")`
  position: relative;
  max-width: 540px;
  color: #F8F0E3;

  @media only screen and (max-width: 575px) {
    padding-bottom: 5rem;
  }
`;

export const ButtonWrapper = styled("div")`
  display: flex;
  justify-content: left;
  max-width: 100%;

  @media screen and (min-width: 1024px) {
    max-width: 80%;
  }

  button:last-child {
    margin-left: 20px;
  }
`;
