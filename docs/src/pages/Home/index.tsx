import { lazy } from "react";
import IntroContent from "../../content/IntroContent.json";
import AboutContent from "../../content/AboutContent.json";
import MissionContent from "../../content/MissionContent.json";

const Container = lazy(() => import("../../common/Container"));
const ScrollToTop = lazy(() => import("../../common/ScrollToTop"));
const ContentBlock = lazy(() => import("../../components/ContentBlock"));

const Home = () => {
  return (
    <Container>
      <ScrollToTop />
      <ContentBlock
        type="left"
        title={IntroContent.title}
        content={IntroContent.text}
        button={IntroContent.button}
        icon="mascot.png"
        id="intro"
      />
      <ContentBlock
        type="right"
        title={MissionContent.title}
        content={MissionContent.text}
        icon="Howitani-1.m4v"
        id="mission"
      />
      <ContentBlock
        type="left"
        title={AboutContent.title}
        content={AboutContent.text}
        icon="graphs.svg"
        id="about"
      />
      {/* <ContentBlock
        type="left"
        title={ProductContent.title}
        content={ProductContent.text}
        icon="waving.svg"
        id="product"
      />
      <Contact
        title={ContactContent.title}
        content={ContactContent.text}
        id="contact"
      /> */}
    </Container>
  );
};

export default Home;
